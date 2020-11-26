import re
from collections import defaultdict
import difflib
from tqdm import tqdm

data_file = 'specificdata/rdiscoveryconceptresults.txt'

line_format = re.compile(
    r"ID: (\d+) - label: (.+?) - alts: {'input': (\[.+?\]), 'weight': (\d+)}"
)

SPACINGS = {' ', '-', '–'}


class Entry:
    def __init__(self, line: str):
        match = line_format.match(line)
        groups = match.groups()
        if len(groups) != 4:
            raise ValueError('The line does not have the correct format!')
        self.id_ = groups[0]
        self.label = groups[1]
        self.alts = eval(groups[2])
        self.weight = eval(groups[3])

    def __repr__(self):
        return f'Entry({self.label} ({self.id_}):\n{str(self.alts)})'

    def collapsed_alts(self):
        collapsed_alts = {}
        for alt in self.alts:
            reduced_form = reduce_form(alt)
            if reduced_form not in collapsed_alts:
                collapsed_alts[reduced_form] = AltForm(reduced_form)
            collapsed_alts[reduced_form].add(alt)
        return collapsed_alts


class AltForm:
    def __init__(self, collapsed_form):
        self.collapsed_form = collapsed_form
        self.variants = {}
        self._spacings = None

    def add(self, variant: str):
        variant = variant.lower()
        if variant in self.variants:
            return
        self._spacings = None
        spacings = set()
        diffs = list(difflib.ndiff(self.collapsed_form, variant))
        for i in range(len(self.collapsed_form)):
            while diffs[i].startswith('+'):
                spacings.add(i)
                diffs.pop(i)
        self.variants[variant] = spacings

    def _update_spacings(self):
        aggregated_spacings = defaultdict(int)
        for variant, spacings in self.variants.items():
            for spacing_index in spacings:
                aggregated_spacings[spacing_index] += 1
        self._spacings = aggregated_spacings

    def get_spacings(self):
        if not self._spacings:
            self._update_spacings()
        return self._spacings

    def _good_and_bad_spacings(self):
        threshold = len(self.variants) / 2
        good, bad = set(), set()
        for spacing, count in self.get_spacings().items():
            if count > threshold:
                good.add(spacing)
            else:
                bad.add(spacing)
        return good, bad

    def ranked_variants(self):
        good, bad = self._good_and_bad_spacings()
        ranked_variants = sorted(
            self.variants,
            key=lambda v: (len(self.variants[v].intersection(good))
                           - len(self.variants[v].intersection(bad)))
            if not contains_multi_space(v) else -10,  # 10 is just a random penalty
            reverse=True
        )
        return ranked_variants

    def __repr__(self):
        variants = str(self.ranked_variants())
        return f'{self.collapsed_form}: {variants}'


def reduce_form(alt_form: str):
    return ''.join(c for c in alt_form.lower() if c not in SPACINGS)


def contains_multi_space(variant: str):
    at_space = False
    for c in variant:
        if not c.isalnum():
            if at_space:
                return True
            else:
                at_space = True
        else:
            at_space = False
    return False


with open(data_file) as data_in:
    entries = [Entry(line) for line in data_in]

alt_forms = [alt_form for entry in tqdm(entries)
             for alt_form in entry.collapsed_alts().values()]

alt_forms.sort(key=lambda af: len(af.get_spacings()) / len(af.collapsed_form),
               reverse=True)
