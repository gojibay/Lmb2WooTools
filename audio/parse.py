#!/usr/bin/python 


import json
from pprint import pprint

with open('brands.json') as data_file:    
    data = json.load(data_file)


for elt in data:
	print(str(elt['id']) + " : " + str(elt['name'])  + ',')

