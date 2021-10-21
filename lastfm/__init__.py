#!/usr/bin/env python3

# import sys
import pylast
import time
import datetime
import logging
import sys


class LFM:
    """last fm connection"""
    def __init__(self, settings):
        self.network = None
        self.settings = settings
        try:
            self.connect()
        except ConnectionError as err:
            sys.exit(err)

        self.track = None
        self.artist = None

    def set_track(self, track):
        self.track = track

    def set_artist(self, artist):
        self.artist = artist

    # +----------------------+
    # | Connection to lastFM |
    # +----------------------+

    def connect(self):

        try:
            if hasattr(self.settings, 'key') and hasattr(self.settings, 'secret') and \
               hasattr(self.settings, 'username') and hasattr(self.settings, 'password'):

                password_hash = pylast.md5(self.settings.password)
                opts = {'api_key': self.settings.key,
                        'api_secret': self.settings.secret,
                        'username': self.settings.username,
                        'password_hash': password_hash}
            self.network = pylast.LastFMNetwork(**opts)
        except Exception:
            raise ConnectionError('Connection Error')

    # +----------+
    # | SCROBBLE |
    # +----------+

    def scrobble(self, artist, track):
        # Get UNIX timestamp
        unix_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))

        try:
            self.network.scrobble(artist=artist,
                                  title=track,
                                  timestamp=unix_timestamp)
        except Exception as e:
            logging.critical(str(e))
            sys.exit('no scrobble')

    # +-----------------------+
    # | Get Cover from lastfm |
    # +-----------------------+

    def get_cover(self, artist, album):
        album = self.network.get_album(artist, album)
        return album.get_cover_image(2)
