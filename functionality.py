import json
from os import path
import pathlib
import zipfile
from shutil import rmtree

def fetch_lang_from_jar(path_to_file,lang_file):
    with zipfile.ZipFile(path_to_file) as jar:
        for file in jar.infolist():
            if file.filename.endswith(lang_file):
                extract_path = pathlib.Path(__file__).parent / 'temp'
                jar.extract(file.filename,extract_path)
                return extract_path / file.filename


def parse_lang_file(path_to_file):
    try:
        with open(path_to_file, mode='r', encoding='utf-8') as f:
            data = f.read()
        return json.loads(data)
    except json.decoder.JSONDecodeError as e:
        print('Error while parsing JSON file! ',e)
    except FileNotFoundError as e:
        print('Could not open lang file! ', e)
        

def update_lang_file(path_to_en_us:pathlib.WindowsPath, path_to_translated:pathlib.WindowsPath,path_to_output:pathlib.WindowsPath, SortOutput:bool=False, delete_temp:bool = True):
    if (not isinstance(path_to_en_us, pathlib.WindowsPath)) or (not isinstance(path_to_translated, pathlib.WindowsPath)) or (not isinstance(path_to_output, pathlib.WindowsPath)):
        raise TypeError
    # Read data into JSON objects
    if path_to_en_us.suffix == '.jar':
        path_to_en_us = fetch_lang_from_jar(path_to_en_us, 'en_us.json')

    if path_to_translated.suffix == '.jar':
        path_to_translated = fetch_lang_from_jar(path_to_translated, 'ru_ru.json')

    en_us_json = parse_lang_file(path_to_en_us)
    translated_json = parse_lang_file(path_to_translated)

    assert (en_us_json != None and translated_json != None) , 'Could not get data from lang files'
    if delete_temp:
        rmtree(pathlib.Path(__file__).parent / 'temp')
    
    #Initialize new JSON which will be outputted
    new_json = json.loads('{}')

    #Fill the output JSON
    if not SortOutput:
        for key in en_us_json.keys():
            new_json[key] = translated_json.get(key, en_us_json[key]) # Translated_json[key], or if NaN then en_us_json[key]
    if SortOutput:
        for key in sorted(en_us_json):
            new_json[key] = translated_json.get(key, en_us_json[key]) # Translated_json[key], or if NaN then en_us_json[key]


    #Re-iterate to find out untranslated lines. Could implement while filling the output JSON, but it turned out very messy and unreadable, so it's separate iteration
    line = 2
    untranslated_lines = {}
    for key in new_json.keys():
        if new_json[key] == en_us_json[key] or new_json[key] == '':
            untranslated_lines[line] = new_json[key]
        line += 1


    #Output
    with open(path_to_output, mode='w', encoding='utf-8') as f:
        output_string = json.dumps(new_json, ensure_ascii=False, indent=2)
        f.write(output_string)

        if len(untranslated_lines) > 0:
            print(f'There are a total of {len(untranslated_lines)} keys not translated! Specifically:')
            for line in untranslated_lines.keys():
                print(f'line {line}, "{untranslated_lines[line]}"')
    return untranslated_lines


if __name__=='__main__':
    #Butchery custom translation as an example
    folder = pathlib.Path(__file__).parent/'testdata'
    jar = folder / 'butcher-2.4.7.jar'
    en_us = folder / 'en_us.json'
    ru_ru = folder / 'ru_ru.json'
    output = folder / 'ru_ru_output.json'
    print(type(en_us))
    update_lang_file(jar,ru_ru,output,True,False)
    # print(fetch_lang_from_jar(jar))