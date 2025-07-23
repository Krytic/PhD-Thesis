import os

chaps = []

BEGIN_AIM_TOKEN = r'% !aim:'
BEGIN_STRUCTURE = r'% begin structure'
END_STRUCTURE = r'% end structure'

for file in os.listdir('chapters'):
    if file.endswith('.tex'):
        chaps.append(f"chapters/{file}")

for file in os.listdir('chapters/appendices'):
    if file.endswith('.tex'):
        chaps.append(f"chapters/appendices/{file}")

chaps.sort(key=lambda row: row[-5])

aims = [r"\begin{enumerate}" + '\n']

for chap in chaps:
    with open(chap, 'r') as f:
        aim = None
        label = None

        for line in f.readlines()[:4]:
            if line.startswith(BEGIN_AIM_TOKEN):
                aim = line[len(BEGIN_AIM_TOKEN):].strip()

            if line.startswith(r'\chapter'):
                loc = line.find(r"\label")
                label = line[loc+7:-2]

        if aim is not None and label is not None:
            aims.append(fr"    \item In \Cref{{{label}}}, {aim}" + "\n")

aims.append(r"\end{enumerate}" + '\n')

begin = None
end = None
with open('chapters/chapter01.tex', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.strip() == BEGIN_STRUCTURE:
            begin = i
        if line.strip() == END_STRUCTURE:
            end = i
            break

if begin is None or end is None:
    print("Could not find the pasting location!")
else:
    before = lines[:begin+1]
    after = lines[end:]

    with open('chapters/chapter01.tex', 'w') as f:
        for line in before:
            f.write(line)
        for line in aims:
            f.write(line)
        for line in after:
            f.write(line)
