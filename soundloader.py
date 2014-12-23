#!/usr/bin/python2

import sys, re, urllib, urllib2

if len(sys.argv) < 2:
    exit("Usage: soundloader.py <user> <type> <client_id>")

def main():
    # get user
    user = sys.argv[1]

    # get type
    dl_type = sys.argv[2]

    if dl_type != "favorites":
        dl_type = "tracks"

    # get client_id
    client_id = sys.argv[-1]

    # get soundcloud api
	soundcloud_api = "https://api.soundcloud.com/users/%s/%s?client_id=%s&limit=9999" % (user, type, client_id)

    try:
        xml =

if __name__ == '__main__':
    main()
