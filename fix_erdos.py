with open('sources.bib', 'r') as f:
    content = f.read()

content = content.replace('Erd\\H{o}s', 'Erd{\\"o}s')

with open('sources.bib', 'w') as f:
    f.write(content)
