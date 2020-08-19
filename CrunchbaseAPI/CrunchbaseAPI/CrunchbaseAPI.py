# basic setup
import json
import requests
import pandas as pd
from datetime import datetime, date, time, timedelta, timezone
from concurrent import futures

_RAPIDAPI_KEY = ""

_MAX_WORKERS = 20 # for multithreading

# functions
def setup_key(MyKey):
    """
    Set the RAPIDAPI_KEY to user's own key
    """
    global _RAPIDAPI_KEY
    _RAPIDAPI_KEY = MyKey
    

# The request function 
def _trigger_organization_api(pricing):
    """
    trigger an organization api to get data
    """
        
    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': _RAPIDAPI_KEY
          }
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"
    
    response = requests.request("GET", url, headers=headers, params=pricing)
      
    if(200 == response.status_code):
      return json.loads(response.text)
    else:
      return None

def _trigger_people_api(pricing):
    """
    trigger an people api to get data
    """
    
    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': _RAPIDAPI_KEY
          }
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"
      
    response = requests.request("GET", url, headers=headers, params=pricing)
      
    if(200 == response.status_code):
      return json.loads(response.text)
    else:
      return None


def _get_org_pages(pricing):
    return _trigger_organization_api(pricing)['data']['paging']['number_of_pages']

def _get_people_pages(pricing):
    return _trigger_people_api(pricing)['data']['paging']['number_of_pages']


def _org_one_page(tup):
    pricing, properties, k = tup
    pricing['page'] = k
    
    api_response = _trigger_organization_api(pricing)
    
    res = []
    for org in api_response['data']['items']:
        res.append([org['properties'][property] for property in properties ])
    
    res = pd.DataFrame(res,columns = properties)
    return (k,res) 

def _people_one_page(tup):
    pricing, properties, k = tup
    pricing['page'] = k
    
    api_response = _trigger_people_api(pricing)
    
    res = []
    for people in api_response['data']['items']:
        res.append([people['properties'][property] for property in properties ])
    
    res = pd.DataFrame(res,columns = properties)
    return (k,res) 


def GetOrgData(pricing: dict, properties: list) ->pd.DataFrame:
    """
    Get organization data. 
    
    param pricing: optional parameters passed to get data
    pricing = {
    updated_since = , :number(timestamp) (When provided, restricts the result set to Organizations where updated_at >= the passed value)
    query = , :string (Full text search of an Organization's name, aliases (i.e. previous names or "also known as"), and short description)
    name = , :string (Full text search limited to name and aliases)
    domain_name = , :string (Text search of an Organization's domain_name (e.g. www.google.com))
    locations = , :string (Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco)
    organization_types = , :string (Filter by one or more types. Multiple types are separated by commas. Available types are "company", "investor", "school", and "group". Multiple organization_types are logically AND'd.)
    sort_order = , :string (The sort order of the collection. Options are "created_at ASC", "created_at DESC", "updated_at ASC", and "updated_at DESC")
    }
    
    param properties: properties of organizations users want to get
    properties = [
    "permalink"
    "api_path"
    "web_path"
    "api_url"
    "name"
    "stock_exchange"
    "stock_symbol"
    "primary_role"
    "short_description"
    "profile_image_url"
    "domain"
    "homepage_url"
    "facebook_url"
    "twitter_url"
    "linkedin_url"
    "city_name"
    "region_name"
    "country_code"
    "created_at"
    "updated_at"
    ]
    """
    
    pages = _get_org_pages(pricing) # get the number of pages we need to go through
    
    workers = min(_MAX_WORKERS,pages) # multithreading
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(_org_one_page, ((pricing, properties, i+1) for i in range(pages)) )

    result = sorted(list(res),key=lambda x: x[0]) # sort by the pages 
    
    page_results = [res[1] for res in result] # get a list of page-data
    
    return pd.concat(page_results,axis=0)   # return a Dataframe


def GetPeopleData(pricing: dict, properties: list) ->pd.DataFrame:
    """
    Get people data. 
    
    param pricing: optional parameters passed to get data
    pricing = {
    name = , :string (A full-text query of name only)
    query = , :string (A full-text query of name, title, and company)
    updated_since = , :number(timestamp) (When provided, restricts the result set to People where updated_at >= the passed value)
    sort_order = , :string (The sort order of the collection. Options are "created_at ASC", "created_at DESC", "updated_at ASC", and "updated_at DESC")
    locations = , :string (Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco)
    socials = , :string (Filter by social media identity (comma separated, AND'd together) e.g. socials=ronconway)
    types = , :string (Filter by type (currently, either this is empty, or is simply "investor"))
    }
    
    param properties: properties of organizations users want to get
    properties = [
    "permalink"
    "api_path"
    "web_path"
    "api_url"
    "first_name"
    "last_name"
    "gender"
    "title"
    "organization_permalink"
    "organization_api_path"
    "organization_web_path"
    "organization_name"
    "profile_image_url"
    "homepage_url"
    "facebook_url"
    "twitter_url"
    "linkedin_url"
    "city_name"
    "region_name"
    "country_code"
    "created_at"
    "updated_at"
    ]
    """
    
    pages = _get_people_pages(pricing) # get the number of pages we need to go through
    
    workers = min(_MAX_WORKERS,pages) # multithreading        
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(_people_one_page, ((pricing, properties, i+1) for i in range(pages)) )

    result = sorted(list(res),key=lambda x: x[0]) # sort by the pages 
    
    page_results = [res[1] for res in result] # get a list of page-data
    
    return pd.concat(page_results,axis=0)   # return a Dataframe


def TransformTime(year, month, day, time_zone = timezone.utc):
    """
    This function helps to transform a time into int(timestamp)
    """
    
    return int( datetime(year = year, month=month, day=day).replace(tzinfo=timezone.utc).timestamp() )

