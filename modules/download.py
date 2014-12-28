import urllib, urllib2, json, re, os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TOPE, TPE1, TPE4, APIC, TCON, TLEN, COMM, TORY, WOAF, WOAR, error

downloaded = {}
remix = False

def main():
    soundcloud_api = "https://api.soundcloud.com/users/aosoon/tracks?client_id=c824cbcaae028929162ef98858b372de&limit=9999"
    download_list = create_download_list(soundcloud_api)

    for key in download_list:
        download_track(download_list[key])

    print "\nDownloading completed!"

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


def download_track(track):
    title = "%s.mp3" % track['title']
    title = title.replace('/', '-')

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
            downloaded.update({track['permalink']:title})

            #print track['artwork_url'],track['id']

            # try to download track artwork
            try:
                urllib.urlretrieve(track['artwork_url'],track['permalink'])
            except IOError as e:
                print "Unable to download artwork for track '%s'." % title
            else:
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
                if remix:
                    audio.tags.add(
                        TPE4(				# Remixer
                            encoding=3,
                            text=remixer(track)
                        )
                    )
                audio.tags.add(
                    APIC(				# Cover photo
                        encoding=3, # 3 is for utf-8
                        mime='image/jpg', # image/jpeg or image/png
                        type=3, # 3 is for the cover image
                        desc=u'Cover',
                        data=open(track['permalink']).read()
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
                        text=track['release_year']
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
                    print "WARNING: Failed to delete temporary cover art file (%s)" % track['permalinkpython ']

    else:
        print "No song ID found for the track '%s'. Skipping." % title


if __name__ == '__main__':
    main()
