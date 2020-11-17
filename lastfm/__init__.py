#!/usr/bin/env python3

# import sys
import pylast
import time
import datetime
import json
from collections import namedtuple
import logging
import os


class LFM:
    """last fm connection"""
    def __init__(self):
        self.get_settings()
        logging.info('connected')
        self.connect()
        logging.info('connected')
        self.track = None
        self.artist = None

    def set_track(self, track):
        self.track = track

    def set_artist(self, artist):
        self.artist = artist

    # +----------------------------------------+
    # | Convert Json to Object - hook function |
    # +----------------------------------------+

    def cSecretsDecoder(self, secretsDict):
        return namedtuple('X', secretsDict.keys())(*secretsDict.values())

    # +-----------------------------------+
    # | Read JSON String with credentials |
    # +-----------------------------------+

    def get_settings(self):
        logging.info('connected')
        try:

            script_path = os.path.dirname(os.path.realpath(__file__))
            secret = os.path.join(script_path, "../secret.json")
            with open(secret, 'r') as fi:
                self.settings = json.loads(fi.read(),
                                           object_hook=self.cSecretsDecoder)
        except Exception as e:
            logging.info(str(e))

    def connect(self):
        password_hash = pylast.md5(self.settings.password)

        self.network = pylast.LastFMNetwork(api_key=self.settings.key,
                                            api_secret=self.settings.secret,
                                            username=self.settings.username,
                                            password_hash=password_hash)

    def scrobble(self, artist, track):
        # Get UNIX timestamp
        unix_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        self.network.scrobble(artist=artist,
                              title=track,
                              timestamp=unix_timestamp)

        # Confirm
        # print("Confirmation from Last.fm:")
        # recent_tracks = self.network.get_user(self.settings.username) \
        # .get_recent_tracks(limit=1)
        # print(recent_tracks)

    def get_cover(self, artist, album):
        album = self.network.get_album(artist, album)
        # wiki test
        # wiki = album.get_wiki_summary()
        # print(wiki)
        return album.get_cover_image(2)
