import json
import glob
import os
import gzip
from tqdm import tqdm
import sys
import inspectutils


def get_file_path_choice():
    data_files = glob.glob('./data/*')
    for i, path in enumerate(data_files):
        print(i, ':', os.path.basename(path))
    choice = int(input('Choose a number from the list above: '))
    return data_files[choice]


def load_file(filepath: str):
    extension = os.path.basename(filepath).split('.')[1]
    if extension == 'jsonl':
        data = {}
        lines_generator = open(filepath)
        metadata = next(lines_generator)  # which does not contain an n-gram
        print('Reading file ...')
        lines = [line for line in lines_generator]
        key = None
        for line in tqdm(lines, desc='Loading data', file=sys.stdout):
            info = json.loads(line)
            if not key:
                key = determine_key(info)
            data[info[key]] = info
        return metadata, data

    elif extension == 'json':
        print('Loading data ...')
        return None, json.load(open(filepath))


PRIORITIZED_KEYS = ['_id', 'conceptKey']


def determine_key(info: dict):
    for key in PRIORITIZED_KEYS:
        if key in info:
            return key


path = get_file_path_choice()
metadata, data = load_file(path)





