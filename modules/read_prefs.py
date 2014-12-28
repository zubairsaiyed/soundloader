import urllib, urllib2, json, re, os
from pprint import pprint

PREF_FILENAME = "config.pref"
PREF_TEMPLATE = {"client_id":"","downloads":{}}

if not os.path.exists(PREF_FILENAME):
	print "Preferences file not found. Attempting to create 'prefs' file."
	try:
		file = open(PREF_FILENAME,"w")
		json.dump(PREF_TEMPLATE, file)
		file.close();
		exit("Preferences file created. Please populate with soundcloud app client id and then restart program.")
	except:
		exit("Unable to create preferences (pref) file. Check user and file permissions and retry.")

try:
	json_data=open(PREF_FILENAME)
	data = json.load(json_data)
	json_data.close()
except:
	exit("Error reading preferences file")

if len(data["client_id"]) == 0:
	exit("Please update SoundCloud app client id in preferences (prefs) file and retry.")

client_id = data["client_id"]
