import bibtexparser
from tabulate import tabulate
from math import floor, ceil
import colorama
from colorama import Fore, Style, Back
colorama.init()

library = bibtexparser.parse_file("thesis.bib")

if len(library.failed_blocks) > 0:
    print("Some blocks failed to parse. Check the entries of `library.failed_blocks`.")
else:
    print("All blocks parsed successfully")

key_name_pairs = dict()
to_remove = ['abstract', 'file']
i = 0

for block in library.entries:
    for field in to_remove:
        try:
            value = block.pop(field)
            if value is None:
                raise ValueError(f"Block has no field \"{field}\".")
            i += 1
        except (KeyError, ValueError):
            continue

bibtexparser.write_file("clean_thesis.bib", library)