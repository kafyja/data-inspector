from main import load_file

CORPUS = 'cabi'
OUTPUT_DIR = '/Users/kasper.jacobsen/Desktop/diffs'


new_meta, new = load_file('../data/' + CORPUS + '-1000-new.jsonl')
old_meta, old = load_file('../data/' + CORPUS + '-1000-old.jsonl')


new_filtered = {k: v for k, v in new.items()
                if 'belowAllowedMinRectifiedFrequencyInDocAndCorpus' in v
                and 'fullText' not in v}
old_filtered = {k: v for k, v in old.items()
                if 'belowAllowedMinRectifiedFrequencyInDocAndCorpus' in v
                and 'fullText' not in v}


missing = [v for k, v in old_filtered.items() if k not in new_filtered.keys()]
extra = [v for k, v in new_filtered.items() if k not in old_filtered.keys()]


print('Writing files ...')
with open(f'{OUTPUT_DIR}/{CORPUS}-now-filtered.txt', 'w+') as out:
    print(*[', '.join((c['display'], c['key'])) for c in extra], sep='\n',
          file=out)

with open(f'{OUTPUT_DIR}/{CORPUS}-now-filtered-detailed.jsonl', 'w+') as out:
    print(*extra, sep='\n', file=out)

with open(f'{OUTPUT_DIR}/{CORPUS}-now-included.txt', 'w+') as out:
    print(*[', '.join((c['display'], c['key'])) for c in missing], sep='\n',
          file=out)

with open(f'{OUTPUT_DIR}/{CORPUS}-now-included-detailed.jsonl', 'w+') as out:
    print(*missing, sep='\n', file=out)

