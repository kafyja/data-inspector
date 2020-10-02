import json
import glob
import os
import gzip
from tqdm import tqdm
import sys
from inspectutils import *


def get_file_path_choice():
    data_files = glob.glob('./data/*')
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


def load_file(filepath: str):
    extension = os.path.basename(filepath).split('.')[1]
    if extension == 'jsonl':
        data = {}
        lines_generator = open(filepath)
        metadata = next(lines_generator)  # which does not contain an n-gram
        print('Loading file:', filepath)
        lines = [line for line in lines_generator]
        key = None
        for line in tqdm(lines, file=sys.stdout):
            info = json.loads(line)
            if not key:
                key = determine_key(info)
            data[info[key]] = info
        return metadata, data

    elif extension == 'json':
        print('Loading:', filepath)
        return None, json.load(open(filepath))


PRIORITIZED_KEYS = ['_id', 'conceptKey']


def determine_key(info: dict):
    for key in PRIORITIZED_KEYS:
        if key in info:
            return key


path = get_file_path_choice()
if type(path) == list:
    data = [load_file(p) for p in path]
else:
    metadata, data = load_file(path)





