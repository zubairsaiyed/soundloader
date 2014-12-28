import urllib, urllib2, json, re, os
from pprint import pprint

client_id = ""
downloads = {}
PREF_TEMPLATE = {"client_id":client_id,"downloads":downloads}
PREF_FILENAME = "config.pref"

if not os.path.exists(PREF_FILENAME):
	file = open(PREF_FILENAME,"w")
	json.dump(PREF_TEMPLATE, file)
	file.close();

try:
	json_data=open(PREF_FILENAME)
except:
	json_data=""

data = json.load(json_data)
json_data.close()

pprint(data)

data["client_id"] = "test_client"
data["downloads"]["testId"] = "testTitle"
data["downloads"]["anotherTestId"] = "anotherTestTitle"

pprint(data)

# del data["downloads"]["testId"]

pprint(data)

if "testId" in data["downloads"]:
	print "found 'testId'!"
else:
	print "did not find 'testId'!"

PREF_TEMPLATE = {"client_id":data['client_id'],"downloads":data['downloads']}
file = open(PREF_FILENAME,"w")
json.dump(PREF_TEMPLATE, file)
file.close();


def generate_prefs():
	print "hello"
