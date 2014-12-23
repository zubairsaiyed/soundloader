import urllib, urllib2, json, re
from pprint import pprint



try:
	json_data=open('prefs')
except:
	json_data=""

data = json.load(json_data)

if not data['client_id']:
	

pprint(data)
json_data.close()
