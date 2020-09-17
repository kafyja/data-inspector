from tabulate import tabulate


def compare_entries(*entries):
    keys = list(set.union(*[set(entry.keys()) for entry in entries]))
    values = [[key] + [str(entry[key])[:70] if key in entry else None
                       for entry in entries]
              for key in keys]
    print(tabulate(values))
