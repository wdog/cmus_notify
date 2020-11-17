#!/bin/env python3

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
import requests
from lastfm import LFM


" TODO "
" write cover in folder only if not exists "


class CmusNotify:
    def __init__(self):
        self.get_filename_path()
        self.get_tags()
        self.lfm = LFM()
        self.extract_cover()

        self.notify(self.tags.title, self.tags.album,
                    self.tags.artist, self.icon)

        " scrobble lastfm "
        r = LFM().scrobble(self.tags.artist, self.tags.title)
        print(r)

    def write_icon(self, source):
        with open(self.icon, "wb") as outfile:
            outfile.write(source)

    # +----------------------------+
    # | Extract Image from mp3 tag |
    # +----------------------------+

    def extract_cover(self):

        """
        1) get image from tag
        2) get image from folder (cover.jpg or album.jpg or ???)
        3) get from lasastfm
        4) default image
        """

        tmp_image = '/tmp/xyz.jpg'

        if (self.tags.picture):
            data = self.tags[stagger.id3.APIC][0].data
            self.icon = tmp_image
            self.write_icon(data)
        else:
            self.icon = 'music'

        self.icon = 'music'
        if (self.icon == 'music'):
            try:
                url = self.lfm.get_cover(self.tags.artist,
                                         self.tags.album)
                r = requests.get(url)
                self.icon = tmp_image
                " TODO md5 of current file - do not download again "
                print('lastFm cover')
                self.write_icon(r.content)

            except Exception as e:
                print(e)
                pass

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
