import os
import glob
from collections import namedtuple


def get_logs():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    logs = glob.glob(os.path.join(base_dir, 'logs', '*.log'))
    return logs


def get_key(row):
    key = row.split('KEY_')[-1].split(')')[0]
    if 'SHIFT' in key:  # to get rid of 'LEFT' and 'RIGHT'
        key = 'SHIFT'
    return key


def get_presses(file):
    presses = []
    press = namedtuple('press', ['key', 'ind'])
    with open(file, 'r') as f:
        for ind, row in enumerate(f):
            if 'KEY' in row and 'down' in row:
                key = get_key(row)
                presses.append(press(key, ind))
    return presses


def compare2list(presses, txtlist):
    sequences = []
    seq = []
    for press in presses:
        if press.key == txtlist[len(seq)]:
            seq.append(press.ind)
            if len(seq) == len(txtlist):
                sequences.extend([ind for ind in range(min(seq), max(seq) + 2)]) # adding one to catch the up action
                seq = []
        else:
            seq = []
    return sequences


def mod_logs(sequences, source):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    name = os.path.split(source)[-1] + '.mod'
    outfile = os.path.join(base_dir, 'censored-logs') + os.sep + name
    with open(source, 'r') as fin:
        with open(outfile, 'w') as fout:
            for ind, row in enumerate(fin):
                if ind not in sequences:
                    fout.write(row)



def main(txtlist=[]):
    files = get_logs()
    for file in files:
        print("Checking file {}".format(file))
        presses = get_presses(file)
        sequences = compare2list(presses, txtlist)
        mod_logs(sequences, file)


if __name__ == "__main__":
    # p4sSw0rd
    main(txtlist=['P', '4', 'S', 'SHIFT', 'S', 'W', '0', 'R', 'D'])