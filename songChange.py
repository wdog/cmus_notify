#!/usr/bin/env python3

# title          : songChange.py
# description    : Uses notify send for title artist and album cover
# author         : wdog666@gmail.com
# date           : 20201116
# version        : 0.3
# notes          : requires stagger, pylast
# python_version : 3.8.6
# =============================================================================

import os
import sys
import stagger
import requests
import argparse
from lastfm import LFM
import logging


" TODO "
" write cover in folder only if not exists "


class CmusNotify():

    # +------+
    # | init |
    # +------+

    def __init__(self, option):

        logging.info('INIT')
        logging.info(option)
        self.filepath = None
        self.tags = None
        self.icon = None
        self.default_icon = 'music'

        if not self.is_running():
            sys.exit('not running')

        logging.info('running')

        self.enableScrobble = option.scrobbing
        self.enableLastFm = option.lastfm

        logging.info('get_filename_path')
        self.get_filename_path()

        logging.info('get_tags')
        self.get_tags()

        if (self.enableLastFm):
            logging.info('enableLastFm')
            self.lfm = LFM()

        logging.info('extract_cover')
        self.extract_cover()

        " scrobble lastfm "
        if (self.enableLastFm and self.enableScrobble):
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

        if self.icon is None and self.enableLastFm and self.enableScrobble:
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
        r = os.popen(cmd).read().strip()

        if r == 'playing':
            return True
        return False

    # +-------------------------+
    # | Call system notify-send |
    # +-------------------------+

    def notify(self):
        command = f'''
        notify-send -i "{self.icon}" "🎶 {self.tags.title}" \
        "\n<i>💿 {self.tags.album}</i>\n<b>🕺 {self.tags.artist}</b>"
'''
        os.system(command)


if __name__ == '__main__':
    # script_path = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename="/tmp/app.log", format='%(asctime)s - %(name)s - '
                        '%(levelname)s: %(message)s', datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lastfm',
                        help='Enable LastFm cover',
                        action='store_true')
    parser.add_argument('-s', '--scrobbing',
                        help='Enable LastFm scrobbing',
                        action='store_true')
    args = parser.parse_args()
    cmn = CmusNotify(args)
    cmn.notify()
