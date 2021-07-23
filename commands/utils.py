import os
from mutagen.mp3 import MP3

conv = list(" ()|[]")


def change_audio_rate(dir_path, speed_rate=2):
    prefix = 'rt{}'.format(speed_rate)
    if os.path.exists(dir_path):
        folder = dir_path.split('/')[-1]
        new_dir_path = '/'.join(dir_path.split('/')[:-1]) + '/' + prefix + '.' + folder
        os.mkdir(new_dir_path)
        l = list(os.listdir(dir_path))
        l.sort()
        for f in l: # f -> file
            fpath = dir_path + '/' + f
            fname = '.'.join(f.split('.')[:-1])
            new_fpath = new_dir_path + '/' + fname + '.' + prefix + '.mp3'
            '''
            if not os.path.exists(new_fpath):
                open(new_fpath, 'a').close()
            '''
            for c in conv:
                fpath = fpath.replace(c, f"\{c}")
                new_fpath = new_fpath.replace(c, f"\{c}")

            comm = 'ffmpeg -i {old_file} -filter:a "atempo={rate}" -vn {new_file} -y'.format(
                old_file=fpath,
                rate=speed_rate,
                new_file=new_fpath,
            )
            print('\n=======================\n', comm, '\n==========================\n')
            os.system(comm)
            print('# {} -> finished!'.format(new_fpath))


def video_to_audio_and_change_rate(dir_path, speed_rate=2):
    prefix = '.{}.rt{}'.format('ToAud', speed_rate)
    if os.path.exists(dir_path):
        folder = dir_path.split('/')[-1]
        new_dir_path = '/'.join(dir_path.split('/')[:-1]) + '/' + folder + prefix
        try:
            os.mkdir(new_dir_path)
        except Exception as ex:
            print('### Exception in mkdir path: ', ex)
        l = list(os.listdir(dir_path))
        l.sort()
        for f in l:  # f -> file
            fpath = dir_path + '/' + f
            new_fpath = new_dir_path + '/' + '.'.join(f.split('.')[:-1]) + prefix + '.mp3'
            '''
            if not os.path.exists(new_fpath):
                open(new_fpath, 'a').close()
            '''
            for c in conv:
                fpath = fpath.replace(c, "\{}".format(c))
                new_fpath = new_fpath.replace(c, "\{}".format(c))

            comm = 'ffmpeg -i {old_file} -f mp3 -ab 192000 -filter:a "atempo={rate}" -vn {new_file}'.format(
                old_file=fpath,
                rate=speed_rate,
                new_file=new_fpath,
            )
            print(comm)
            os.system(comm)
            print('# {} -> finished!'.format(new_fpath))


def video_to_audio(dir_path):
    prefix = '.{}'.format('ToAud')
    if os.path.exists(dir_path):
        folder = dir_path.split('/')[-1]
        new_dir_path = '/'.join(dir_path.split('/')[:-1]) + '/' + prefix + folder
        os.mkdir(new_dir_path)
        l = list(os.listdir(dir_path))
        l.sort()
        for f in l:  # f -> file
            fpath = dir_path + '/' + f
            new_fpath = new_dir_path + '/' + prefix + '.'.join(f.split('.')[:-1]) + '.mp3'
            '''
            if not os.path.exists(new_fpath):
                open(new_fpath, 'a').close()
            '''
            for c in conv:
                fpath = fpath.replace(c, "\{}".format(c))
                new_fpath = new_fpath.replace(c, "\{}".format(c))

            comm = 'ffmpeg -i {old_file} -f mp3 -ab 192000 -vn {new_file}'.format(
                old_file=fpath,
                new_file=new_fpath,
            )
            print(comm)
            os.system(comm)
            print('# {} -> finished!'.format(new_fpath))


def get_files(bp):
    files = []
    for d in os.listdir(bp):
        if os.path.isfile(os.path.join(bp, d)):
            files.append(os.path.join(bp, d))
        elif os.path.isdir(os.path.join(bp, d)):
            _files = get_files(os.path.join(bp, d))
            files.extend(_files)
    return files


def get_audio_details(p):
    l = get_files(p)
    #d = {i: MP3(i).info.length/60 for i in l if (i.split('.'))[-1]=='mp3'}
    d = {}
    for i in l:
        try:
            d[i] = MP3(i).info.length/60
        except Exception as ex:
            print(i, ':\n', ex)
    return d


