# how to deploy a model
-open a jupyter notebook or python file: 

import pandas as pd \
import requests \
import json

df = pd.read_csv('data/Testing.csv')\
features = list(df.columns)\
target = 'outcome'\
features.remove(target)\
features.remove('Unnamed: 0')\
test_row= df[features].iloc[2,:].to_dict()

d = {'query':test_row}\
url = 'http://INSERT_PUBLIC_IP:5000/' \
headers =  {'Content-type': 'application/json', 'Accept': 'text/plain'}\
response = requests.get(url, data=json.dumps(d),headers=headers,timeout=3)\
response.json()
