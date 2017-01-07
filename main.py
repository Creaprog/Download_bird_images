#!/usr/bin/python3
# coding: utf-8

import requests
import json
import os
import shutil
#import pdb; pdb.set_trace()

#Step 1
list_bird = open("birds.txt", "r")
buffer = list_bird.read()
my_array = buffer.splitlines()
list_bird.close()
list_links = open("links.txt", "w")
os.mkdir("images")

#Step 2
for i in range(len(my_array)) :
    obj = (requests.get('http://api.gbif.org/v1/species/match?verbose=true&kingdom=Plantae&name=' + my_array[i]).json())
    if "alternatives" in obj :
        for alternative in obj["alternatives"] :
            obj2 = requests.get('http://api.gbif.org/v1/species/{}/media'.format(alternative['usageKey'])).json()
            for results in obj2["results"] :
                if ("identifier" in results) :
                    print(results["identifier"])
                    list_links.write(results["identifier"] + "\n")
                    #Step 3
                    response = requests.get(results["identifier"], stream=True)
                    with open('images/' + my_array[i] + '.jpg', 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    del response
list_links.close()