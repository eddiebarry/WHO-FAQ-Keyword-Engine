import pandas as pd
import json
import hashlib
import re


xl = pd.read_excel("./VSN Categorization Template V3.xlsx")
xl = xl.fillna("")
print(xl.head())

config_dict = {}
for x in xl.columns:
    if x in ["Master Question", "Master Answer"]:
        continue
    config_dict[x]= list(xl[x].unique())

def process_config_dict(dic):
    new_dict = {}
    for x in dic:
        new_list = []
        for string in dic[x]:
            string = string.replace('(',',').replace(')',',').replace('/',',')
            new_ = string.lower().split(',')
            new = [x.strip() for x in new_]
            new_list.extend(new)
        
        if "" in new_list:
            new_list.remove("")

        new_dict[x]= list(set(new_list))
    
    return new_dict

        

config_dict = process_config_dict(config_dict)

for idx,x in xl.iterrows():
    object_dict = dict(x)
    json_name = hashlib.sha512(x['Master Question'].encode()).hexdigest()
    json_file_name = "/root/pylucene/FAQ_Answer_project/keyword_engine/test_excel_data/json_data/" + json_name+".json"
    with open(json_file_name , 'w') as json_file:
        json.dump(object_dict, json_file, indent = 4, sort_keys=True)

json_file_name = "unique_keywords.json"
with open(json_file_name , 'w') as json_file:
    json.dump(config_dict, json_file, indent = 4, sort_keys=True)

