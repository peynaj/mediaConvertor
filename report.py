import mconv

try:
    from vars import path
except Exception as ex:
    print(f'Can not: `from .vars import path` -> Exception: {ex}')
    path = input('Enter path:')

details = mconv.get_audio_details(path)

# === report ===
r = []
r.append('{x} REPORT {x}'.format(x='=' * 25))
r.append(f'* Path: {path}')
r.append('=' * 58)

items = list(details.items())
items.sort(key=lambda x: x[0])
folders_detail = dict()

for k, v in items:
    name = k[len(path)+1:]
    r.append(f'/{name} => {v:.3f}')

    folder = name.split('/')[0]
    if folder not in folders_detail:
        folders_detail[folder] = dict(cnt=1, dur=v)
    else:
        folders_detail[folder]['cnt'] += 1
        folders_detail[folder]['dur'] += v

r.append('')

report_base = ' {folder:{filler}<{fn}} {separator} {cnt:{filler}^{cn}} {separator} {dur:{filler}^{dn}}'
n = dict(fn=len(max(folders_detail.keys(), key=lambda x: len(x))) + 2, cn=8, dn=10)

r.append(report_base.format(folder='', cnt='', dur='', filler='-', separator='-', **n))
r.append(report_base.format(folder='Folder', cnt='Count', dur='Dur(h)', filler=' ', separator='|', **n))
r.append(report_base.format(folder='', cnt='', dur='', filler='-', separator='+', **n))

all_dur = 0
for folder, detail in sorted(folders_detail.items()):
    dur = detail['dur']/60
    all_dur += dur
    r.append(report_base.format(folder=folder, cnt=detail['cnt'], dur=f'{dur:.3f}', filler=' ', separator='|', **n))

r.append(report_base.format(folder='', cnt='', dur='', filler='-', separator='+', **n))
r.append(report_base.format(folder='All', cnt=len(details), dur=f'{all_dur:.3f}', filler=' ', separator='|', **n))
r.append(report_base.format(folder='', cnt='', dur='', filler='-', separator='-', **n))

print('\n'.join(r))
