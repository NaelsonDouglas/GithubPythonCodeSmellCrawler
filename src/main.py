import pathlib
import subprocess
import os
import json
import pandas as pd
from crawler import Crawler
from detector import pylint_detect
from commit_getter import get_commit


GET_NEW_DATA = False


crawler = Crawler()
outputs_dir = pathlib.Path('outputs').absolute()
dumps_dir = crawler.dumps_dir.absolute()
already_collected = pd.read_parquet('data.parquet')
already_collected = list(already_collected.repo.unique())

def load_output(file_path):
    with open(file_path) as f:
        return json.load(f)

def add_meta(result_dict,commit, repo_name):
    result_dict['commit'] = commit
    result_dict['repo_name'] = repo_name

def make_pylint_df():
    df = pylint_detect(str(current_repo_dir))
    df['lines_amount'] = 0
    if len(df) > 0:
        relevant_files = df.filename.unique()
        for path in keep_list:
            try:
                source_text = path.read_text()
                amount_lines = 1 + len([char for char in source_text if char == '\n'])
            except UnicodeDecodeError:
                amount_lines = 0
            file_name = str(path).split(str(dumps_dir.name)+'/')[-1]
            file_name = file_name.replace(crawler.current_repo.name+'/','')
            df.loc[df.filename == file_name, 'lines_amount'] = amount_lines
        df['commit'] = commit
        df['repo'] = crawler.current_repo.full_name
    return df

def delete_files(file_list):
    for path in delete_list:
        path.unlink()

def create_all_files(repo_dir):
    return list(repo_dir.rglob('*'))

def create_keep_list(repo_dir):
    all_files = create_all_files(repo_dir)
    keep_list =  [i for i in all_files if i.is_file() and i.suffix == '.py']
    return keep_list

def create_delete_list(repo_dir):
    all_files = list(repo_dir.rglob('*'))
    delete_list =  [i for i in all_files if i.is_file() and not i.suffix == '.py']
    return delete_list


if __name__ == '__main__':
    if GET_NEW_DATA:
        add_header = True
        first = True
        repo = None
        while repo is not None or first == True:
            repo = -1
            first = False
            repo = crawler.next()
            while repo is None or crawler.current_repo.full_name in already_collected:
                repo = crawler.next()
                print('skipping')
            output_path = pathlib.Path(outputs_dir,crawler.current_repo.name+'.json').absolute()
            if not output_path.exists():
                crawler.clear_directory()
                crawler.clone_current()
                commit = get_commit(str(crawler.get_current_repo_path()))
                current_repo_dir = pathlib.Path(dumps_dir,crawler.current_repo.name).absolute()
                keep_list = create_keep_list(current_repo_dir)
                delete_list = create_delete_list(current_repo_dir)
                delete_files(delete_list)
                try:
                    df = make_pylint_df()
                except json.decoder.JSONDecodeError:
                    continue
                if len(df) > 0:
                    df.to_json(str(output_path))

    jsons = list(outputs_dir.glob('*.json'))
    jsons = list(map(lambda x: json.loads(x.read_text()), jsons))
    df = pd.concat([pd.DataFrame(i) for i in jsons])
    df.reset_index(inplace=True,drop=True)
    df.to_parquet('data.parquet')
    del jsons