soundloader
===========

##Overview
Is a Python script to test downloading of a user's SoundCloud tracks or favorites. Also maintains a memory of already downloaded tracks to prevent duplicate downloads.

Special thanks to the developers of [Soundcloud-Downloader](https://github.com/oziks/Soundcloud-Downloader) for demonstrating use of SoundCloud API for downloading.

##Requirements
Must have [Mutagen](https://bitbucket.org/lazka/mutagen) python module installed (for proper MP3/ID3 tagging).

##Usage

Must update *config.pref* with SoundCloud API **client id** (and optionally a download directory) before running.

If a download directory is not specified, tracks will be saved in a sub-directory of the working directory called "downloads"

```python
python soundloader.py <soundcloud_user> <track_type>
```

+ *track_type* must be 'tracks' (uploads) or 'favorites' (likes)
+ if 'clear' is entered in place of both *user* and *track_type*, the maintained 'downloaded' list of tracks will be cleared.

##Future Work (Todo)
- update downloaded list as each file is downloaded

- remove files from downloaded list if download fails

- use user artwork if track artwork fails to download
- do not try to remove temporary image file if no image was downloaded

- multi-thread downloads
