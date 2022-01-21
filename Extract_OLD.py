import requests
import os
import json
import pandas as pd

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    token = os.environ["BEARER_TOKEN"]
    r.headers["Authorization"] = f"Bearer {token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def get_list(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def id_list():
    list_req_url = "https://api.twitter.com/1.1/lists/members.json"
    parlListId = 864088912087715840
    query_params = {'list_id': '{}'.format(parlListId), 'count': '5000'}
    json_response = get_list(list_req_url, query_params)
    # extract the user IDs
    members = pd.DataFrame.from_dict(json_response['users'])
    user_ids = list(members['id'])
    return user_ids

# === user information requests

def create_headers():
    """
    create the request headers, includes the token
    """
    headers = {"Authorization": "Bearer {}".format(os.environ.get("BEARER_TOKEN"))}
    return headers

def connect_to_endpoint(url, headers):
    """
    connect to the API and return the json response
    """
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    headers = create_headers()
    json_response = connect_to_endpoint(search_url, headers)
    #return json.dumps(json_response, indent=4, sort_keys=True)
    return json_response

# get the current list of MPs
user_id_list = id_list()

# list to hold all of the json responses
aggregate_data = []

for user in user_id_list:
    # define which fields will be returned
    tweet_fields = 'created_at,author_id,conversation_id,in_reply_to_user_id,referenced_tweets,text,public_metrics,context_annotations'
    user_fields = 'username,created_at,public_metrics,verified,url'
    expansions = 'author_id'
    max_results = '30'
    
    # the user request url
    search_url = "https://api.twitter.com/2/users/{}/tweets?expansions={}&tweet.fields={}&user.fields={}&max_results={}".format(user,expansions,tweet_fields,user_fields,max_results)

    print(search_url)
    response = main()
    
    aggregate_data.append(response)
    
import pickle

# pickle the response for now - this will turn into a file sent to an S3 bucket
with open('mptweetspickle', 'wb') as fp:
    pickle.dump(aggregate_data, fp)