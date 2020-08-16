import mconv

try:
    from vars import path
except Exception as ex:
    print(f'Can not: `from .vars import path` -> Exception: {ex}')
    path = input('Enter path:')


report = mconv.printable_report(path)
print(report)
