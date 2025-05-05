import os
import re
from collections import Counter
from operator import itemgetter
import bibtexparser
import tabulate

tokens = dict()


def find_key(dictionary, key):
    return list(dictionary.keys())[list(dictionary.values()).index(key)]


bibfile = []

with open('thesis.bib', 'r') as f:
    for line in f.readlines():
        if line.startswith('@') and line.strip().endswith(','):
            token = line.strip().split('{')[-1][:-1]

            if ':' in token:
                tokens[token] = token  # done already
            else:
                # handle
                if '_' in token:
                    parts = token.rsplit('_', maxsplit=2)

                    first_author = parts[0][0].upper()+parts[0][1:]
                    year = parts[2]

                    new_token = first_author+":"+year

                    if new_token in tokens.values():
                        # we need a letter delimiter
                        other_token = find_key(tokens, new_token)
                        print(f"Collision on {new_token} ({token} with {other_token})")

                        trial_token = new_token

                        i = 0

                        while trial_token in tokens.values():
                            trial_token = new_token + chr(97+i)

                            i += 1

                            if i > 26:
                                raise ValueError("Unresolvable collision on {token}")

                        new_token = trial_token

                    tokens[token] = new_token

                    line = line.replace(token, new_token)

        bibfile.append(line)

with open('thesis.bib', 'w') as f:
    f.seek(0)
    f.writelines(bibfile)

# with open('')

fnames = []

for file in os.listdir('chapters/'):
    if not os.path.isdir(file) and file.endswith('.tex'):
        fnames.append(f'chapters/{file}')

for file in os.listdir('chapters/appendices'):
    if not os.path.isdir(file) and file.endswith('.tex'):
        fnames.append(f'chapters/appendices/{file}')


def sort_key(item):
    year = int(re.sub('[^0-9]', '', item.split(':')[1]))
    first_author = item[0].lower()
    return (year, first_author)


intext_citations = []

for file in fnames:
    new_contents = []

    with open(file, 'r') as f:
        contents = f.readlines()

    for line in contents:
        for key, value in tokens.items():
            line = line.replace(key, value)
        new_contents.append(line)

    for idx, line in enumerate(new_contents):
        capturing = False

        if r'\cite' in line:
            occs = [m.start() for m in re.finditer(r'\\cite', line)]

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

                key_items = [k.strip() for k in keys[1:-1].split(',')]

                intext_citations.extend(key_items)

                if len(key_items) == 1:
                    continue

                sorted_items = sorted(key_items, key=sort_key)
                new_part = ", ".join(sorted_items)
                line = line.replace(keys[1:-1], new_part)

                new_contents[idx] = line

    with open(file, 'w') as f:
        f.seek(0)
        f.writelines(new_contents)

unused_tokens = list(set(tokens.values()) - set(intext_citations))

library = bibtexparser.parse_file("thesis.bib")

key_name_pairs = dict()

for entry in library.entries:
    key = entry.key

    try:
        name = entry.fields_dict['title'].value
        name = name.replace('{', '').replace('}', '').lower().strip()

        if name == name.upper():
            name = name[0].upper() + name[1:]
    except KeyError:
        continue

    key_name_pairs[key] = name

with open('stats.log', 'w') as f:
    f.seek(0)
    f.write(f"{len(unused_tokens)} unused items in bibfile ({len(unused_tokens)/len(tokens)*100:.1f}% of file):\n")

    table = []

    for tok in sorted(unused_tokens):
        table.append([tok, key_name_pairs[tok]])

    f.writelines(tabulate.tabulate(table, tablefmt='fancy_outline', headers=['Citation Key', 'Work Name']))
    f.write('\n\n')

    cnts = Counter(intext_citations)
    key = find_key(cnts, max(cnts.values()))

    top5 = dict(sorted(cnts.items(), key=itemgetter(1), reverse=True)[:5])

    f.write(f"Most cited:\n")
    f.write(f"    {key} ({cnts[key]} times)\n\n")

    f.write("Top 5:\n")
    for k, v in top5.items():
        f.write(f"    {k} ({v} times)\n")