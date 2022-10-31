import logging

def nested_dict_string_to_list(dictionary_initial:dict) ->dict:
    """Takes a dict with a dict nested inside of it which has strings as its values. 
        unpacks this and changes the string to a list of the words in the string with 
        a comma delimiter and rebuilds and returns the nested dict structure

    Args:
        dictionary_initial (dict): nested dictionary with strings at its second
        level values 

    Returns:
        dict: nested dict with 2 layers and a list of words as the value of the second layer
    """    
    dictionary_new={}
    for key, value in dictionary_initial.items():
            # subscript 2 indicated it is a nested part of the dict
            dictionary_new_2 ={}
            for key2, value2 in value.items():
                dictionary_new_2[key2] = str(value2).split(", ")
            dictionary_new[key] = dictionary_new_2

    return dictionary_new

def str_to_list_in_dict(dictionary:dict) ->dict:
    #Having this in the current format will slow the code down if it is called frequently. 
    #If this happens run once and create global variable as quick fix
    """intakes dictiory of strings and returns the a dict with the same keys but 
    strings are convert to lists 

    Returns:
        dict: dict with the strings broken into lists
    """
    dictionary_new ={}
    for key, value in dictionary.items():
        dictionary_new[key] = str(value).split(", ")
    return dictionary_new

def single_list_from_nested_dict_string_to_list(dictionary:dict) ->list:
    
    master_list=[]
    for key, value in dictionary.items():
            for key2, value2 in value.items():
                master_list = list(set(master_list+str(value2).split(", ")))

    return master_list