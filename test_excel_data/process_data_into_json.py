import pandas as pd
import json
import hashlib

xl = pd.read_excel("./VSN Categorization Template V3.xlsx")
xl = xl.fillna("")
print(xl.head())

for x in xl.columns:
    print(x)

for idx,x in xl.iterrows():
    object_dict = dict(x)
    json_name = hashlib.sha512(x['Master Question'].encode()).hexdigest()
    json_file_name = "/root/pylucene/FAQ_Answer_project/keyword_engine/test_excel_data/json_data/" + json_name+".json"
    with open(json_file_name , 'w') as json_file:
        json.dump(object_dict, json_file, indent = 4, sort_keys=True)

# list of unique labels
