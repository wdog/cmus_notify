#!/usr/bin/env python3

# import sys
import pylast
import time
import datetime


class LFM:
    """last fm connection"""
    def __init__(self, settings):
        self.settings = settings
        self.connect()
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

    def get_cover(self, artist, album):
        album = self.network.get_album(artist, album)
        return album.get_cover_image(2)
