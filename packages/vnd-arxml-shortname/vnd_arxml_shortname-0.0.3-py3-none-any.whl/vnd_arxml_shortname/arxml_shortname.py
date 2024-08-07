import os
from typing import List
import re

def sdb_shortname(dirpath: str, filenames):
    pattern = r'MAIN[^-]*'
    for file in filenames:
        base, ext = os.path.splitext(file)
        if ext in (".arxml", ".dbc", ".ldf"):
            name_split = base.split('_')
            name_split = [word for word in name_split if word != 'MAIN']
            name_split = [re.sub(pattern, '', part) for part in name_split]
            for part in name_split:
                if part.isdigit():
                    name_split.remove(part)
                if 'AR-' in part:
                    name_split.remove(part)

            print(f'Old name: {base}, extension: {ext}')
            new_base = str("_".join(name_split))
            print(f'New name: {new_base}')
            complete_new_name = "".join([new_base, ext])
            os.rename(os.path.join(dirpath, file), os.path.join(dirpath, complete_new_name))
