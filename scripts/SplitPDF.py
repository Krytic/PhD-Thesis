import pikepdf

from pikepdf import Pdf

pdf = Pdf.open('PhD_Thesis.pdf')

found_pages = [(0, 'Title')]

with open('main.chaps', 'r') as file:
    for line in file.readlines():
        line = line.strip()
        parts = line.split(',')

        text = parts[0].strip()
        current_page = int(parts[1].strip())-1

        if text.lower().startswith('bibliography'):
            text = 'Bibliography'

        if text.lower().startswith('contents'):
            text = 'Contents'

        print(f'Found {text} on page {current_page}')

        found_pages.append((current_page, text))

for i, match in enumerate(found_pages):
    if i == len(found_pages) - 1:
        j = found_pages[i][0]
        k = None
    else:
        j = found_pages[i][0]
        k = found_pages[i+1][0]

    if match[1].lower() == 'table-of-contents':
        k = j + 3
        # manual override, TOC is 3 pages.

    # extract pages j to k
    dst = Pdf.new()
    for page in pdf.pages[j:k]:
        dst.pages.append(page)
    dst.save(f'rendered_chapters/{match[1]}.pdf')

pdf.close()
