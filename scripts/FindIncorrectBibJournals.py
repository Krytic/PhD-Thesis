import bibtexparser
from tabulate import tabulate
from math import floor, ceil
import colorama
from colorama import Fore, Style, Back
colorama.init()

library = bibtexparser.parse_file("thesis.bib")

key_name_pairs = dict()

for entry in library.entries:
    key = entry.key
    try:
        name = entry.fields_dict['journal'].value
        name = name.replace('{', '').replace('}', '').lower().strip()
        if name == name.upper():
            name = name[0].upper() + name[1:]
    except KeyError:
        continue
    key_name_pairs[key] = name.replace(r'\&', '&')

scanning = False
lookups_from_tex = dict()
with open('commands.tex', 'r') as f:
    lines = f.readlines()

    for line in lines:
        if 'Standard journal abbreviations' in line:
            scanning = True

        if scanning:
            if line.strip().startswith('%'):
                continue
            if line.startswith('\\newcommand'):
                line = line[1:].split('\\', maxsplit=1)[1]
                line = line.split('{', maxsplit=1)
                key, val = line[0].strip(), line[1].strip()

                val, comment = val.split('%', maxsplit=1)
                val = val.strip()
                comment = comment.strip()

                lookups_from_tex[comment.lower()] = key

header = [r'\cite key', 'Journal (from TeX)', 'Journal shorthand suggestion']
results = []

num = 0

for k, v in key_name_pairs.items():
    if v[0] == "\\":
        continue
    else:
        v_temp = v
        if v.split()[0].lower() == 'the':
            v_temp = ' '.join(v.split()[1:])

        if v_temp.lower() in lookups_from_tex.keys():
            results.append([k,
                            f'{v[0].upper()}{v[1:]}',
                            '\\' + lookups_from_tex[v_temp.lower()]])
            # print(f"{k} ({v[0].upper()}{v[1:]}) -- did you mean {lookups_from_tex[v.lower()]}?")
        else:
            results.append([k, f'{v[0].upper()}{v[1:]}', ''])
            # print(f"{k} ({v[0].upper()}{v[1:]})")
        num += 1

table = tabulate(results, header, tablefmt='double_outline')

hdr = 'Non-TeXed bibliography file keys'


def make_header(hdr, blank_before=2):
    output = "\n" * blank_before
    row = table.split('\n')[0]
    second_row = table.split('\n')[1]
    last_row = table.split('\n')[-1]

    n = max(len(row), 79)
    dl = len(row[0] + row[1] * (n-2) + row[-1]) - 2 - len(hdr)

    if dl % 2 == 0:
        m = dl // 2
        p = dl // 2
    else:
        m = floor(dl / 2)
        p = ceil(dl / 2)

    output += f"{Fore.GREEN}{Style.BRIGHT}"

    output += f"{row[0]}{row[1] * (n-2)}{row[-1]}\n"
    output += f"{second_row[0]}{' ' * m}{hdr}{' ' * p}{second_row[-1]}\n"
    output += f"{last_row[0]}{last_row[1] * (n-2)}{last_row[-1]}\n"
    output += f"{Style.RESET_ALL}"
    output += f"\n"
    return output


print(make_header(hdr, blank_before=20))

if num > 0:
    print(table)
else:
    print("""
                                __ooooooooo__
                           oOOOOOOOOOOOOOOOOOOOOOo
                       oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
                    oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
                  oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
                oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
               oOOOOOOOOOOO*  *OOOOOOOOOOOOOO*  *OOOOOOOOOOOOo
              oOOOOOOOOOOO      OOOOOOOOOOOO      OOOOOOOOOOOOo
              oOOOOOOOOOOOOo  oOOOOOOOOOOOOOOo  oOOOOOOOOOOOOOo
             oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
             oOOOO     OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO     OOOOo
             oOOOOOO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO OOOOOOo
              *OOOOO  OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  OOOOO*
              *OOOOOO  *OOOOOOOOOOOOOOOOOOOOOOOOOOOOO*  OOOOOO*
               *OOOOOO  *OOOOOOOOOOOOOOOOOOOOOOOOOOO*  OOOOOO*
                *OOOOOOo  *OOOOOOOOOOOOOOOOOOOOOOO*  oOOOOOO*
                  *OOOOOOOo  *OOOOOOOOOOOOOOOOO*  oOOOOOOO*
                    *OOOOOOOOo  *OOOOOOOOOOO*  oOOOOOOOO*
                       *OOOOOOOOo           oOOOOOOOO*
                           *OOOOOOOOOOOOOOOOOOOOO*
                                ""ooooooooo""

╔═══════════════════════════════════════════════════════════════════════════╗
║                   All citation keys are TeXed! Nice job.                  ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")

print()