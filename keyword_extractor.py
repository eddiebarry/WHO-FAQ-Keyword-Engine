import json
from os import listdir
from os.path import join as os_path_join
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
    def __init__(self, config_path):
        """ Simple init function """
        # self.config = config

        self.config_path = config_path

        self.dict = {}
        for filename in listdir(config_path):
            if filename.endswith('.json'):
                project_id, version_id = filename.split('_')[:2]
                self.dict[project_id] = self.dict.setdefault(project_id, {})
                with open(os_path_join(config_path, filename), 'r') as f:
                    self.dict[project_id][version_id] = json.load(f)
    
    def parse_regex_query(self, query, project_id, version_id):
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
        project_id : String
            A unique identifier of the project of interest
        version_id : String
            A unique identifier of the version of interest
        """
        boosting_tokens = defaultdict(list)
        for fields in self.dict[project_id][version_id]:
            list_words = self.dict[project_id][version_id][fields]
            for wrd in list_words:
                if wrd in query:
                    boosting_tokens[fields].append(wrd.strip())
        
        return dict(boosting_tokens)

    def parse_config(self, config, project_id, version_id):

        # modifying the dictionary structure to be as expected (list of 
        # dictionaries with a single key each --> unique dictionary with 
        # including all keys):
        config = {list(d.keys())[0]: list(d.values())[0] for d in config}

        # updating the corresponding dictionary:
        self.dict[project_id][version_id] = config

        # finding the filename corresponding to the actual settings for the 
        # given project id and keyword id:
        filename_beginning = project_id + '_' + version_id + '_'
        for filename in listdir(self.config_path):
            if filename.endswith('.json') and  \
                filename.startswith(filename_beginning):
                break

        # # overwriting old settings in corresponding file with new settings:
        # with open(os_path_join(self.config_path, filename), 'w') as f:
        #     json.dump(self.dict[project_id][version_id], f)

if __name__ == '__main__':
    jsonpath = "./keyword_config"    
    ext = KeywordExtract(jsonpath)
    query = "what is the life expectancy of my child or son if they have polio?"
    print(ext.parse_regex_query(query, project_id='999', version_id='0'))