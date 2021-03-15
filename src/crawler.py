from github import Github
import git
from configparser import ConfigParser
configs = ConfigParser()
configs.read('configs.ini')
from tqdm import tqdm

class Crawler:
        def __init__(self):
                self.gh  = Github(configs.get('github','token'))
                self.repos = self.gh.search_repositories(query='language:python')
                self.repos = iter(self.repos)
                self.current_repo = ''
                self.visited_repos = []


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
                repo = next(self.repos)
                self.current_repo = repo.full_name
                self.visited_repos.append(repo)
                print(f'Current repository: {self.current_repo}')
                result = self.list_repo_contents(repo)
                return result

c = Crawler()