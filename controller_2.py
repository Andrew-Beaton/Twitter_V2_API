

import json
import logging
import validation_data as val
import os
import query_dm as qd

def start_return_counter(max_returns:int):
    global total_returns
    global over_max
    global max_overall_returns

    max_overall_returns = max_returns
    over_max = False
    total_returns = 0

def add_to_return_counter(new_results_total:int):
    global total_returns
    global max_overall_returns
    global over_max
    logging.debug(f"total returns is {total_returns}")
    logging.debug(f"new_results total is {new_results_total}")
    total_return_type= type(total_returns)

    total_returns += int(new_results_total)
    t_return_type = type(new_results_total)
    logging.debug(f"New total returns is {total_returns}")

    if total_returns >= max_overall_returns:
        over_max = True

def get_current_dir_path():
    return os.getcwd()


def controller_master(endpoint_list:list,master_query:dict,out_types:list,tweet_id:list,
                        max_overall_returns:int,split_max_across_users,save_dir=""):
    logging.debug("Starting max return counter")

    if save_dir =="":
        save_dir = get_current_dir_path()
        logging.debug(f"save_dir set to {save_dir}")

    start_return_counter(max_overall_returns)
    logging.debug("Starting debug")


    val.validation_master(endpoint_list,master_query)
    logging.debug(f"Validation complete")
    #if
       #restart_manager


    processed_query_endpoint,endpoint_options = builder(endpoint_list,master_query,tweet_id)
    logging.debug(f"Builder is compelete with keys {processed_query_endpoint.keys()}")
    logging.debug(f"Builder is compelete with option keys {endpoint_options.keys()}")


    if split_max_across_users == True:
        local_max = int(max_overall_returns/(len(endpoint_list)*(master_query["usernames"].count(",")+1)))
    else:
        local_max=int(9e9)

    logging.debug(f"local max is {local_max}")    
        
    final_results = {}
    class_dict = {}

    for endpoint, user_dict  in processed_query_endpoint.items():


        if endpoint =="tweet timeline":
            for username,url in user_dict.items():
                run_name  = f"{endpoint}_{username}"

                class_dict[run_name] = qd.Query(local_max = local_max,url=url,endpoint =endpoint,username=username,options=endpoint_options[endpoint],
                save_loc = save_dir,save_list=out_types)

                class_dict[run_name].query_api()
                class_dict[run_name].process_data(username)
                logging.debug(f"finished {endpoint} {username}")
                final_results[f"{endpoint}_{username}"] =class_dict[run_name].allresults_data



        elif endpoint in ["search tweets","tweet count"]:
            run_name  = f"{endpoint}"
            class_dict[run_name] = qd.Query(local_max =local_max,url=val.endpoint_filtering_dict()[endpoint]
            ,endpoint =endpoint,options=endpoint_options[endpoint],
            save_loc = save_dir,save_list=out_types)

            class_dict[run_name].query_api()    
            class_dict[run_name].process_data("")
            logging.debug(f"finished {endpoint}")
            final_results[f"{endpoint}"] =class_dict[run_name].allresults_data
        
        elif endpoint =="tweets liking users":
            for tweet_id,url in user_dict.items():
                run_name  = f"{endpoint}_{tweet_id}"
                class_dict[run_name] = qd.TLU_query(local_max = local_max,url=url,tweet_id=tweet_id,
                save_loc = save_dir,save_list=out_types)

                class_dict[run_name].query_api()
                class_dict[run_name].process_data(tweet_id)
                logging.debug(f"finished {endpoint} {tweet_id}")
                final_results[f"{endpoint}_{tweet_id}"] =class_dict[run_name].allresults_data

            
   
    return final_results

def standard_query_builder(endpoint_specific_options:dict,endpoint:str,master_query:dict)->dict:
    """Creates a standard quey using the key filtering dictionary and endpoints. With these it checks the master
    query and includes ones it can find there and logs for info any it can not. 

    Args:
        endpoint_specific_query (dict): dict that has all the querys in it which will be added to and output
        endpoint (str): Specific endpoint uses in this run of the function
        master_query (dict): user generated query which all endpoint queries come from/

    Returns:
        dict: List of all endpoint customized queries  including the new one from this function run
    """
    for element in val.endpoint_key_filtering_dict()[endpoint] :
                try:
                    #tries to find that option as a key in the master query and adds it to the current endpoint
                    #specific query
                    endpoint_specific_options[element] = master_query[element]
                except:
                    #logs when a possible option for the endpoint is not used
                    logging.info(f"did not find {element} in master query")
    return endpoint_specific_options









