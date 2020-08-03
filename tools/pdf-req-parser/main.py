from helpers import *
from PyPDF2 import PdfFileReader
import simplejson
import sys
import os


if len(sys.argv) < 2:
    print('Wrong args. Should be: <INPUT_DIRECTORY>')
    sys.exit(-1)

INPUT_DIRECTORY = sys.argv[1]
INPUT_LIST_FILE = '{}/input.json'.format(INPUT_DIRECTORY)
OUTPUT_FILE = '{}/output.json'.format(INPUT_DIRECTORY)

if not os.path.isfile(INPUT_LIST_FILE):
    print('{} file does not exist.'.format(INPUT_LIST_FILE))
    sys.exit(-2)

input_list = {}
with open('{}'.format(INPUT_LIST_FILE), 'rb') as input_file:
    input_list = simplejson.load(input_file)

requirements = {}
# Stage 1
# Processing of the table which is described in input.json file.
for input_entry in input_list:
    file_path = '{}/{}'.format(INPUT_DIRECTORY, input_entry['filename'])
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

        # only for SWS files (temporary)
        # todo: implement other types (_RS_, _TPS_)
        current_rs = None
        for entry in entries:
            if 'RS' in entry:
                current_rs = entry
                requirements[input_entry['filename']][current_rs] = {}
            elif 'SWS' in entry:
                requirements[input_entry['filename']][current_rs][entry] = { 'more_data': 'soon' }

with open(OUTPUT_FILE, 'w+') as json_file:
    json_file.write(simplejson.dumps(requirements, indent=4))
