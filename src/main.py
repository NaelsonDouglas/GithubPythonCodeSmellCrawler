import pathlib
import subprocess
import json
import pandas as pd
from crawler import Crawler

outputs_dir = pathlib.Path('outputs')
crawler = Crawler()

def load_output(file_path):
    with open(file_path) as f:
        return json.load(f)

add_header = True
first = True
repo = None
while repo is not None or first == True:
    repo = -1
    first = False    
    next_repo_name = crawler.next_repo_name()
    output_path = pathlib.Path(outputs_dir,next_repo_name+'.json')
    if not output_path.exists():
        repo = crawler.clone_current()
        command = f'pylint --output-format=json *.py > {str(output_path.absolute())}.json'
        subprocess.run(command,shell=True)