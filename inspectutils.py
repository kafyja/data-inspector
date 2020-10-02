from tabulate import tabulate


def compare_entries(*entries):
    keys = list(set.union(*[set(entry.keys()) for entry in entries]))
    values = [[key] + [str(entry[key])[:70] if key in entry else None
                       for entry in entries]
              for key in keys]
    print(tabulate(values))


def get_discontinuous_concepts_from_index_file(data: dict):
    concepts = data['concepts']
    return [c for c in concepts
            if any(len(loc['ranges']) > 1 for loc in c['locations'])]

