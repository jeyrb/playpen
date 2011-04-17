#!/usr/bin/env python

from appscript import app
import unittest
import hashlib

class PossibleDuplicate:
    def __init__(self, track_a, track_b):
        self.track_a = track_a
        self.track_b = track_b

    def match(self):
        return self._file_hash(self.track_a) == self._file_hash(self.track_b)

    def _file_hash(self, track):
        h = hashlib.sha1()
        path = track.location().path
        f = open(path, 'rb')
        h.update(f.read())
        f.close()
        d = h.hexdigest()
        return d

def find_tracks():

    iTunes = app('iTunes')
    library = iTunes.library_playlists['Library']
    stash = {}
    dups = []
    for t in library.file_tracks():
        key = (t.duration(), t.size())
        if key in stash:
            dup = stash[key]
            try:
                print "Possible Duplicate %s(%d,%d) and %s (%d,%d)" % (
                t.name(), t.size(), t.duration(), dup.name(), dup.size(), dup.duration())
            except TypeError:
                print "Type failure for %s" % t.name()
            dups.append(PossibleDuplicate(dup, t))
        else:
            stash[key] = t

    for d in dups:
        if d.match():
            print "A: %s %s %s" % (d.track_a.id(), d.track_a.location(), d.track_a.database_ID())
            print "B: %s %s %s" % (d.track_b.id(), d.track_b.location(), d.track_b.database_ID())


class JeyTunesTest(unittest.TestCase):
    def test_list(self):
        find_tracks()

