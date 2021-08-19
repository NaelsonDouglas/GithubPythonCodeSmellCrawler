from pylama.main import check_path, parse_options
from rich import print
import subprocess
import pandas as pd
import json
import os


my_redefined_options = {
    #'linters': ['pep257', 'pydocstyle', 'pycodestyle', 'pyflakes'],
    'linters': ['pycodestyle', 'pyflakes', 'mccabe'],
    #'sort': 'F,E,W,C,D,...',
    'skip': '*__init__.py,*/test/*.py, *.md, */.git/*',
    'async': True,
    'force': True
}

def error_to_dict(e):
    d = {
            'linter' : e.linter,
            'col' : e.col,
            'lnum' : e.lnum,
            'type' : e.type,
            'text' : e.text,
            'filename' : e.filename.replace('dumps/',''),
            'number' : e.number
        }
    return d

def pylint_detect(my_path):
    command = f'pylint --output-format=json {my_path}/*.py > temp.json'
    #command = f'find . -type f -wholename \'{my_path}/*.py\' | xargs pylint --output-format=json > temp.json'
    current_path = os.getcwd()
    os.chdir(my_path)
    codes = 'W0201,W0221,W0401,R0801,C1801,W0102,W0622,R0123,R0912,R1707,R1710,R1714,C0121,C0200,R1732'
    command = f'pylint --output-format=json --disable=all --enable={codes} j=0 *.py > {current_path}/temp.json'
    subprocess.run(command,shell=True)
    os.chdir(current_path)
    with open('temp.json') as f:
        errors = json.load(f)
    df = pd.DataFrame(errors)
    df['linter'] = 'pylint'
    df = df.rename(columns={'column' : 'col',
                        'line' : 'lnum',
                        'path' : 'filename',
                        'message-id' : 'number',
                        'message' : 'text'}
                )
    if len(df) > 0:
        df.type = df.type.apply(lambda x : x[0].upper())
    if len(df) > 0:
        df.filename = df.filename.apply(lambda x: x.replace('dumps/',''))
    return df


def pylama_detect(my_path):
    options = parse_options([my_path], **my_redefined_options)
    errors = check_path(options, rootdir='.')
    errors = list(map(error_to_dict, errors))
    errors = [i for i in errors if i['filename'].endswith('.py')]
    return pd.DataFrame(errors)

def detect(my_path):
    pylint = pylint_detect(my_path)
    pylama = pylama_detect(my_path)
    result = pd.concat([pylint,pylama])
    result = result.reset_index(drop=True)
    return result


if __name__ == '__main__':
    import pandas as pd
    errors = detect('./dumps')
    e = errors[0]
    df = pd.DataFrame(errors)