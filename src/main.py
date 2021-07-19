import pathlib
import subprocess
import os
import json
import pandas as pd
from crawler import Crawler
from detector import pylint_detect
from commit_getter import get_commit


GET_NEW_DATA = True


crawler = Crawler()
outputs_dir = pathlib.Path('outputs').absolute()
dumps_dir = crawler.dumps_dir.absolute()



def load_output(file_path):
    with open(file_path) as f:
        return json.load(f)



def add_meta(result_dict,commit, repo_name):
    result_dict['commit'] = commit
    result_dict['repo_name'] = repo_name



if GET_NEW_DATA:
    add_header = True
    first = True
    repo = None
    while repo is not None or first == True:
        repo = -1
        first = False
        crawler.next()
        output_path = pathlib.Path(outputs_dir,crawler.current_repo.name+'.json').absolute()
        if not output_path.exists():
            crawler.clear_directory()
            crawler.clone_current()
            commit = get_commit(str(crawler.get_current_repo_path()))
            current_repo_dir = pathlib.Path(dumps_dir,crawler.current_repo.name).absolute()
            all_files = list(current_repo_dir.rglob('*'))
            delete_list =  [i for i in all_files if i.is_file() and not i.suffix == '.py']
            keep_list =  [i for i in all_files if i.is_file() and i.suffix == '.py']
            for path in delete_list:                
                path.unlink()
            df = pylint_detect(str(current_repo_dir))
            df['lines_amnt'] = 0
            for path in keep_list:
                source_text = path.read_text()
                amount_lines = 1 + len([char for char in source_text if char == '\n'])
                file_name = str(path).split(str(dumps_dir.name)+'/')[-1]
                df.loc[df.filename == file_name, 'lines_amnt'] = amount_lines
                if len(df) > 5:
                    pass
                    #breakpoint()
            df['commit'] = commit
            df['repo'] = crawler.current_repo.full_name
            df.to_json(str(output_path))

jsons = list(outputs_dir.glob('*.json'))
jsons = list(map(lambda x: json.loads(x.read_text()), jsons))
df = pd.concat([pd.DataFrame(i) for i in jsons])
df.reset_index(inplace=True,drop=True)
df.to_parquet('data.parquet')
del jsons