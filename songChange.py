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
import json
from collections import namedtuple
from lastfm import LFM
import logging


" TODO "
" write cover in folder only if not exists "


class CmusNotify():

    # +------+
    # | init |
    # +------+

    def __init__(self, option):

        #  is cmus playing?
        if not self.is_cmus_playing():
            sys.exit('not playing')

        self.file_path = None
        self.tags = None
        self.icon = None
        # default icon
        self.default_icon = 'music'
        # lastfm options
        self.enableScrobble = option.scrobbing
        self.enableLastFm = option.lastfm

        # get mp3 track file path
        self.get_file_path()

        # extract tags from file
        self.get_tags()

        # lastfm connect if requested
        if (self.enableLastFm):
            self.get_lastfm_settings()
            self.lfm = LFM(self.lastfm_settings)

        # get cover from various sources
        self.extract_cover()

        # scrobble lastfm is requested
        if (self.enableLastFm and self.enableScrobble):
            self.lfm.scrobble(self.tags.artist, self.tags.title)

    # +----------------------------------------+
    # | Convert Json to Object - hook function |
    # +----------------------------------------+

    def cSecretsDecoder(self, secretsDict):
        return namedtuple('LastFMSettings', secretsDict.keys())(*secretsDict.values())

    # +-------------------------------------------+
    # | Get lastFm settings from secret.json file |
    # +-------------------------------------------+

    def get_lastfm_settings(self):
        try:
            secret_file = "secret.json"
            secret_path = os.path.dirname(os.path.realpath(__file__))

            secret = os.path.join(secret_path, secret_file)
            with open(secret, 'r') as fi:
                self.lastfm_settings = json.loads(fi.read(),
                                                  object_hook=self.cSecretsDecoder)
        except Exception as e:
            logging.critical(str(e))
            sys.exit('no credential')

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
        print("searching in tags")
        if (self.tags.picture):
            self.icon = os.path.join(self.album_path, "album.jpg")
            data = self.tags[stagger.id3.APIC][0].data
            self.write_icon(self.icon, data)

    # +----------------------+
    # | Get Icon from Folder |
    # +----------------------+

    def get_cover_from_folder(self):
        print("searching in folder")
        possible_files = ['album.jpg', 'folder.jpg', 'cover.jpg']
        for possible_file in possible_files:
            file_cover = os.path.join(self.album_path, possible_file)
            # file exist?
            if os.path.isfile(file_cover):
                # first wins
                self.icon = file_cover
                print("found in folder " + self.icon)
                break

    # +----------------------+
    # | Get Icon From LastFM |
    # +----------------------+

    def get_cover_from_lastfm(self):
        print("searching from lastfm")
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

        print("using: " + self.icon)
    # +------------------------------+
    # | Get Object Tag from filepath |
    # +------------------------------+

    def get_tags(self):
        self.tags = stagger.read_tag(self.file_path)

    # +----------------------------------+
    # | Get Coplete path of current song |
    # +----------------------------------+

    def get_file_path(self):
        cmd = "cmus-remote -Q|grep file|awk '{$1=\"\"; print $0}'"
        self.file_path = os.popen(cmd).read().strip()
        self.album_path = os.path.dirname(self.file_path)

    # +--------------------------+
    # | Check is Cmus is playing |
    # +--------------------------+

    def is_cmus_playing(self):
        cmd = "cmus-remote -C status |grep status | awk '{print $2}' "
        r = os.popen(cmd).read().strip()

        if r == 'playing':
            return True
        return False

    # +-------------------------+
    # | Call system notify-send |
    # +-------------------------+

    def notify(self):
        print("notify with: " + self.icon)
        command = f'''
        notify-send -i \"{self.icon}\" "{self.tags.title}" \
        "<i>{self.tags.album}</i>\n<b>{self.tags.artist}</b>"
'''
        os.system(command)

# +------+
# | RUN  |
# +------+


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

    if (args.scrobbing and not args.lastfm):
        sys.exit('Scrobbling -s requires LastFM -l')

    cmn = CmusNotify(args)
    cmn.notify()