def builder(endpoint_list:list,master_query:dict,tweet_id:list) ->dict: 
    """This function controls all of the building of the queries that will later be sent to the API
    It handles different types of endpoint and executes the correct sub building process for the endppoint

    Args:
        endpoint_list (list): List of all endpoints that have been requested by the user
        master_query (dict): The complete query as set out by the user
        tweet_id (list): This is a list that can be used for looking up the tweets liking users endpoint

    Returns:
        dict: build queries in various forms which are then going to be used with the connectors to make 
        the API requests
    """
    #list to section of the url builds that need user lookups
    url_with_user_lookup_list = ["tweet timeline","users liked tweets","user following"]
    endpoint_query_option_builder = {}
    processed_query_endpoint = {}
    for endpoint in endpoint_list:
        logging.debug(f"start Endpoint {endpoint}")
        endpoint_specific_query = {}
        #logging.debug(f"current endpoint is {endpoint}")

        #the use lookup endpoint requires specific handling
        if endpoint == "user lookup":
            user_lookup_url_final = user_search_url_builder(val.endpoint_filtering_dict()[endpoint]
                                                            ,master_query,val.endpoint_key_filtering_dict())

            processed_query_endpoint[endpoint] = user_lookup_url_final
        
        #executes specific behaviour if the endpoint has been added to the url endpoint list
        elif endpoint in url_with_user_lookup_list:
            logging.debug(f"endpoint : {endpoint} is in url user lookup")
            timeline_url_final = url_builder_with_user_lookup(val.endpoint_filtering_dict()[endpoint],
                                                            master_query)
            logging.debug(f" url buiilder with user lookup  returned  {timeline_url_final}")
            processed_query_endpoint[endpoint] = timeline_url_final
            endpoint_query_option_builder [endpoint] = standard_query_builder(endpoint_specific_query,endpoint,master_query)

        elif endpoint == "tweets liking users":
            
            processed_query_endpoint[endpoint] = url_builder_from_list(val.endpoint_filtering_dict()[endpoint],tweet_id)


        else:
        #selects each possible option for each endpoint in the user given list
            logging.debug(f"endpoint : {endpoint} is in general build")
            endpoint_specific_query = standard_query_builder(endpoint_specific_query,endpoint,master_query)

            processed_query_endpoint[endpoint] =val.endpoint_filtering_dict()[endpoint]
            endpoint_query_option_builder[endpoint] = endpoint_specific_query
            
            #logging.debug([endpoint_query_option_builder[endpoint],endpoint])
    logging.debug(f"The porcessed query endpoint is {processed_query_endpoint}")
    logging.debug(f"th endpoint query options are {endpoint_query_option_builder}")

    return [processed_query_endpoint,endpoint_query_option_builder]








def user_search_url_builder(url:str,master_query:dict,endpoint_option_filtering:dict) -> str:
    """Creates the customized url for the users specified in the master query

    Args:
        url (str): This is the base url for the endpoint
        master_query (dict): Initial user supplied query
        endpoint_option_filtering (dict): the fields list which each endpoint will accept

    Returns:
        str: created a url with the user and the custom request options specifid by the user 
    """
    
    url_usernames  =  url+"usernames="+master_query["usernames"]
    for element in endpoint_option_filtering["user lookup"]:
        if element != "usernames":
            try:
                url_customized = url_usernames +"&"+str(element)+"="+ master_query[element]
            except:
                logging.info(f"Did not find  {element} to add to user lookup {url_usernames}")

    if url_customized in locals():
        return (url_customized)
    else:
        return(url_usernames)


def url_builder_with_user_lookup(url:str,master_query:dict) ->dict:
    """Creates the url while doirng required userd id lookup.

    Args:
        url (str): This is the base url for the endpoint that will be used to build the custom request onto
        master_query (dict): Users initially submitted query

    Returns:
        dict: url for each user in the list and their usernames as the dict key
    """    

    user_lookup_results = user_lookup_for_other_endpoints(master_query)
    formatted_urls = embed_userID_in_url(user_lookup_results,url)
    logging.debug(formatted_urls)
    
    return formatted_urls
    


def url_builder_from_list(url:str,insert_list:list) ->dict:
    """created a dict of urls which have the insert from the insert list

    Args:
        url (str): _url with {} set up for .fromat insert
        insert_list (list): list of items to be set in url individually

    Returns:
        dict: key is insert and value is url with insert in it ready for api 
    """
    formatted_url = {}
    for inserts in insert_list:
        formatted_url[inserts] = url.format(inserts)
        logging.debug(f"finished formatting {formatted_url}")

    return formatted_url

def user_lookup_for_other_endpoints(master_query:dict):

        user_lookup_url_final = user_search_url_builder(val.endpoint_filtering_dict()["user lookup"],
                                                        master_query,val.endpoint_key_filtering_dict())
        print(user_lookup_url_final)
        user_lookup = qd.Query(url=user_lookup_url_final,endpoint ="user lookup")
        user_lookup.query_api()
        user_lookup.process_data()
        return user_lookup.allresults_data
    
def organise_usernames_ids(user_lookup_results:dict) ->dict:
    """Collects usernames and id into a dictionary which matches them together

    Args:
        user_lookup_results (dict):The results of the use lookup from the API

    Returns:
        usernames_with_id (dict) : matched usernames and IDs 
    """        
    user_ID_list  = user_lookup_results["id"].tolist()
    username_list = user_lookup_results["username"].tolist()
    usernames_with_id  =dict(zip(username_list,user_ID_list))
    return usernames_with_id

def embed_userID_in_url(user_lookup_results,url:str):
    formatted_urls = {}

    usernames_with_id = organise_usernames_ids(user_lookup_results)

    for username,id in usernames_with_id.items():
        try:
            formatted_urls[username] = url.format(id)
        except:
            logging.warning(f"Unable to format timeline url for {id}")

    return formatted_urls