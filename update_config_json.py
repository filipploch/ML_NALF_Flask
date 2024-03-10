import os
current_folder = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')

with open('config.json', 'r', encoding='utf-8') as json_file:
    file_content = json_file.read()
file_content = file_content.replace('path-to-project', current_folder)

with open('ML_NALF_Flask.json', 'w', encoding='utf-8') as json_file:
    json_file.write(file_content)