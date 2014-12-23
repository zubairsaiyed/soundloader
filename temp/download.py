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

title = "%s.mp3" % j[0]['title']
title = title.replace('/', '-')

# regular expression for the string we will search for in waveform-url tag
regexp = 'https://w1.sndcdn.com/(.*?)_m.png'

# find the song ID, if any
match = re.search(regexp, j[0]['waveform_url'])

if match:
    # create a new stream hyperlink with the song ID
    url = "http://media.soundcloud.com/stream/%s" % match.group(1)
else:
    print "No song ID found for the %s user. Exiting." % sys.argv[1]
    sys.exit()

print "Downloading File '%s'" % title
try:
    urllib.urlretrieve(url, title)
except IOError as e:
    print 'Connection to SoundCloud Failed, unable to download:\n '+title+'\n continuing to next song'


#urllib.urlretrieve('http://media.soundcloud.com/stream/CMpxiekOu2O3', "song.mp3")
