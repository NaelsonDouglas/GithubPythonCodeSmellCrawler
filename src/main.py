import pathlib
import json
import pandas as pd
from crawler import Crawler
from static_crawler import StaticCrawler
from detector import pylint_detect
from commit_getter import get_commit, count_contributors, get_first_commit_date

GET_NEW_DATA = True

crawler = Crawler()
outputs_dir = pathlib.Path('outputs').absolute()
dumps_dir = crawler.dumps_dir.absolute()
# warnings_per_repo = pd.read_csv('warnings_per_repo.csv')
# already_collected = list(warnings_per_repo.repo.unique())
# crawler.append_blacklist(already_collected)


def load_output(file_path):
    with open(file_path, encoding='utf8') as f:
        return json.load(f)


def count_lines(repo_dir):
    sources = pathlib.Path(repo_dir).glob('**/*.py')
    nof_lines = 0
    for source in sources:
        if not source.is_dir():
            nof_lines = nof_lines + len(source.open().readlines())
    return nof_lines

def get_repo_metadata(crawler):
    repo_dir = str(crawler.get_current_repo_path())
    commit = get_commit(repo_dir)
    full_name = crawler.current_repo.full_name
    starsgazers = crawler.current_repo.stargazers_count
    contributors = count_contributors(repo_dir)
    nof_lines = count_lines(repo_dir)
    first_commit = get_first_commit_date(repo_dir)
    metadata = {'repo':full_name, 'stargazers': starsgazers,'warnings': 0, 'commit': commit, 'contributors': contributors, 'nof_lines': nof_lines, 'first_commit': first_commit}
    return metadata

def persist_metadata(metadata, output = 'warnings_per_repo.csv'):
    try:
        metas = pd.read_csv(output)
        metas = metas.append(metadata, ignore_index=True)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        metas = pd.DataFrame(metadata)
    metas = metas.groupby('repo').head(1)
    metas = metas.sort_values('stargazers').reset_index(drop=True)
    metas.to_csv(output,index=False)


def make_pylint_df(current_repo_dir):
    df = pylint_detect(str(current_repo_dir))
    df['lines_amount'] = 0
    warnings_count = len(df)
    metadata = get_repo_metadata(crawler)
    if warnings_count > 0:
        metadata['warnings'] = warnings_count
        for path in create_keep_list(current_repo_dir):
            try:
                source_text = path.read_text()
                amount_lines = 1 + len([char for char in source_text if char == '\n'])
            except UnicodeDecodeError:
                amount_lines = 0
            file_name = str(path).split(str(dumps_dir.name)+'/')[-1]
            file_name = file_name.replace(crawler.current_repo.name+'/','')
            df.loc[df.filename == file_name, 'lines_amount'] = amount_lines
        df['commit'] = metadata['commit']
        df['repo'] = crawler.current_repo.full_name
        df['stargazers'] = crawler.current_repo.stargazers_count
    persist_metadata(metadata, 'meta.csv')
    return df


def delete_files(file_list):
    for path in file_list:
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


def analyze_repository(crawler, output_path):
    crawler.clear_directory()
    crawler.clone_current()
    current_repo_dir = pathlib.Path(dumps_dir, crawler.current_repo.name).absolute()
    delete_list = create_delete_list(current_repo_dir)
    delete_files(delete_list)
    try:
        print('entrando')
        #df = make_pylint_df(current_repo_dir)
        meta = pd.DataFrame([get_repo_metadata(crawler)])
        persist_metadata(meta, 'meta.csv')
    except json.decoder.JSONDecodeError:
        print('bugou')
        meta = []
    if len(meta) > 0:
        meta.to_json(str(output_path))

if __name__ == '__main__':
    if GET_NEW_DATA:
        ADD_HEADER = True
        FIRST = True
        REPO = None
        while REPO is not None or FIRST is True:
            REPO = -1
            FIRST = False
            REPO = crawler.next()
            while REPO is None:
                REPO = crawler.next()
                print('skipping')
            output_path = pathlib.Path(outputs_dir, crawler.current_repo.name+'.json').absolute()
            if not output_path.exists():
                analyze_repository(crawler, output_path)

    jsons = list(outputs_dir.glob('*.json'))
    jsons = list(map(lambda x: json.loads(x.read_text()), jsons))
    df = pd.concat([pd.DataFrame(i) for i in jsons])
    df.reset_index(inplace=True, drop=True)
    df.to_parquet('data.parquet')
    del jsons
