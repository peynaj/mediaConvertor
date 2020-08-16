import os
import sys
from .utils import printable_report, change_audio_rate, video_to_audio_and_change_rate


report = 'report'
convert = 'convert'


def mconv_help():
    hlp = f'''mconv
=====
mconv {report} [/path/to/directory (default:cwd)]
mconv {convert} [to=v/a (video/audio) (default=a)] [rate=2] [/path/to/directory (default:cwd)]
====='''
    print(hlp)
    return


def main():
    if len(sys.argv) == 1:
        mconv_help()
        return

    else:
        command = sys.argv[1]

        if command == report:
            if len(sys.argv) > 2:
                path = sys.argv[2]
            else:
                path = os.getcwd()
            pr = printable_report(path)
            print(pr)
            return

        elif command == convert:
            to_ = 'a'
            rate = 2
            path = os.getcwd()
            for arg in sys.argv[2:]:
                if arg.startswith('to='):
                    to_ = arg[len('to='):]
                    if to_ not in ['a', 'v']:
                        print(f'Invalid to: {to_}')
                        mconv_help()
                        return
                elif arg.startswith('rate='):
                    rate = arg[len('rate='):]
                    try:
                        rate = float(rate)
                    except Exception as ex:
                        print(f'Invalid rate: {rate}')
                        mconv_help()
                        return
                else:
                    if os.path.exists(arg):
                        path = arg
                    else:
                        print(f'Invalid arg(path?): {arg}')
                        mconv_help()
                        return
            if to_ == 'a':
                change_audio_rate(path, rate)
            elif to_ == 'v':
                video_to_audio_and_change_rate(path, rate)

        else:
            print(f'Invalid command: {command}')
            mconv_help()
