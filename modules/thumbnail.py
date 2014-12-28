from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, error

audio = MP3('example.mp3', ID3=ID3)

# add ID3 tag if it doesn't exist
try:
    audio.add_tags()
except error:
    pass

audio.tags.add(
    APIC(
        encoding=3, # 3 is for utf-8
        mime='image/jpg', # image/jpeg or image/png
        type=3, # 3 is for the cover image
        desc=u'Cover',
        data=open('example.jpg').read()
    )
)
audio.tags.add(
    TIT2(
        encoding=3,
        text="testTitle"
    )
)
audio.save()
