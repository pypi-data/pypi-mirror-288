# ipynib extractor
srcsuffix = ".ipynb"
dstsuffix = ".py"
import json
from datetime import datetime

def makepy(*args):
    for basename in args:
        with open(basename+srcsuffix) as f:
            a = json.load(f)
        with open(basename+dstsuffix,'w') as f:
            for line in a['cells'][1]['source']:
                f.write(line)
        print(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} {basename}")