import os

if os.path.exists('main.todos') and not os.path.exists('TODOLIST'):
    with open('main.todos', 'r') as f:
        lines = f.readlines()

    new_lines = []

    for i, line in enumerate(lines):
        line = line[len(r'\gdef \@todo{'):-2]
        line = line.replace(r'\%', '%') + "\n"
        new_lines.append(line)

    with open('../TODOLIST', 'w') as f:
        f.seek(0)
        f.writelines(new_lines)