def printable_report(path):
    details = get_audio_details(path)

    # === report ===
    r = []
    r.append('{x} REPORT {x}'.format(x='=' * 25))
    r.append(f'* Path: {path}')
    r.append('=' * 60)

    items = list(details.items())
    items.sort(key=lambda x: x[0])
    folders_detail = dict()

    for k, v in items:
        name = k[len(path) + 1:]
        r.append(f'./{name} => {v:.3f}')

        folder = '/'.join(name.split('/')[:-1]) or '.'
        if folder not in folders_detail:
            folders_detail[folder] = dict(cnt=1, dur=v)
        else:
            folders_detail[folder]['cnt'] += 1
            folders_detail[folder]['dur'] += v

    r.append('')

    report_base = ' {folder:{filler}<{fn}} {separator} {cnt:{filler}^{cn}} {separator} {dur:{filler}^{dn}} {separator} {avg:{filler}^{an}}'
    n = dict(fn=max(len(max(folders_detail.keys(), key=lambda x: len(x))), 8) + 2, cn=8, dn=10, an=11)

    separator_line = Colors.ENDC + ' ' + report_base.format(folder='', cnt='', dur='', avg='', filler='-', separator='+', **n)

    r.append(separator_line)
    r.append(Colors.BOLD + ' ' + report_base.format(folder='Folder', cnt='Count', dur='Dur(h)', avg='Avg(m)', filler=' ', separator='|', **n))
    r.append(separator_line)

    all_dur = 0
    all_cnt = 0
    folders_colors = [Colors.OKBLUE, Colors.OKGREEN]
    i = 0
    for folder, detail in sorted(folders_detail.items()):
        cnt = detail.get('cnt', 0)
        dur = detail['dur'] / 60
        avg = (dur * 60 / cnt) if cnt else 0
        all_dur += dur
        all_cnt += cnt
        color = folders_colors[i % len(folders_colors)]
        r.append(color + ' ' + report_base.format(folder=folder, cnt=cnt, dur=f'{dur:.3f}', avg=f'{avg:.3f}', filler=' ', separator='|', **n))
        i += 1

    r.append(separator_line)

    all_avg = (all_dur * 60 / all_cnt) if all_cnt else 0
    r.append(Colors.BOLD + ' ' + report_base.format(folder='All', cnt=all_cnt, dur=f'{all_dur:.3f}', avg=f'{all_avg:.3f}', filler=' ', separator='|', **n))

    r.append(separator_line)

    result = '\n'.join(r)

    return result


def mix_podcast_files(src_path, prefix):
    if not os.path.exists(src_path):
        print(f"Path not found: {src_path}")
        return
    all_directories = [path for path in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, path))]
    all_podcast_directories = [_dir for _dir in all_directories if _dir.startswith(prefix)]
    all_podcast_directories.sort()
    podcast_dir_to_files = dict()
    print("* Podcast Directories:")
    min_dir_file_count = 10**10
    for _dir in all_podcast_directories:
        path = os.path.join(src_path, _dir)
        files = os.listdir(path)
        files.sort()
        podcast_dir_to_files[_dir] = files
        count = len(files)
        if count > 0:
            min_dir_file_count = min(count, min_dir_file_count)
        print(f"* {count:02d} > {_dir}")
        if count == 0:
            do_rm_dir = input(f"### Remove empty directory: [{path}] [Y/n]? ")
            if do_rm_dir.lower() == "y":
                os.system(f"rm -rf {path}")

    if min_dir_file_count == 10**10:
        min_dir_file_count = 0

    if min_dir_file_count == 0:
        print(f"Minimum of directories file count is 0.\nFinished!")
        return
    loop_count = input(f"Enter loop count:\n[Default is {min_dir_file_count}. Enter blank to continue with {min_dir_file_count}]\n")
    if loop_count and not loop_count.isalnum():
        print("Invalid number!")
        return
    if not loop_count:
        loop_count = min_dir_file_count
    else:
        loop_count = min(min_dir_file_count, int(loop_count))

    # === Move files ===
    dest_path = os.path.join(src_path, "0.2.pod.mix")
    if not os.path.exists(dest_path):
        os.system(f"mkdir {dest_path}")
    print(f"* Dest path: {dest_path}")
    last_index = 0
    for file in os.listdir(dest_path):
        file_name_parts = file.split(".")
        index = file_name_parts[0]
        if index.isalnum():
            last_index = max(last_index, int(index))

    print(f"* Last Index: {last_index}")
    for _ in range(loop_count):
        for _dir in all_podcast_directories:
            files = podcast_dir_to_files[_dir]
            if not files:
                print(f"Directory is empty: {_dir}\nFinished!")
                return
            last_index += 1
            file = files[0]
            podcast_dir_to_files[_dir] = files[1:]
            file_name_parts = file.split(".")
            file_name_base = ".".join(file_name_parts[:-1])
            file_name_extension = file_name_parts[-1]
            file_src_path = os.path.join(src_path, _dir, file)
            file_dest_path = os.path.join(dest_path, f"{last_index:02d}.{file_name_base}.{_dir[len(prefix):]}.{file_name_extension}")
            command = f"mv {file_src_path} {file_dest_path}"
            print(f"> {command}")
            os.system(command)
    print("Finished!")
    return


COLORS = dict(
    HEADER='\033[95m',
    OKBLUE='\033[94m',
    OKCYAN='\033[96m',
    OKGREEN='\033[92m',
    WARNING='\033[93m',
    FAIL='\033[91m',
    ENDC='\033[0m',
    BOLD='\033[1m',
    UNDERLINE='\033[4m'
)

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
