import pathlib
import subprocess
import json
import pandas as pd
from crawler import Crawler
from detector import detect
from commit_getter import get_commit

crawler = Crawler()

outputs_dir = pathlib.Path('outputs').absolute()
dumps_dir = crawler.dumps_dir.absolute()

def load_output(file_path):
    with open(file_path) as f:
        return json.load(f)

def add_meta(result_dict,commit, repo_name):
    result_dict['commit'] = commit
    result_dict['repo_name'] = repo_name


add_header = True
first = True
repo = None
while repo is not None or first == True:
    print('ok')
    repo = -1
    first = False
    crawler.next()
    output_path = pathlib.Path(outputs_dir,crawler.current_repo.name+'.json').absolute()
    if not output_path.exists():
        crawler.clone_current()
        result = detect(dumps_dir)
        df = pd.DataFrame(result)
        df['commit'] = crawler.current_commit
        df['repo'] = crawler.current_repo.full_name
        df.to_json(str(output_path))