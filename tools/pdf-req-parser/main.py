from PyPDF2 import PdfFileReader
import simplejson


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


DOCS_DIRECTORY = 'docs'
INPUT_LIST_FILE = 'input.json'
OUTPUT_DIRECTORY = 'output'

input_list = {}
with open('{}/{}'.format(DOCS_DIRECTORY, INPUT_LIST_FILE), 'rb') as input_file:
    input_list = simplejson.load(input_file)

requirements = {}
for input_entry in input_list:
    file_path = '{}/{}'.format(DOCS_DIRECTORY, input_entry['filename'])
    print('Processing new file: {}'.format(file_path))
    with open(file_path, 'rb') as f:
        requirements[input_entry['filename']] = {}  # new key in requirements list
        pdf = PdfFileReader(f)
        entries = []
        for page_num in range(input_entry['first_page'] - 1, input_entry['last_page']):
            print('\tPage {}/{}'.format(page_num + 1, input_entry['last_page']))
            page = pdf.getPage(page_num)
            text = page.extractText().replace('\n', '')
            entries.extend(find_all_entries_between(text, '[', ']', required_char='_'))

        # only for SWS files
        current_rs = None
        for entry in entries:
            if 'RS' in entry:
                current_rs = entry
                requirements[input_entry['filename']][current_rs] = {}
            elif 'SWS' in entry:
                requirements[input_entry['filename']][current_rs][entry] = { 'more_data': 'soon' }

with open('{}/requirements.json'.format(OUTPUT_DIRECTORY), 'w+') as json_file:
    json_file.write(simplejson.dumps(requirements, indent=4))
