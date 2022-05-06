from crawler import Crawler
import pandas as pd
from github import Github
from configparser import ConfigParser
from commit_getter import checkout_repo
import pathlib

configs = ConfigParser()
configs.read('configs.ini')

commits = dict(pd.read_parquet('data.parquet')[['repo','commit']].values)
warnings = pd.read_csv('warnings_per_repo.csv')[['repo']]
warnings['commit'] = warnings.repo.apply(lambda x: commits.get(x))

class StaticCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.repos = (self.gh.get_repo(r) for r in warnings.repo)
        self.commits = (c for c in warnings.commit.values)
        self.current_repo = None
        self.current_commit = None

    def next(self):
        super().next()
        print('changed the commit')
        self.current_commit = next(self.commits)

    def clone_current(self):
        super().clone_current()
        if self.current_commit is not None:
            checkout_repo(self.get_current_repo_path(), self.current_commit)

if __name__ == '__main__':
    from main import get_repo_metadata, persist_metadata
    c = StaticCrawler()
    c.next()
    while c.current_repo is not None:
        c.clone_current()
        metadata = get_repo_metadata(c)
        c.next()
        c.clear_directory()
        persist_metadata(metadata, 'meta.csv')