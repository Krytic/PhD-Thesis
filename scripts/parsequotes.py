import re

quotes = {
    'openingquote': '',
    'closingquote': ''
}

cleanups = {
    '\\\\': '\n',
    r'\vspace': '\n\\vspace',
    '%': '',
    r'\hrule': '<hr />',
    r'\vspace{30pt}': '',
    r'\vspace{10pt}': '',
    '``': '"',
    "''": '"',
    '\n': '<br />',
    r'\pgfornament[width=0.3\textwidth]{89}': '&sim;&nbsp;&middot;&nbsp;&sim;',
    '<hr /><br />': '<hr />'
}

with open('dedications.tex') as f:
    while line := f.readline():
        line = line.strip()
        if line.startswith('%'):
            continue  # comment
        for key in quotes.keys():
            if line.startswith('\\' + key):
                quotes[key] = line.strip()
                if line.endswith('\\\\'):
                    while (line2 := f.readline()):
                        quotes[key] += line2.strip()
                        if quotes[key].endswith('}'):
                            break

for key, quote in quotes.items():
    # quote = (quote.replace('\\\\', '\n')
    #               .replace(r'\vspace', '\n\\vspace')
    #               .replace('%', '')
    #               .replace(r'\hrule', '<hr />')
    #               .replace(r'\vspace{30pt}', '')
    #               .replace(r'\vspace{10pt}', '')
    #               .replace('``', '"')
    #               .replace("''", '"')
    #               .replace('\n','<br />')
    #               .replace(r'\pgfornament[width=0.3\textwidth]{89}','&sim;&nbsp;&cdot;&nbsp;&sim;')
    #               .replace('<hr /><br />', '<hr />'))

    for cleankey, cleanval in cleanups.items():
        quote = quote.replace(cleankey, cleanval)

    x = re.findall(r"\\textsc\{[a-zA-Z\-,.! ]*\}", quote)

    for match in x:
        name = match[len('\\textsc{'):-1]
        quote = quote.replace(match, f'<span class="small-caps">{name}</span>')
        y = re.findall(r"\\phantom\{[ *]\}", quote)
        for match_y in y:
            quote = quote.replace(match_y, '<br />')

    z = re.findall(r"\\textit\{[a-zA-Z\-,. ]*\}", quote)

    for match in z:
        name = match[len('\\textit{'):-1]
        quote = quote.replace(match, f'<span class="italic">{name}</span>')

    quote = "<div>" + quote[1+len(key)+1:]
    quote = quote.replace('}{', '</div><br /><div class="is-pulled-right">&mdash; ')
    quote = quote[:-1] + "</div>"

    quotes[key] = quote

with open('quotes.html', 'w') as f:
    contents = f"""
<div class='column is-6'>
<h1>Opening Quote</h1>
{quotes['openingquote']}
</div>
<div class='column is-6'>
<h1>Closing Quote</h1>
{quotes['closingquote']}
</div>
"""
    f.writelines(contents)