import json
from collections import OrderedDict

file_data = OrderedDict()

file_data['name'] = 'strawberry data'
file_data['house'] = 1
file_data['line'] = 1
file_data['direction'] = 1
file_data['location'] = 4

with open('data.json', 'w', encoding='utf-8') as make_file:
    json.dump(file_data, make_file, ensure_ascii=False, indent='\t')

