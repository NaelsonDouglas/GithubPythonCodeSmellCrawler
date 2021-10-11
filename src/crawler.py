import subprocess
import pathlib
from github import Github
from git import Git
from configparser import ConfigParser
import os
from shutil import rmtree
from glob import glob
import pandas as pd


configs = ConfigParser()
configs.read('configs.ini')
from tqdm import tqdm

DEBUG = True

blacklist = ('jackfrued/Python-100-Days',
    'donnemartin/system-design-primer',
    'vinta/awesome-python',
    'tensorflow/models',
    'fo40225/tensorflow-windows-wheel',
    'jeffkaufman/icdiff'
    )

class Crawler:
    def __init__(self):
        self.gh = Github(configs.get('github', 'token'))
        self.repos = self.gh.search_repositories(query='language:python', sort='stars', order='desc')
        self.repos = iter(self.repos)
        self.current_repo = ''
        self.visited_repos = []
        self.dumps_dir = pathlib.Path('dumps')
        self.git = Git(self.dumps_dir)
        self.blacklist = blacklist

    def append_blacklist(self, new_repos):
        self.blacklist = tuple(list(self.blacklist) + new_repos)

    def _make_clone_command(self, uri, repo_name):
        str_dumps_dir = str(self.dumps_dir)
        clone_command = f'git clone --depth 1 --filter=blob:limit=5m {uri} {str_dumps_dir}/{repo_name}'
        return clone_command

    def list_repo_contents(self, repo):
        contents = repo.get_contents('')
        result = []
        pbar = tqdm(total=len(contents))
        iterations = 0
        while contents:
            file_content = contents.pop(0)
            iterations += 1
            if file_content.type == 'dir':
                contents.extend(repo.get_contents(file_content.path))
                pbar.total = len(contents) + iterations
                pbar.refresh()
            else:
                if '.py' in file_content.path:
                    source_code = repo.get_contents(file_content.path).decoded_content.decode(
                        'UTF-8'
                    )
                    result.append(source_code)
            pbar.update(1)
        pbar.close()
        return result

    def next_repo_name(self):
        next_uri = self.next()
        repo_name = next_uri.split('/')[-1].split('.git')[0]
        return repo_name

    def next(self):
        try:
            repo = next(self.repos)
            if repo.full_name in self.blacklist:
                return self.next()
        except:
            repo = None
        self.current_repo = repo
        if repo != None:
            self.visited_repos.append(repo)
            result = repo.clone_url
        else:
            result = None
        self.current_uri = result
        print(f'Current repository: {self.current_repo}\n')
        return result

    def clear_directory(self):
        filelist = self.dumps_dir.glob('*')
        for f in filelist:
            if os.path.isfile(f):
                os.remove(f)
            else:
                rmtree(f)

    def get_current_repo_path(self):
        return pathlib.Path(self.dumps_dir.absolute(), self.current_repo.name)

    def clone_current(self):
        current_repo_path = self.get_current_repo_path()
        if self.current_uri != None:
            if not current_repo_path.exists():
                repo_name = self.current_repo.name
                clone_cmd = self._make_clone_command(self.current_uri,repo_name)
                process = subprocess.run(clone_cmd.split(), stdout=subprocess.PIPE)
                #self.git.clone(self.current_uri)
            if self.current_repo._rawData['fork']:
                return self.clone_current()
            return self.current_repo

    def list_files(self, extension='py'):
        files_list = [i for i in self.dumps_dir.rglob(f'*.{extension}')]
        files_list.sort()
        return files_list

# c = Crawler()
# c.clone_current()
# c.list_files()
if __name__ == '__main__':
    crawler = Crawler()

    repo = crawler.clone_current()
    print(repo)
    add_header = True
    while repo is not None:
        crawler.list_files()
        repo = crawler.clone_current()