
import json
import logging
import controller_2 as cont

logging.basicConfig(
    level=logging.DEBUG
)



#search_query = {"query":"#scotland #sunny -is:retweet","tweet.fields":"geo,created_at"}

# "search tweets", "tweet count","user lookup","tweet timeline","users liked tweets","tweets liking users",
#"user following"

endpoint_list = ["search tweets"]
#["tweet timeline","search tweets","tweet count"]

# Output options are currently 
# file -json dump to text file 
#table - returns pandas dataframe 
#csv combines results into csv and saves
output_types = ["csv","file"]

#"crypto,beincrypto,VitalikButerin,SatoshiLite,fluffypony,DailyCryptoCast,eth_classic,BittrexUS,cryptod0tnews,cnLedger"
#selbey
query = {"query":"cat #primeday","tweet.fields":"context_annotations,geo,created_at,public_metrics","granularity":"day",
"usernames":"DigitalRadish,SelbeyAnderson,GreentargetUK",
"user.fields":"username,description,created_at,entities,verified,public_metrics","max_results":100}

tweet_ID = []

#restart_token = "b26v89c19zqg8o3fpz2mvl3qh4bqcsfwwxejldr2o9ojh"
#restart_token ="b26v89c19zqg8o3fpz2mvl2ubdtkje5qasp0t9qv36fzx"

# Note - max overall returns must be greater than max results set within the query

max_overall_returns = 60

#Sets each endpoint user combination =  max overall/ (number of usernames * number of endpoints )
split_max_across_users =True

save_directory = "C:\\Users\\AndrewBeaton\\OneDrive - lumilinks.com\\Documents\\Twitter_scrapping_output\\"

def main() ->dict:
    
    results = cont.controller_master(endpoint_list,query,
                                    output_types,tweet_ID,
                                    max_overall_returns,
                                    split_max_across_users,
                                    save_dir=save_directory )

    return results
    

if __name__ == "__main__":
    final_res  = main()
    #print(type(inspect))
    #print(final_res)
