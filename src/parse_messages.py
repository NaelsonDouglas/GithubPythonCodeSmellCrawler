import re
import pandas as pd
from rich import print

def split_match(text):
    name, code = text.replace(':','').split(' ')
    code = code.replace('(','').replace(')','')
    result = (name, code)
    return result

text = None
with open('messages.txt') as f:
    text = f.read()


core = r'\:.*\s*\(.*\)\:'
messages = re.findall(core,text)
messages = [split_match(m) for m in messages]

df = pd.DataFrame(messages, columns = ['symbol','code'])
df.to_csv('new_codes.csv',index=False)
