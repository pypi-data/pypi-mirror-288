from systempath import Directory, File
import requests.__version__
from typing import Generator, Iterator

d = Directory('tree')

content = b'1'

for file in d.tree(omit_dir=True):
    # if not isinstance(x, File):
    #     continue

    if content in file:
        print(file)
