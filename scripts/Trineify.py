import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-ow', nargs='?', default='n', type=str)
parser.add_argument('-tgt', nargs='?', default=25, type=int)
args = parser.parse_args()

if args.ow in 'yn':
    overwrite = {'y': True, 'n': False}[args.ow]
else:
    raise ValueError(f'-ow must be y or n, not {args.ow}')

for filename in os.listdir('chapters'):
    if os.path.isdir(f'chapters/{filename}'):
        continue
    if not filename.startswith('chapter'):
        continue

    with open(f'chapters/{filename}', 'r') as f:

        found = False

        lines = f.readlines()

        for lineno, raw_line in enumerate(lines):
            line = raw_line.strip()

            if line.startswith('%'):
                continue  # comment
            elif line == '':
                continue  # blank
            elif line.startswith('\\'):
                if line.startswith('\\lettrine'):
                    break  # this chapter already has a drop cap
                else:
                    continue
            else:
                # this is the first content line, that doesn't have a drop cap.
                firstchar = line[0]
                first_word = line.split(" ")[0][1:]
                line_split = line.split()
                rest_of_line = " ".join(line.split(" ")[1:])

                i = 0
                j = 0

                for letter in line:
                    if letter == ' ':
                        j += 1

                        continue

                    i += 1

                    if i > args.tgt:
                        break

                length_up_to_target = sum(map(len, line_split[:j]))
                length_including_target = sum(map(len, line_split[:j+1]))
                targets = [length_including_target, length_up_to_target]

                target = min(targets, key=lambda x: abs(x-args.tgt))

                if target < args.tgt:
                    do = "shorten"
                else:
                    do = "lengthen"

                word = line_split[j]

                print(f"Now examining: {filename}")
                print(f"    > Letter {i} occurs in word {j} ({word}).)")
                print(f"    > Length up to: {length_up_to_target}")
                print(f"    > Length including: {length_including_target}")
                print(f"    > Choice: {do}")

                if do == 'lengthen':
                    k = j+1
                else:
                    k = j

                preamble = ' '.join(line_split[:k])[1:]
                mantissa = ' '.join(line_split[k:])

                new_line = f'\\lettrine[lines=3]{{{firstchar}}}{{{preamble}}} {mantissa}\n'


                # new_line = f'\\lettrine[lines=3]{{{firstchar}}}{{{first_word}}} {rest_of_line}\n'
                found = True
                break

    if found:
        print(new_line)

        if overwrite:
            lines[lineno] = new_line
            with open(f'chapters/{filename}', 'w') as f:
                f.seek(0)
                f.writelines(lines)