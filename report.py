import mconv

try:
    from vars import path
except Exception as ex:
    print(f'Can not: `from .vars import path` -> Exception: {ex}')
    path = input('Enter path:')

details = mconv.get_audio_details(path)

# report #########
r = ['=' * 15 + ' REPORT ' + '=' * 15]
r.append(f'* Path: {path}')
r.append(f'* Length: {len(details)}')
r.append(f'* Sum: {sum(details.values())/60} h')
r.append('=' * 40)

for k, v in details.items():
    r.append(f'{k[len(path):]} => {v/60:.5f}')

r.append('=' * 40)

print('\n'.join(r))
