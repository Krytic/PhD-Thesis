import terminus

codes = []
alphabet = [chr(97+i).upper() for i in range(26)]
JUST_TRY_IT_ALL = False


def get_version_of_package(package):
    if package.lower() != 'python':
        out, err, reason = terminus.execute('pip list')

        lines = out.split('\n')
        bits = lines[1].split(' ')
        len1, len2, len3 = len(bits[0]), len(bits[1]), len(bits[2])

        for line in lines[2:]:
            pkgname = line[:len1].strip()
            version = line[len1:len1+len2+1].strip()

            if package.lower() == pkgname.lower():
                return version
    else:
        out, err, reason = terminus.execute('python --version')
        out = out.strip().split()
        return out[1]


def envision():
    out, err, reason = terminus.execute('pip list')

    lines = out.split('\n')
    bits = lines[1].split(' ')
    len1, len2, len3 = len(bits[0]), len(bits[1]), len(bits[2])

    table = []  # ['Package', 'Version', 'Editable Location']]

    for line in lines[2:]:
        package = line[:len1].strip()
        version = line[len1:len1+len2+1].strip()
        install_loc = line[len1+len2+1:].strip()

        table.append((package, version))

    return table


fname = None
for letter in alphabet:
    with open(f'chapters/appendices/appendix{letter}.tex', 'r') as f:
        lines = f.readlines()
        for lineno, line in enumerate(lines):
            if lineno >= 4: break
            if line.strip() == '% !versioning-file':
                fname = f'chapters/appendices/appendix{letter}.tex'
                break
    if fname is not None:
        break

if fname is None:
    raise ValueError("Could not find the file to order.")

names = []

with open(fname, 'r') as f:
    for line in f.readlines():
        if line.strip().startswith(r'\codename'):
            line = line.strip().split("&")

            codename = line[0][len(r'\codename{'):].strip()[:-1]

            version = line[1].strip()
            if version == '':
                inferred_version = get_version_of_package(codename)
                if inferred_version is not None:
                    print(f'No version listed for {codename}, setting to v{inferred_version}')
                else:
                    print(f'No version listed for {codename} and a version could not be inferred. Ignoring.')

                    inferred_version = ''

                version = inferred_version

            citation = line[2].rstrip(r'\\').strip()

            codes.append([codename, version, citation])
            names.append(codename)

if JUST_TRY_IT_ALL:
    all_packages = envision()

    for (code, version) in all_packages:
        if code not in names:
            codes.append([code, version, '-'])

codes.sort(key=lambda x: x[0])
clean_latex = []

max_sizes = [0 for _ in range(len(codes[0]))]

for code in codes:
    code[0] = fr"\codename{{{code[0]}}}"
    for i in range(len(code)):
        max_sizes[i] = max(max_sizes[i], len(code[i]))

for code in codes:
    for i in range(len(code)):
        if i == 0:

            code[i] = code[i].rjust(max_sizes[i], ' ')
        else:
            code[i] = code[i].ljust(max_sizes[i], ' ')

    clean_latex.append(" & ".join(code) + " \\\\")

with open(fname, 'r+') as f:
    replacing = False
    next_one = False

    j = 0
    contents = f.readlines()

    for i, line in enumerate(contents):
        line = line.rstrip('\n').lstrip('\n')

        if line.strip().endswith("%!begin-replace"):
            replacing = True
            next_one = True

        if line.strip().endswith("%!end-replace"):
            replacing = False

        if j >= len(clean_latex):
            # we provided too much space
            replacing = False
            next_one = False

        if line.strip().endswith('%!match-indent'):
            indent_level = len(line) - len(line.lstrip(' '))

        if replacing:
            if not next_one:
                # indent_level = len(line) - len(line.lstrip(' '))
                newline = " " * indent_level + clean_latex[j]
                line = newline
                j += 1
            else:
                next_one = False
        contents[i] = line

    f.seek(0)
    f.write("\n".join(contents))
    f.truncate()