#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 18:22:46 2020

@author: wanghaojie
"""

import CrunchbaseAPI.CrunchbaseAPI as api
import sys

if __name__ == "__main__":

    try: 
    
        # test case
        mykey = '<YOUR_RAPIDAPI_KEY>'
        api.setup_key(mykey)
        orgs = 0
        people = 0
        
        def test1():
            """
            With multithreading:
            #CPU times: user 780 ms, sys: 92.2 ms, total: 873 ms
            #Wall time: 33.3 s

            Without multithreading: 
            #CPU times: user 778 ms, sys: 78 ms, total: 856 ms
            #Wall time: 2min 7s
            """
            global orgs, people
            
            api.org_pricing = {"updated_since": TransformTime(2020, 8, 9), "sort_order":"updated_at ASC"}
            org_properties = ['name','api_url']
            api.orgs = GetOrgData(org_pricing, org_properties)
        
            api.people_pricing = {"updated_since": TransformTime(2020, 8, 9), "location":"California"}
            people_properties = ['first_name','last_name']
            api.people = GetPeopleData(people_pricing, people_properties)
        
    
    except Exception as e:
        print("Major Exception ...Aborting")
        sys.exit(e)