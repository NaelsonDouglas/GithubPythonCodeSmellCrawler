from pylava.main import check_path, parse_options
from rich import print

my_redefined_options = {
    #'linters': ['pep257', 'pydocstyle', 'pycodestyle', 'pyflakes'],
    'sort': 'F,E,W,C,D,...',
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
            'filename' : e.filename,
            'number' : e.number
        }
    return d

def detect(my_path):
    options = parse_options([my_path], **my_redefined_options)
    errors = check_path(options, rootdir='.')
    errors = list(map(error_to_dict, errors))
    errors = [i for i in errors if i['filename'].endswith('.py')]
    return errors

if __name__ == '__main__':
    import pandas as pd    
    errors = detect('./dumps')
    e = errors[0]
    df = pd.DataFrame(errors)
    print(df)