def find_all_entries_between(text, p, q, required_char=None):
    entries = []
    entry = ''
    found = False
    for ch in text:
        if ch == p:
            found = True
            entry += ch
        elif ch == q:
            entry += ch
            if not required_char:
                entries.append(entry.replace('{}{}'.format(p, p), p).replace('{}{}'.format(q, q), q))
            else:
                if required_char in entry:
                    entries.append(entry.replace('{}{}'.format(p, p), p).replace('{}{}'.format(q, q), q))
            entry = ''
            found = False
        if found:
            entry += ch
    return entries
