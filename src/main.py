import pathlib
import subprocess
import json
import pandas as pd
from crawler import Crawler
from detector import detect
from commit_getter import get_commit


GET_NEW_DATA = False


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
            crawler.clone_current()
            commit = get_commit(str(crawler.get_current_repo_path()))
            current_repo_dir = pathlib.Path(dumps_dir,crawler.current_repo.name).absolute()
            delete_list = list(current_repo_dir.rglob('*'))
            delete_list =  [i for i in delete_list if i.is_file() and not i.suffix == '.py']
            for path in delete_list:
                path.unlink()
            df = detect(str(current_repo_dir))
            df['commit'] = commit
            df['repo'] = crawler.current_repo.full_name
            df.to_json(str(output_path))

jsons = list(outputs_dir.glob('*.json'))
jsons = list(map(lambda x: json.loads(x.read_text()), jsons))
df = pd.concat([pd.DataFrame(i) for i in jsons])
df.reset_index(inplace=True,drop=True)
df.to_parquet('data.parquet')
del jsons