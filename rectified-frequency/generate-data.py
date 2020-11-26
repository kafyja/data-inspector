import argparse
import glob
import gzip
import json

import jsonlines
from tqdm import tqdm

ALL_FEATURES = {
    'concentration', 'conceptKeyFrequencyInDoc', 'discontinuousFrequencyInDoc',
    'frequencyInCorpus', 'frequencyPerDocument', 'fullText',
    'g_highDocumentFrequentHighRankedConcept', 'globalScore',
    'hasManyDisplayForms', 'highScoring', 'hits', 'hitsRatioToCorpusSize',
    'isAbbreviation', 'isAbbreviationDefinition', 'isBadUnigram',
    'isDescriptionConceptInDoc', 'isMaterialSubstance', 'isNounPhraseInCorpus',
    'isOntologyMatch', 'isRareConceptWithLeadingDigit', 'isValid', 'jsonExport',
    'localScore', 'maxFrequencyInSingleDocument', 'maxNgramSizeInCorpus',
    'maxSupergramFrequencyInCorpus', 'maxSupergramFrequencyInDoc',
    'minRectifiedFrequencyInCorpus', 'minRectifiedFrequencyInDoc',
    'mostCommonDisplayInCorpus', 'mostCommonPosTagPatternFrequencyInCorpus',
    'ngramFrequencyInCorpus', 'ngramFrequencyInDoc', 'ngramSize',
    'normalizedConceptKeyFrequencyInDoc', 'normalizedDiscontinuousTfInDoc',
    'normalizedFrequencyInCorpus', 'normalizedFrequencyPerDocument',
    'normalizedGlobalScore', 'normalizedIdf',
    'normalizedLeastFrequentTermCountInCorpus',
    'normalizedMinRectifiedFrequencyInCorpus',
    'normalizedMinRectifiedFrequencyInDoc',
    'normalizedNgramFrequencyInCorpus', 'normalizedNgramFrequencyInDoc',
    'normalizedPmi', 'normalizedRectifiedFrequencyInCorpus',
    'normalizedRectifiedFrequencyInDoc', 'normalizedRectifiedTfInDoc',
    'normalizedSummaryConceptKeyFrequencyInCorpus', 'normalizedTfIdfInDoc',
    'pmi', 'rectifiedFrequencyInCorpus', 'rectifiedFrequencyInDoc',
    'sentenceCentralityInDocument', 'sentenceFactClueScoreInDocument',
    'summaryConceptKeyFrequencyInDoc', 'variationsCount', 'weighedFeaturesScore'
}

RELEVANT_FEATURES = {
    'discontinuousFrequencyInDoc', 'frequencyInCorpus', 'jsonExport',
    'minRectifiedFrequencyInCorpus', 'minRectifiedFrequencyInDoc',
    'mostCommonDisplayInCorpus', 'normalizedMinRectifiedFrequencyInCorpus',
    'normalizedMinRectifiedFrequencyInDoc', 'normalizedNgramFrequencyInCorpus',
    'normalizedNgramFrequencyInDoc', 'normalizedPmi',
    'normalizedRectifiedFrequencyInCorpus', 'normalizedRectifiedFrequencyInDoc',
    'normalizedRectifiedTfInDoc', 'normalizedTfIdfInDoc',
    'rectifiedFrequencyInCorpus', 'rectifiedFrequencyInDoc'
}

parser = argparse.ArgumentParser()
parser.add_argument('output_name', type=str)
parser.add_argument('json_glob_pattern', type=str)
args = parser.parse_args()

file_paths = glob.glob(args.json_glob_pattern, recursive=True)

output = []

for fp in tqdm(file_paths, 'Getting concept features'):
    with gzip.open(fp) as file:
        data = json.load(file)
    concepts = data['concepts']
    for concept in concepts:
        features = {f['label']: f['value'] for f in concept['features']
                    if f['label'] in RELEVANT_FEATURES}
        features['document'] = data['_id']
        features['key'] = concept['key'] + '-' + features['document']
        output.append(features)

print('Writing file ...')
if not args.output_name.endswith(".jsonl"):
    args.output_name += ".jsonl"
with jsonlines.open(args.output_name, 'w') as out:
    out.write(
        {'conceptCount': len(output), }
    )
    out.write_all(output)
