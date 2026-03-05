import re

with open('sources.bib', 'r') as f:
    content = f.read()

# remove {"error": ...} lines
content = re.sub(r'\{"error".*?\n', '', content)

# split by @
entries = content.split('@')
unique_entries = []
seen_keys = set()

for entry in entries:
    if not entry.strip(): continue
    # extract key
    m = re.match(r'^[a-zA-Z]+{([^,]+)', entry)
    if m:
        key = m.group(1)
        if key not in seen_keys:
            seen_keys.add(key)
            unique_entries.append('@' + entry)
    else:
        unique_entries.append('@' + entry)

with open('sources.bib', 'w') as f:
    f.write('\n'.join(unique_entries))

print("Fixed sources.bib")
