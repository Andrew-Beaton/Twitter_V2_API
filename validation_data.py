import logging
import dictionary_functions  as dictf


def endpoint_filtering_dict():
    #List of all endpoints currently setup for access through this code and their urls 
    end_point_repository = {"search tweets":"https://api.twitter.com/2/tweets/search/recent",
                        "tweet count":"https://api.twitter.com/2/tweets/counts/recent",
                        "user lookup":"https://api.twitter.com/2/users/by?",
                        "tweet timeline":"https://api.twitter.com/2/users/{}/tweets",
                        "users liked tweets":"https://api.twitter.com/2/users/{}/liked_tweets",
                        "tweets liking users":"https://api.twitter.com/2/tweets/{}/liking_users",
                        "user following":"https://api.twitter.com/2/users/{}/following"
                        }
    return end_point_repository


def endpoint_key_filtering_dict() ->dict:
    #dict containing lists of keys that can be used with each endpoint. This ensures that only 
    #applicable requests go to each endpoint.
    endpoint_option_filtering = {"search tweets":["query","tweet.fields","user.fields","expansions","media.fields","place.fields","poll.fields","max_results"],
                        "tweet count":["query","granularity","end_time","since_id","start_time"],
                        "user lookup":["usernames","tweet.fields","user.fields","expansions","max_results"],
                        "tweet timeline": ["tweet.fields","user.fields","expansions","max_results","media.fields","place.fields","poll.fields"],
                        "users liked tweets":["expansions","max_results","media.fields","pagination_token","place.fields","poll.fields","tweet.fields","user.fields"],
                        "tweets liking users":["expansions","max_results","media.fields","pagination_token","place.fields","poll.fields","tweet.fields","user.fields"],
                        "user following":["expansions","max_results","pagination_token","tweet.fields","user.fields"]
                        }


    return endpoint_option_filtering


def user_following_enum_values():
    users_following = {
        "expansions":"pinned_tweet_id",
        "tweet.fields":"",
        "user.fields":"created_at, description, entities, id, location, name, pinned_tweet_id, profile_image_url, protected, public_metrics, url, username, verified, withheld"
    }
    return users_following


def users_liked_tweets_enum_values():
    users_liked_tweets = {
        "expansions":"pinned_tweet_id",
        "media.fields":"duration_ms, height, media_key, preview_image_url, type, url, width, public_metrics, non_public_metrics, organic_metrics, promoted_metrics, alt_text",
        "place.fields":"contained_within, country, country_code, full_name, geo, id, name, place_type",
        "pool.fields":"duration_minutes, end_datetime, id, options, voting_status",
        "tweet.fields":"attachments, author_id, context_annotations, conversation_id, created_at, entities, geo, id, in_reply_to_user_id, lang, non_public_metrics, public_metrics, organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets, reply_settings, source, text, withheld",
        "user.fields":"created_at, description, entities, id, location, name, pinned_tweet_id, profile_image_url, protected, public_metrics, url, username, verified, withheld"

    }
    return users_liked_tweets

def tweets_liking_users_enum_values():
    tweets_liking_users = {
        "expansions":"pinned_tweet_id",
        "media.fields":"duration_ms, height, media_key, preview_image_url, type, url, width, public_metrics, non_public_metrics, organic_metrics, promoted_metrics, alt_text",
        "place.fields":"contained_within, country, country_code, full_name, geo, id, name, place_type",
        "pool.fields":"duration_minutes, end_datetime, id, options, voting_status",
        "tweet.fields":"attachments, author_id, context_annotations, conversation_id, created_at, entities, geo, id, in_reply_to_user_id, lang, non_public_metrics, public_metrics, organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets, reply_settings, source, text, withheld",
        "user.fields":"created_at, description, entities, id, location, name, pinned_tweet_id, profile_image_url, protected, public_metrics, url, username, verified, withheld"

    }
    return tweets_liking_users

def tweet_timeline_enum_values():
    #timeline enum fields
    timeline = {
            "tweet.fields":"attachments, author_id, context_annotations, conversation_id, created_at, entities, geo, id, in_reply_to_user_id, lang, non_public_metrics, public_metrics, organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets, reply_settings, source, text, withheld",
            "user.fields":"created_at, description, entities, id, location, name, pinned_tweet_id, profile_image_url, protected, public_metrics, url, username, verified, withheld)",
            "expansions":"attachments.poll_ids, attachments.media_keys, author_id, entities.mentions.username, geo.place_id, in_reply_to_user_id, referenced_tweets.id, referenced_tweets.id.author_id",
            "media.fields":"duration_ms, height, media_key, preview_image_url, type, url, width, public_metrics, non_public_metrics, organic_metrics, promoted_metrics, alt_text, variants",
            "place.fields":"contained_within, country, country_code, full_name, geo, id, name, place_type",
            "poll.fields" :"duration_minutes, end_datetime, id, options, voting_status"
        }
    return timeline
