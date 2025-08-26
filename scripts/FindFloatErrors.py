import os
import re
from collections import Counter
from operator import itemgetter
import bibtexparser
import tabulate

print("SCRIPT DOES NOT WORK.")

fnames = []

for file in os.listdir('chapters/'):
    if not os.path.isdir(file) and file.endswith('.tex'):
        fnames.append(f'chapters/{file}')

for file in os.listdir('chapters/appendices'):
    if not os.path.isdir(file) and file.endswith('.tex'):
        fnames.append(f'chapters/appendices/{file}')

files = dict()


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def discover_tokens(file_contents, token):
    items = []

    for idx, line in enumerate(contents):
        capturing = False

        if token in line:
            occs = [m.start() for m in re.finditer(f'\\{token}', line)]

            for occ in occs:
                keys = ''

                for i in range(0, 500):
                    if line[occ+i] == '{':
                        capturing = True

                    if capturing:
                        keys += line[occ+i]

                    if line[occ+i] == '}':
                        capturing = False
                        break

                items.extend([k.strip() for k in keys[1:-1].split(',')])

    return items


for file in sorted(fnames):
    new_contents = []

    with open(file, 'r') as f:
        contents = f.readlines()

    files[file] = {'reference_order': [], 'defined_order': []}

    key_items = discover_tokens(contents, r'\Cref')

    for item in key_items:
        if item.startswith('chap:'):
            files[file]['reference_order'].append(item)

    label_items = discover_tokens(contents, r'\label')

    for item in label_items:
        if item.startswith('chap:'):
            files[file]['defined_order'].append(item)

for file, lookups in files.items():
    print(f"===== {file} =====")
    reference_order = f7(lookups['reference_order'])
    definitio_order = lookups['defined_order']

    for i in range(len(reference_order)):
        print(reference_order[i], definitio_order[i])