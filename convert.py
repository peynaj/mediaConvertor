import mconv

try:
    from vars import path
except Exception as ex:
    print(f'Can not: `from .vars import path` -> Exception: {ex}')
    path = input('Enter path:')

try:
    from vars import rate
except Exception as ex:
    print(f'Can not: `from .vars import rate` -> Exception: {ex}')
    path = float(input('Enter rate:'))

# convert #########
mconv.change_audio_rate(path, rate)
