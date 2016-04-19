import glob
import json
import os
from collections import namedtuple

import sys


def get_logs(folder):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    logs = glob.glob(os.path.join(base_dir, folder, '*.log*'))
    if len(logs) == 0:
        print("Could not find any files. Please check the name of the folder.")
    return logs


def get_keys(file):
    print("Running over {}".format(file))
    keys = []
    keytuple = namedtuple('keytuple', ['time', 'key', 'direction'])
    with open(file, 'r') as f:
        for row in f:
            splitted = row.split()
            keys.append(keytuple(splitted[3].rstrip(','), splitted[4], splitted[-1]))
    return keys


def main(folder):
    data = []
    files = get_logs(folder)
    for file in files:
        data.extend(get_keys(file))
        data.extend(('EOF', 'EOF', 'EOF'))
    print("Collected {} samples".format(len(data)))
    return data


def save2file(data):
    data_json = 'key_data.json'
    with open(data_json, 'w') as f:
        json.dump(data, f)
    print('Saving data to {}'. format(data_json))

if __name__ == "__main__":
    folder = sys.argv[1]
    data = main(folder)
    save2file(data)