import csv
import validation_data as val
import pandas as pd 
import time 
import json
import logging
import connector as con
from datetime import datetime
import controller_2 as con2


class Query():
    global over_max
    def __init__(self,local_max=9e9,options ={},username="",endpoint="",save_list=[],save_loc="",url=""):
        self.url = url
        self.username = username
        self.endpoint = endpoint
        self.options = options.copy()
        self.save_types= save_list 
        self.local_max = local_max
        self.data_h = Data_handelling(save_loc,self.local_max)


    def query_api(self):
     
        if con2.over_max == True:
            pass
        else:
            if self.url =="":
                self.raw_results = con.endpoint_connector(val.endpoint_filtering_dict()[self.endpoint],self.options)
            elif self.endpoint == "user lookup":
                self.raw_results = con.url_only_connector(self.url)
            else:
                self.raw_results = con.endpoint_connector(self.url,self.options)

    
    def add_token(self):
        self.options["pagination_token"] =self.token
    

    def process_data(self,addtion_file_name):
        
        if con2.over_max == True:
            self.allresults_data = pd.DataFrame(["No results obtained before total limit reached"])
        else:
            if "file" in self.save_types:
                self.data_h.json_to_file(self.raw_results,self.endpoint,addition=addtion_file_name)
            self.data_h.json_to_table(self.raw_results)
            self.token = self.data_h.get_pag_token()
            self.data_h.combine_new_data()
            self.re_query_token(addtion_file_name)

    def re_query_token(self,addtion_file_name):
        logging.debug(f"The token is {self.token}")
        while (self.token !=  None) & (con2.over_max != True) & (self.data_h.local_pulls < self.local_max) :
            logging.debug(f"{con2.over_max} is the current value of over max ")
            self.add_token()
            self.query_api()
            self.process_data(addtion_file_name)
        self.csv_save(addtion_file_name)
        self.allresults_data = self.data_h.all_results_data
    
    def csv_save(self,addtion_file_name):
        self.data_h.save_combined_to_csv(self.endpoint,addtion_file_name)

        

class TLU_query(Query):
    def __init__(self,local_max=9e9,tweet_id="",endpoint="",save_list=[],save_loc="",url=""):
        self.url = url
        self.tweet_id = tweet_id
        self.endpoint = endpoint
        self.save_types= save_list 
        self.local_max = local_max
        self.data_h = Data_handelling(save_loc,self.local_max)
    
    def query_api(self):
        self.raw_results = con.url_only_connector(self.url)


class Data_handelling():
    def __init__(self,save_loc:str,local_max_dh):
        self.page_counter = 0
        self.save_location = save_loc
        self.all_results_data = pd.DataFrame()
        self.all_results_meta = pd.DataFrame()
        self.local_pulls = 0


    def local_max_addition(self,addition):
        self.local_pulls = self.local_pulls+ addition


    def get_pag_token(self):
        try:
            token = self.meta_data_new["next_token"][0]
        except:
            logging.warning("No pagination token found")
            token = None
        return token

    def combine_new_data(self):
        frames = [self.all_results_data, self.results_new]
        self.all_results_data = pd.concat(frames)

        frames_meta = [self.all_results_meta,self.meta_data_new]
        self.all_results_meta =pd.concat(frames_meta)

        con2.add_to_return_counter(self.results_new.shape[0])
        self.local_max_addition(self.results_new.shape[0])

        self.page_counter += 1
    
    def json_to_table(self,api_return):
        """Takes in twitter api json dict and converts to pandas dataframes.
        there is a dataframe for the results and one for the meta data
        """    
        logging.debug("Starting json to table")

        #self.results_new = pd.json_normalize(api_return["data"])
        #print(self.results_new)
        try:
            self.results_new = pd.json_normalize(api_return["data"])    
        except:
            self.results_new = pd.DataFrame()
            json_dump = json.dumps(api_return, indent=4, sort_keys=True)
            logging.warning(f"Unable to normalize json for data in request{json_dump}")



        try:
            self.meta_data_new =  pd.json_normalize(api_return["meta"])
        except:
            self.meta_data_new = pd.DataFrame()
            json_dump = json.dumps(api_return, indent=4, sort_keys=True)
            logging.warning(f"Unable to normalize json for meta data in request{json_dump}")


        logging.debug("finished json to table")



    def json_to_file(self,api_return:dict,endpoint:str,addition=""):
        """Takesin in twitter api json dict and saves to a txt file in working directory. 

        Args:
            api_return (object): dictionary of jsons from twitter API
        """
        #logging.debug("Started json to file ")

        #This sleep ensures unique file names
        time.sleep(1)
        #used for file naming 
        date_time =str(datetime.now().strftime(' %d-%m-%Y %H_%M_%S' ))
        #logging.debug(date_time)
        if addition !="":
            addition = "_"+str(addition)+"_"

        #writes data to file
        with open(f"{self.save_location}twitter_json_{endpoint}{addition}_{str(self.page_counter)}_{date_time}.txt","w") as json_file:
            json.dump(api_return,json_file, indent=4, sort_keys=True)
    
    def save_combined_to_csv(self,endpoint:str,addition):
        final_save_file_name =f"{self.save_location}Twitter_Combined_Results_{endpoint}_{addition}.csv"
        self.all_results_data.to_csv(final_save_file_name)

        final_save_file_name_meta =f"{self.save_location}Twitter_Combined_Meta_Data_{endpoint}_{addition}.csv"
        self.all_results_meta.to_csv(final_save_file_name_meta)
        
