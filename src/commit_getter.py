from pathlib import Path
import os

# def get_commit(repo_path):
#     git_folder = Path(repo_path,'.git')
#     head_name = Path(git_folder, 'HEAD').read_text().split('\n')[0].split(' ')[-1]
#     head_ref = Path(git_folder,head_name)
#     commit = head_ref.read_text().replace('\n','')
#     return commit
def run_detached(path, command):
    initial_dir = os.getcwd()
    os.chdir(str(path))
    result = os.popen(command).read().strip()
    os.chdir(initial_dir)
    return result

def count_contributors(repo_path):
    contributors = run_detached(repo_path, 'git shortlog -s -n')
    return len(contributors)

def get_first_commit_date(repo_path):
    commit = run_detached(repo_path, 'git log  --reverse --pretty=format:"%ad" --date=iso| head -1')
    return commit

def get_commit(repo_path):
    commit = run_detached(repo_path, 'git rev-parse HEAD')
    return commit

if __name__ == '__main__':
    cloned_repo_path = '/home/ndc/repos/GithubPythonCodeSmellCrawler/src/dumps/pylama'
    r = get_commit(cloned_repo_path)
    print(r)