def search_tweets_enum_values():
    #search_tweets enum fields
    search_tweets = {
            "tweet.fields":"attachments, author_id, context_annotations, conversation_id, created_at, entities, geo, id, in_reply_to_user_id, lang, non_public_metrics, public_metrics, organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets, reply_settings, source, text, withheld",
            "user.fields":"created_at, description, entities, id, location, name, pinned_tweet_id, profile_image_url, protected, public_metrics, url, username, verified, withheld",
            "expansions":"attachments.poll_ids, attachments.media_keys, author_id, entities.mentions.username, geo.place_id, in_reply_to_user_id, referenced_tweets.id, referenced_tweets.id.author_id",
            "media.fields":"duration_ms, height, media_key, preview_image_url, type, url, width, public_metrics, non_public_metrics, organic_metrics, promoted_metrics, alt_text",
            "place.fields":"contained_within, country, country_code, full_name, geo, id, name, place_type",
            "poll.fields" :"duration_minutes, end_datetime, id, options, voting_status"
        }
    return search_tweets

    
def tweet_count_enum_values():
    #tweet count enum fields
        #Notes - there are none for tweet count 
    tweet_count = {
        }
    return tweet_count

def user_lookup_enum_values():
    #user lookup enum fields
        #Notes - there are none for tweet count 
    user_lookup = {"expansions":"pinned_tweet_id",
                    "tweet.fields":"attachments, author_id, context_annotations, conversation_id, created_at, entities, geo, id, in_reply_to_user_id, lang, non_public_metrics, public_metrics, organic_metrics, promoted_metrics, possibly_sensitive, referenced_tweets, reply_settings, source, text, withheld",
                    "user.fields":"created_at, description, entities, id, location, name, pinned_tweet_id, profile_image_url, protected, public_metrics, url, username, verified, withheld"
        }
    return user_lookup

def endpoint_field_enum_value(selection:str):
    """Returns the selected endpoints enum dictionaries 

    Args:
        selection (str): _description_

    Returns:
        _type_: _description_
    """
    #make this into a dict call at some point rather than an elif spam
    if selection =="all":
        return {"tweet timeline":tweet_timeline_enum_values(),
                "search tweets":search_tweets_enum_values(),
                "tweet count":tweet_count_enum_values(),
                "user lookup":user_lookup_enum_values(),
                "users liked tweets":users_liked_tweets_enum_values(),
                "tweets liking users":tweets_liking_users_enum_values(),
                "user following": user_following_enum_values(),
                
                }
    else :
        try:
            res = {"tweet timeline":tweet_timeline_enum_values,
                "search tweets":search_tweets_enum_values,
                "tweet count":tweet_count_enum_values,
                "user lookup":user_lookup_enum_values,
                "users liked tweets":users_liked_tweets_enum_values,
                "tweets liking users":tweets_liking_users_enum_values,
                "user following": user_following_enum_values,
               
            }.get(selection)()
            return res
        except:

            logging.error(f"{selection} is not a valid option for endpoint_field_enum_value ")
            exit()





def key_validator(master_query:dict):
    """Checks that all keys supplied are used in at least one endpoint 


    Args:
        master_query (dict): The user supplied query which is checked against endpoint accepted keys
    """
    for key,value in master_query.items():
        present = 0
        # This should be improved at somepoint it can likely be improved in some way
        for dict_lists in endpoint_key_filtering_dict().values():
            if key  in dict_lists :
                present +=1 
                break
            
        if present == 0:
            logging.error(f"{key} is not a supported option")
            exit()


def value_checker(master_query:dict,endpoint_list:list):
    """Checks all enum options to ensure that they are valid for at least one endpoint
    certain exceptions apply, see exceptions_list for details.


    Args:
        master_query (dict): User specified query to be checked
        endpoint_list (list): A list of all current implemented endpoints
    """    
    #Combines all options together into a single list for faster checking
    all_enums_list = dictf.single_list_from_nested_dict_string_to_list(endpoint_field_enum_value("all"))
    
    #These fields are not checked due to thier more bespoke nature 
    #These will be validated by the API with may make error correction more difficult
    exceptions_list = ["query","granularity","usernames","max_results","pagination_token"]
    
    #Loops through the master query extracting each option from the dict
    for key_query,value_query in master_query.items():
        #logging.debug(f"Starting {key_query}")

        #Trys to split the option on commas and gives a warning if there are errors
        try:
            split_value_query = value_query.split(",")
        except: 
            logging.warning(f"Unable to validate {key_query} pleas ensure validity manually")
        #loops through the split options from the master query
        for enum_option in split_value_query:
            #checks the exception list and then if the current enum option is in
            # the list of all options

            if key_query not in exceptions_list  and enum_option not in all_enums_list :
                logging.error(f"{enum_option} is not a valid field for {key_query}")
                exit()
    
    #logging.debug("finished value_checker ")



def endpoint_checker(endpoint_list:list):
    """Checks that the supplied endpoints are ones this tool has integrated
    exits the script if this is not the case

    Args:
        endpoint_list (list): A list of all endpoints which have been integerated into this scrapping tool 
    """    
    for endpoint in endpoint_list:
        if endpoint not in endpoint_key_filtering_dict().keys():
            logging.error(f"{endpoint} is not a supported endpoint")
            exit()
        else:
            break

def validation_master(endpoint_list:list,master_query:dict):
    endpoint_checker(endpoint_list)
    key_validator(master_query)
    value_checker(master_query,endpoint_list)
    
