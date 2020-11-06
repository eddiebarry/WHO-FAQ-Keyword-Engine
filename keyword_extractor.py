import json
from collections import defaultdict

class KeywordExtract:
    """
    Keyword extract is the class which is used for extracting
    keywords from user queries.

    A configuration file of the form :
    {
        "Country": [
            "india",
            "canada"
        ],
        "Disease 2": [
            "tetanus",
            "measles",
            "varicella",
            "chickenpox",
            "pertussis"
        ],
        "Vaccine": [
            "flu",
            "rubella",
            "tetanus",
            "dtap",
        ],
    }

    is needed, where the key is the name of the lucene field and the value
    is the list of all possible values that can be stored in the field.
    The keyword engine extracts these keywords from the query

    At search time, the key-value pairs are used for generating boosting
    tokens

    Attributes
    ----------
    config : jsonObject
        config is the json object which follows the specifications above
        for extracting keywords
    
    dict : Dictionary
        A python dictionary which stores the same info as the config.
        Seperation is maintained as the Json scheme may change, however
        the dictionary must be the same

    Methods
    __init__(config)
        The json configuration file must be loaded and then passed
        to the constructor
    
    parse_regex_query(query)
        Checks if a particular keyword is present in the query string and then
        returns the query string
    """
    def __init__(self, config):
        """ Simple init function """
        # self.config = config
        self.dict = config
    
    def parse_regex_query(self, query):
        """
        Takes a user input query, checks if each keyword specified in the
        config is present or not, and then returns the keyword along
        with the field it should belong to of the format

        boosting_tokens = {
            "keywords":["love"],    
            "subject1":["care"]
        }

        Inputs
        ------
        query_string : String
            The string input by the user
        """
        boosting_tokens = defaultdict(list)
        for fields in self.dict:
            list_words = self.dict[fields]
            for wrd in list_words:
                if wrd in query:
                    boosting_tokens[fields].append(wrd.strip())
        
        return dict(boosting_tokens)

    def parse_config(self, config):
        new_config = {}
        for x in config:
            new_config.update(x)
        return new_config

if __name__ == '__main__':
    jsonpath = "./keyword_config/curated_keywords_1500.json"
    f = open(jsonpath,)
    jsonObj = json.load(f)
    
    ext = KeywordExtract(jsonObj)
    query = "what is the life expectancy of my child or son if they have polio?"
    print(ext.parse_regex_query(query))