import pikepdf

from pikepdf import Pdf

pdf = Pdf.open('PhD_Thesis.pdf')

found_pages = [(0, 'Title')]
j_indexes = []

with open('main.chaps', 'r') as file:
    for line in file.readlines():
        line = line.strip()
        parts = line.split(',')

        text = parts[0].strip()
        current_page = int(parts[1].strip())-1

        title = text.lower()

        if title.startswith('chapter') or title.startswith('appendix'):
            j_indexes.append(current_page)

        if title.startswith('bibliography'):
            text = 'Bibliography'

        if title.startswith('contents'):
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

# extract pages j to k
print("Extracting the chapter cover pages")

dst = Pdf.new()
for j in j_indexes:
    page = pdf.pages[j]
    dst.pages.append(page)

dst.save(f'rendered_chapters/chapter-cover-pages.pdf')


pdf.close()
