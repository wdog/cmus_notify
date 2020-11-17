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
import sys
import stagger
import requests
import argparse
from lastfm import LFM


" TODO "
" write cover in folder only if not exists "


class CmusNotify:

    filepath = None
    tags = None
    icon = None
    default_icon = 'music'

    # +------+
    # | init |
    # +------+

    def __init__(self, option):

        if not self.is_running():
            sys.exit()

        self.enableScroble = option.scrobbing
        self.enableLastFm = option.lastFm

        self.get_filename_path()

        self.get_tags()

        if (self.enableLastFm):
            self.lfm = LFM()

        self.extract_cover()

        self.notify(self.tags.title, self.tags.album,
                    self.tags.artist, self.icon)

        " scrobble lastfm "
        if (self.enableLastFm and self.enableScroble):
            LFM().scrobble(self.tags.artist, self.tags.title)

    # +--------------------+
    # | Write Icon to file |
    # +--------------------+

    def write_icon(self, icon_file, source):
        with open(icon_file, "wb") as outfile:
            outfile.write(source)

    # +--------------------+
    # | Get Icon from tags |
    # +--------------------+

    def get_cover_from_tag(self):
        if (self.tags.picture):
            self.icon = os.path.join(self.album_path, "album.jpg")
            data = self.tags[stagger.id3.APIC][0].data
            self.write_icon(self.icon, data)

    # +----------------------+
    # | Get Icon from Folder |
    # +----------------------+

    def get_cover_from_folder(self):
        albums = ['album.jpg', 'folder.jpg', 'folder.jpg']
        for album in albums:
            filealbum = os.path.join(self.album_path, album)
            if os.path.isfile(filealbum):
                self.icon = filealbum
                break

    # +----------------------+
    # | Get Icon From LastFM |
    # +----------------------+

    def get_cover_from_lastfm(self):
        try:
            url = self.lfm.get_cover(self.tags.artist,
                                     self.tags.album)
            r = requests.get(url)
            self.icon = os.path.join(self.album_path, "album.jpg")
            self.write_icon(self.icon, r.content)
            print('got from lastFM')

        except Exception:
            pass

    # +----------------------------+
    # | Extract Image from mp3 tag |
    # +----------------------------+

    def extract_cover(self):

        """
        1) get image from folder (cover.jpg or album.jpg ...)
        2) get image from tag -> save to album folder
        3) get from lasastfm -> save to album folder
        4) default image
        """

        self.get_cover_from_folder()

        if self.icon is None:
            self.get_cover_from_tag()

        if self.icon is None and self.enableLastFm and self.enableScroble:
            self.get_cover_from_lastfm()

        if self.icon is None:
            self.icon = self.default_icon

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
        self.album_path = os.path.dirname(self.filepath)

    # +--------------------------+
    # | Check is Cmus is running |
    # +--------------------------+

    def is_running(self):
        cmd = "cmus-remote -C status |grep status | awk '{print $2}' "
        self.is_running = os.popen(cmd).read().strip()

        if self.is_running == 'playing':
            return True
        return False

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lastFm',
                        help='Enable LastFm cover',
                        action='store_true')
    parser.add_argument('-s', '--scrobbing',
                        help='Enable LastFm scrobbing',
                        action='store_true')
    args = parser.parse_args()
    CmusNotify(args)
