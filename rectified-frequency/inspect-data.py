import argparse
from main import load_file
from inspectutils import concept_has_feature


CORPUS_RF = 'normalizedMinRectifiedFrequencyInCorpus'
CORPUS_RF_RAW = 'minRectifiedFrequencyInCorpus'
DOC_RF = 'normalizedMinRectifiedFrequencyInDoc'
DOC_RF_RAW = 'minRectifiedFrequencyInDoc'
RF_VALUES = {CORPUS_RF, CORPUS_RF_RAW, DOC_RF, DOC_RF_RAW}


file = '../data/hindawi-1000-new.jsonl'
metadata, data = load_file(file)

fields = {CORPUS_RF, DOC_RF, CORPUS_RF_RAW, DOC_RF_RAW, 'display'}

data = {key: value for key, value in data.items()
        if ('fullText' in value
            or 'belowAllowedMinRectifiedFrequencyInDocAndCorpus' in value)
        and all(f in value for f in RF_VALUES)
        and len(value['display'].split()) > 1}


min_corpus_rf = .1

currently_filtered = sorted(
    ({f: c[f] for f in fields if f in c} for c in data.values()
     if CORPUS_RF in c and DOC_RF_RAW in c and c[DOC_RF_RAW] > 0
     and 'fullText' not in c),
    key=lambda c: c[CORPUS_RF]
)

filtered = sorted(
    ({f: c[f] for f in fields if f in c} for c in data.values()
     if c[CORPUS_RF] < min_corpus_rf
     and (c[DOC_RF] < .7 or c[DOC_RF_RAW] < 3)
     and c[DOC_RF_RAW] > 0),
    key=lambda c: c[CORPUS_RF]
)

unfiltered = sorted(
    ({f: c[f] for f in fields if f in c} for c in data.values()
     if .3 > c[CORPUS_RF] > min_corpus_rf
     or (c[DOC_RF] > .7 and c[DOC_RF_RAW] > 3)
     and c[DOC_RF_RAW] > 0),
    key=lambda c: c[CORPUS_RF]
)
