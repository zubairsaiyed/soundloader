import urllib, urllib2, json, re

soundcloud_api = "https://api.soundcloud.com/users/zubair-saiyed/favorites?client_id=c824cbcaae028929162ef98858b372de&limit=9999"

try:
	# open api URL for reading
	resp = urllib2.urlopen(soundcloud_api)
except ValueError:
	# the user supplied URL is invalid or could not be retrieved
	exit("Error: The user '%s' can not be retrieved" % user)

# store the contents (source) of our song's URL
j = json.load(resp)

for ele in j:
	print "%s\t\t%s" %(ele['kind'], ele['title'])

	
