#!/usr/bin/python2

import sys, re, os, json, urllib, urllib2
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TOPE, TPE1, TPE4, APIC, TCON, TLEN, COMM, TORY, WOAF, WOAR, error
from pprint import pprint

# Global vars
client_id = ""
downloaded = {}
download_dir = ""
PREF_FILENAME = "config.pref"
remix = False

def init():
    if not os.path.exists(PREF_FILENAME):
        print "Preferences file not found - attempting to create 'prefs' file..."
        try:
            with open(PREF_FILENAME,"w") as file:
                json.dump(generate_prefs('','',{}), file)
        except IOError:
            exit("ERROR: Unable to create preferences file (config.pref). Check user and file permissions and retry.")

        exit("Preferences file created. Please populate with soundcloud app client id and then restart program.")

    try:
        with open(PREF_FILENAME, "r") as file:
            data = json.load(file)
    except:
        exit("ERROR: Unable to load preferences file (config.pref). Please delete and re-run to generate template.")

    if len(data["client_id"]) == 0:
        exit("ERROR: Please update SoundCloud app client id in preferences file (config.pref) and retry.")

    global client_id
    global downloaded
    global download_dir

    client_id = data["client_id"]
    downloaded = data["downloaded"]
    download_dir = data["download_dir"]

    try:
        # create download directory
        if download_dir == "":
            download_dir = os.path.join(os.getcwd(),"downloads")
            if not os.path.isdir(download_dir):
                os.mkdir(download_dir)

        os.chdir(download_dir)
    except:
        exit("Error: unable to create download directory. Check permissions or update download directory in config file.")


def main():
    if len(sys.argv) < 3:
        exit("Usage: soundloader.py <user> <type>")

    original_dir = os.getcwd()
    init()

    global client_id
    global download_dir
    global downloaded

    print download_dir

    # get user
    user = sys.argv[1]
    # get type
    dl_type = sys.argv[2]

    if (user == dl_type == "clear"):
        print "Clearing downloaded list from preferences file"
        os.chdir(original_dir)
        try:
            with open(PREF_FILENAME,"w") as file:
                json.dump(generate_prefs(client_id,download_dir,{}), file)
        except IOError:
            exit("ERROR: Unable to clear downloaded list from preferences file (config.pref). Check user and file permissions and retry.")
        exit("Download list cleared!")

    if (dl_type != "favorites") and (dl_type != "tracks"):
        exit("Error invalid track list. Please enter valid track list and try again.")

    # generate soundcloud api
    soundcloud_api = "https://api.soundcloud.com/users/%s/%s?client_id=%s&limit=9999" % (user, dl_type, client_id)
    # soundcloud_api = "https://api.soundcloud.com/users/aosoon/tracks?client_id=c824cbcaae028929162ef98858b372de&limit=9999"

    print "URL to query:\n", soundcloud_api, "\n\nPreviously downloaded songs:"
    pprint(downloaded)
    print("")

    # downloads songs from api
    download(soundcloud_api)

    # update config file with newly downloaded tracks
    os.chdir(original_dir)
    try:
        with open(PREF_FILENAME,"w") as file:
            json.dump(generate_prefs(client_id,download_dir,downloaded), file)
    except IOError:
        exit("ERROR: Unable to update preferences file (config.pref). Check user and file permissions and retry.")

    print "Config file updated!"



def download(api):
    download_list = create_download_list(api)

    for key in download_list:
        download_track(download_list[key])

    if (len(download_list) > 0):
        print "\nDownloading completed!"
    else:
        print "\nNothing new to download from url!"


# generate list of downloadable tracks from api (skipping previously downloaded tracks)
def create_download_list(soundcloud_api):
    try:
        # open api URL for reading
        resp = urllib2.urlopen(soundcloud_api)
    except ValueError:
        # the user supplied URL is invalid or could not be retrieved
        exit("Error: The user '%s' can not be retrieved" % user)

    # store the contents (source) of our song's URL
    j = json.load(resp)

    download_list = {}

    for ele in j:
        if ele['kind'] == "track" and ele['permalink'] not in downloaded:
            download_list.update({ele['permalink']:ele})

    return download_list


# download track, update ID3 tag, add track to downloaded list
def download_track(track):
    global downloaded

    title = "%s.mp3" % track['title']
    title = title.replace('/', '-')
    path = download_dir

    # regular expression for the string we will search for in waveform-url tag
    regexp = 'https://w1.sndcdn.com/(.*?)_m.png'

    # find the song ID, if any
    match = re.search(regexp, track['waveform_url'])

    if match:
        # create a new stream hyperlink with the song ID
        url = "http://media.soundcloud.com/stream/%s" % match.group(1)
        print "Downloading File '%s'" % title
        try:
            urllib.urlretrieve(url, title)
        except IOError as e:
            print 'Connection to SoundCloud Failed, unable to download:\n ' + title + '\n continuing to next song'
        else:
            # update downloaded tracks list
            downloaded.update({track['permalink']:track['title']})

            audio = MP3(title, ID3=ID3)

            # add ID3 tag if it doesn't exist
            try:
                audio.add_tags()
            except error:
                pass

            audio.tags.add(
                TIT2(				# Title
                    encoding=3,
                    text=title[:-4]
                )
            )
            audio.tags.add(
                TOPE(				# Original Artist
                    encoding=3,
                    text=track['user']['username']
                )
            )
            audio.tags.add(
                TPE1(				# Lead Artist
                    encoding=3,
                    text=track['user']['username']
                )
            )
            # try to download track artwork
            if not track['artwork_url'] == None:
                try:
                    urllib.urlretrieve(track['artwork_url'],track['permalink'])
                except IOError as e:
                    print "Unable to download artwork for track '%s'." % title
                else:
                    audio.tags.add(
                        APIC(				# Cover photo
                            encoding=3, # 3 is for utf-8
                            mime='image/jpg', # image/jpeg or image/png
                            type=3, # 3 is for the cover image
                            desc=u'Cover',
                            data=open(track['permalink']).read()
                        )
                    )
            if remix:
                audio.tags.add(
                    TPE4(				# Remixer
                        encoding=3,
                        text=remixer(track)
                    )
                )
            audio.tags.add(
                TCON(				# Genre
                    encoding=3,
                    text=track['genre']
                )
            )
            audio.tags.add(
                TLEN(				# Track Duration
                    encoding=3,
                    text=str(track['duration'])
                )
            )
            audio.tags.add(
                COMM(				# User comments (soundcloud tags)
                    encoding=3,
                    lang=None,
                    desc=u'None',
                    text=track['tag_list']
                )
            )
            audio.tags.add(
                TORY(				# Year of Release
                    encoding=3,
                    text=str(track['release_year'])
                )
            )
            audio.tags.add(
                WOAF(				# File Info
                    url=track['permalink_url']
                )
            )
            audio.tags.add(
                WOAR(				# Artist Info
                    url=track['user']['permalink_url']
                )
            )

            audio.save()

            try:
                os.remove(track['permalink'])
            except OSError as e:
                print "WARNING: Failed to delete temporary cover art file (%s)" % track['permalink']

    else:
        print "No song ID found for the track '%s'. Skipping." % title

def generate_prefs(c_id, download_directory, downloaded_list):
    return {'client_id':c_id,'download_dir':download_directory,'downloaded':downloaded_list}

if __name__ == '__main__':
    main()
