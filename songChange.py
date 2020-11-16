#!/usr/bin/python

# title          : songChange.py
# description    : Uses notify send for title artist and album cover
# author         : wdog666@gmail.com
# date           : 20201116
# version        : 0.2
# notes          : requires stagger
# python_version : 3.8.6
# =============================================================================

import os
import stagger


class CmusNotify:
    def __init__(self):
        self.get_filename_path()
        self.get_tags()
        self.extract_cover()
        self.notify(self.tags.title, self.tags.album,
                    self.tags.artist, self.icon)

    # +----------------------------+
    # | Extract Image from mp3 tag |
    # +----------------------------+

    def extract_cover(self):
        if (self.tags.picture):
            data = self.tags[stagger.id3.APIC][0].data
            self.icon = '/tmp/xyz.jpg'
            with open(self.icon, "wb") as outfile:
                outfile.write(data)
        else:
            self.icon = 'music'

    # +------------------------------+
    # | Get Object Tag from filepath |
    # +------------------------------+

    def get_tags(self):
        self.tags = stagger.read_tag(self.filepath)

    # +----------------------------------+
    # | Get Coplete path of current song |
    # +----------------------------------+

    def get_filename_path(self):
        cmd = "cmus-remote -Q|grep file|awk '{$1=\"\"; print $0}'"
        self.filepath = os.popen(cmd).read().strip()

    # +-------------------------+
    # | Call system notify-send |
    # +-------------------------+

    def notify(self, song, album, artist, icon='music'):
        command = f'''
        notify-send -i "{icon}" "🎶 {song}" \
        "\n<i>💿 {album}</i>\n<b>🕺 {artist}</b>"
'''
        os.system(command)


if __name__ == '__main__':
    CmusNotify()
