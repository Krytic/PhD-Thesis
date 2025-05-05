import os

BEGIN_TOKEN = '%! begin transclude'
END_TOKEN = '%! end transclude'


class verbs:
    COPY = 'copy'
    PASTE = 'paste'


orders = dict()

name = None

for file in os.listdir('chapters/'):
    copying = False

    if file.endswith('.tex'):
        new_lines = []

        with open(f"chapters/{file}") as f:
            pasting = False

            for line in f.readlines():
                cline = line.strip()

                if cline.startswith(END_TOKEN):
                    copying = False
                    pasting = False

                if copying:
                    orders[name].append(line.rstrip())

                if cline.startswith(BEGIN_TOKEN):
                    order = cline[len(BEGIN_TOKEN):].strip().split()
                    name = order[1]

                    match order[0]:
                        case verbs.COPY:
                            copying = True
                            orders[name] = []
                        case verbs.PASTE:
                            print(f'Pasting of transclusion "{name}" ordered in {file}')
                            new_lines.append(line)
                            pasting = True

                            for transcluded_line in orders[name]:
                                new_lines.append(transcluded_line + '\n')

                if not pasting:
                    new_lines.append(line)

        with open(f'chapters/{file}', 'w') as f:
            f.seek(0)
            f.writelines(new_lines)