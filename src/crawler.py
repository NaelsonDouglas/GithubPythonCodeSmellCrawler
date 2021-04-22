from github import Github
from git import Git
from configparser import ConfigParser
import os
from shutil import rmtree
from glob import glob
configs = ConfigParser()
configs.read('configs.ini')
from tqdm import tqdm

DEBUG = False
class Crawler:
        def __init__(self):
                self.gh  = Github(configs.get('github','token'))
                self.repos = self.gh.search_repositories(query='language:python')
                self.repos = iter(self.repos)
                self.current_repo = ''
                self.visited_repos = []
                self.DUMPS_DIR = './dumps/'


        def list_repo_contents(self,repo):
                contents = repo.get_contents('')
                result = []
                pbar = tqdm(total=len(contents))
                iterations = 0
                while contents:
                        file_content = contents.pop(0)
                        iterations +=1
                        if file_content.type == 'dir':
                                contents.extend(repo.get_contents(file_content.path))
                                pbar.total = len(contents)+iterations
                                pbar.refresh()
                        else:
                                if '.py' in  file_content.path:
                                        source_code = repo.get_contents(file_content.path).decoded_content.decode('UTF-8')
                                        result.append(source_code)
                        pbar.update(1)
                pbar.close()
                return result


        def next(self):
                try:
                        if DEBUG:
                                if self.current_repo == '':
                                        repo = next(self.repos)
                                        while repo.full_name != 'donnemartin/system-design-primer':
                                                repo = next(self.repos)
                                                print(repo.full_name)
                        else:
                                repo = next(self.repos)
                except:
                        repo = None
                self.current_repo = repo
                if repo != None:
                        self.visited_repos.append(repo)
                        print(f'Current repository: {self.current_repo}')
                        result = repo.clone_url
                else:
                        result = None
                return result


        def clear_directory(self):
                filelist = glob(os.path.join(self.DUMPS_DIR, "*"))
                for f in filelist:
                        if os.path.isfile(f):
                                os.remove(f)
                        else:
                                rmtree(f)


        def clone_next(self):
                repo = self.next()
                repo_base_name = self.DUMPS_DIR+repo.split('/')[-1].split('.git')[0]
                if repo != None:
                        if not DEBUG:
                                self.clear_directory()
                        if not os.path.isdir(repo_base_name):
                                Git(self.DUMPS_DIR).clone(repo)
                        if self.current_repo._rawData['fork']:
                                return self.clone_next()
                        return self.current_repo

        def list_files(self,extension='py'):
                files_list = []
                for root, directories, files in os.walk(self.DUMPS_DIR):
                        for name in files:
                                if extension is None or name.endswith(extension):
                                        files_list.append(os.path.join(root, name))
                files_list.sort()
                return files_list

# c = Crawler()
# c.clone_next()
# c.list_files()