import json
import glob
import os
import gzip
from tqdm import tqdm
import sys
from inspectutils import *


def get_file_path_choice():
    data_files = sorted(f for f in glob.glob('./data/**/*', recursive=True)
                        if os.path.isfile(f))
    for i, path in enumerate(data_files):
        print(i, ':', path)
    print('Input index numbers of file(s) to load from the above list. '
          + 'Use "*" to load all and "-" to exclude certain files.')
    choice = str(input('Choose file(s) to load:'))

    if '-' in choice:
        include, exclude = choice.split('-')
    else:
        include = choice
        exclude = ''
    include = [i for i in include.strip().split() if not i == '']
    exclude = [i for i in exclude.strip().split() if not i == '']
    if include[0] == '*':
        return [data_files[i] for i in range(len(data_files))
                if str(i) not in exclude]
    elif len(include) > 1:
        return [data_files[int(i)] for i in include if i not in exclude]
    else:
        return data_files[int(include[0])]


def _read_json_lines(lines_generator):
    for line in lines_generator:
        info = json.loads(line)
        key = info[determine_key(info)]
        yield key, info


COUNT_FIELDS = {'conceptCount', 'keyCount', 'ngramCount'}


def load_file(filepath: str, as_generator=False):
    extension = os.path.basename(filepath).split('.')[-1]
    if extension == 'jsonl':
        lines_generator = open(filepath)
        return_metadata = json.loads(next(lines_generator))
        for key in COUNT_FIELDS:
            if key in return_metadata:
                total = return_metadata[key]
                break
        else:
            total = None
        if as_generator:
            return return_metadata, _read_json_lines(lines_generator)
        else:
            print('Loading file:', filepath)
            return_data = {key: info for key, info in tqdm(
                _read_json_lines(lines_generator), total=total,
                file=sys.stdout)}
            return return_metadata, return_data

    elif extension == 'json':
        print('Loading:', filepath)
        return None, json.load(open(filepath))

    elif extension == 'csv':
        return_data = {}
        lines_generator = open(filepath)
        return_metadata = json.loads(next(lines_generator))
        print('Loading file:', filepath)
        column_headers = next(lines_generator).strip().split('\t')
        data_types = None
        for key in COUNT_FIELDS:
            if key in return_metadata:
                total = return_metadata[key]
                break
        else:
            total = None
        for line in tqdm(lines_generator, total=total, file=sys.stdout):
            line = line.split('\t')
            info = {}
            if not data_types:
                data_types = [
                    str if v == ''
                    else type(eval(v) if not v.replace(' ', '').isalpha() else v)
                    for v in line
                ]
            for key, data_type, value in zip(column_headers, data_types, line):
                value = value.strip()
                info[key] = data_type(value) if not value == '' else value
            key = determine_key(info)
            return_data[info[key]] = info
        return return_metadata, return_data

    elif extension == 'txt':
        pass


PRIORITIZED_KEYS = ['_id', 'key', 'conceptKey', 'conservativeKey']


def determine_key(info: dict):
    for key in PRIORITIZED_KEYS:
        if key in info:
            return key


if __name__ == '__main__':
    path = get_file_path_choice()
    if type(path) == list:
        data = [load_file(p) for p in path]
    else:
        metadata, data = load_file(path)



# for looking at concepts that are filtered out from initial to collapsed aggregation
# collapsed, collapse_keys = data
# missed = []
# for key, info in load_file('data/projectmuse-documents-v1-concept-aggregations.jsonl', as_generator=True)[1]:
#     if collapse_keys[1][key]['collapsedKey'] not in collapsed[1]:
#         missed.append(info['display'])


