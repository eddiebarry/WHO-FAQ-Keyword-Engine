import json
from collections import defaultdict

class KeywordExtract:
    def __init__(self, config):
        self.config = config
        self.dict = self.parse_config(self.config)
    
    def parse_regex_query(self, query):
        boosting_tokens = defaultdict(list)
        for fields in self.dict:
            list_words = self.config[fields]
            for wrd in list_words:
                if wrd in query:
                    boosting_tokens[fields].append(wrd.strip())
        
        return dict(boosting_tokens)

    def parse_config(self, config):
        return config

if __name__ == '__main__':
    jsonpath = "./test_excel_data/curated_keywords.json"
    f = open(jsonpath,)
    jsonObj = json.load(f)
    
    ext = KeywordExtract(jsonObj)
    query = "what is the life expectancy of my child or son ?"
    print(ext.parse_regex_query(query))
