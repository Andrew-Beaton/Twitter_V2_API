
class Validation():
    def __init__(self,endpoint_list:list,query:dict,save_location:str,tweet_id):
        self.endpoint_list  = endpoint_list
        self.raw_query = query
        self.save_location = save_location
        self.tweet_id =tweet_id
