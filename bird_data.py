import json
import os
import re

data="data.json"

if os.path.exists(data):
    with open(data, 'r') as file:
        onsitedata = json.load(file)
else:
    onsitedata = {}