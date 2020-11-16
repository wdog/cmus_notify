#!/usr/bin/python

# title          :songChange.py
# description    :Uses notify send for title artist and album cover
# author         :wdog666@gmail.com
# date           :20201115
# version        :0.1
# usage          :insert into rc file:
#                :set status_display_program=~/.config/cmus/songChange.py

# notes          : requires stagger
# python_version :3.8.6
# =============================================================================

import os
import stagger


# +-------------------+
# | Send notification |
# +-------------------+


def notify(song, album, artist, icon='music'):
    command = f'''
    notify-send -i "{icon}" "🎶 {song}" "<i>💿 {album}</i>\n<b>🕺 {artist}</b>"
'''
    os.system(command)


# +-----------------------------------------------+
# | Extract Images to display from TAG if present |
# +-----------------------------------------------+


def get_cover(mp3):
    if (mp3.picture):
        data = mp3[stagger.id3.APIC][0].data
        icon = '/tmp/xyz.jpg'
        with open(icon, "wb") as outfile:
            outfile.write(data)
    else:
        " default icon "
        icon = 'music'
    return icon


# +---------------+
# | Main function |
# +---------------+

def main(filename):
    mp3 = stagger.read_tag(filename)

    icon = get_cover(mp3)
    notify(mp3.title, mp3.album, mp3.artist, icon)


# +--------------------------------------------------------------+
# | Retrieve filepath of current playing file using cmus-remote  |
# +--------------------------------------------------------------+


def get_filename():
    cmd = "cmus-remote -Q|grep file|awk '{$1=\"\"; print $0}'"
    filename = os.popen(cmd).read().strip()
    return filename

# +-----+
# | RUN |
# +-----+


if __name__ == '__main__':
    main(get_filename())
