import markdown
import re

with open('wc.txt', 'r') as f:
    contents = f.readlines()
    wc = int(contents[-1].strip().split(',')[1])
    if wc < 500:
        contents = contents[:-1]

    new_contents = []

    for i, line in enumerate(contents):
        current_wc = int(line.strip().split(',')[1])
        previous_wc = int(contents[i-1].strip().split(',')[1])

        if i == 0:
            new_contents.append(line)
        if i >= 1:
            if current_wc < 0.9 * previous_wc:
                # This is probably a compilation error.
                continue
            elif current_wc == previous_wc:
                # nothing changed
                continue
            else:
                new_contents.append(line)


with open('wc.txt', 'w') as f:
    f.writelines(new_contents)

with open('main.toc', 'r') as f:
    sections = []
    while line := f.readline():
        if line.strip() == '': continue
        if line.strip().startswith(r"\babel"):
            # language directive (I'm extra and have a passage in ancient greek)
            # we wish to ignore this.
            continue

        startpoint = len(r"\contentsline ")
        parts = line.strip()[startpoint:].split("}{", 1)
        parts = [part.strip("{}") for part in parts]

        level = parts[0]
        heading = parts[1]

        if heading.startswith(r"\numberline"):
            heading = heading.split("}", 1)[1]

        heading = heading.rsplit("}{", 2)[0]

        if heading.startswith("Bibliography"):
            heading = 'Bibliography' # weird formatting.
        if heading.startswith("Table of Contents"):
            heading = 'Table of Contents' # weird formatting.

        heading = (heading.replace(" {", "{")
                          .replace(r'\&', '&')
                          .replace(' $', '$')
                          .replace(':$', ': $')
                          .replace(' }', '}')
                          .replace('The$', 'The $'))

        x = re.findall(r"\SI\{[0-9]*\.*[0-9]*\}\{\\msun\}", heading)

        for match in x:
            dissection = match[3:-1].split('}{')
            mantissa = dissection[0]
            load = dissection[1]

            if load.strip().lower() == r'\msun':
                load = r'M_\odot'

            heading = heading.replace(f'\\{match}', f'{mantissa}{load}')

        y = re.findall(r"\\textsc\{[a-zA-Z]*\}", heading)

        for match in y:
            name = match[len('\\textsc{'):-1]
            heading = heading.replace(match, f'<span class="small-caps">{name}</span>')

        sections.append((level, heading))

def get_depth(header):
    return {
    'chapter': 1,
    'section': 2,
    'subsection': 3,
    'subsubsection': 4
    }[header]

TOC = ""

for item in sections:
    depth = get_depth(item[0])

    spaces = (depth - 1) * 4

    TOC += f"{' ' * spaces}* {item[1]}\n"

TOC = markdown.markdown(TOC.strip())
# TOC = TOC.replace('<ul>', '<ol>').replace('</ul>', '</ol>')

with open('TOC.html', 'w') as f:
    f.write(TOC)
