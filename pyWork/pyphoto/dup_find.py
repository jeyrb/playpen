#!/usr/bin/env python

"""Detect duplicate photos in an iPhoto library, using SHA1 hashes to determine equality
"""

import appscript
import os.path
import unittest
import hashlib
import os
import shutil
import os.path


__author__ = 'jey'

class HashCache(object):
    cachedir = '/tmp/iphotoduphashcache'

    def __init__(self):
        if not os.path.exists(HashCache.cachedir):
            os.makedirs(HashCache.cachedir)

    def clean(self):
        if os.path.exists(HashCache.cachedir):
            print "Cleaning %d entries from cache " % self.len()
            shutil.rmtree(HashCache.cachedir)
            os.makedirs(HashCache.cachedir)

    def __setitem__(self, key, value):
        file = self._cachefile(key)
        f = open(file, 'w')
        f.write(value)
        f.close()

    def __contains__(self, item):
        file = self._cachefile(item)
        if os.path.exists(file):
            return True
        else:
            return False

    def __getitem__(self, key):
        file = self._cachefile(key)
        if os.path.exists(file):
            f = open(file, "r")
            hash = f.read()
            f.close()
            return hash
        else:
            return None

    def __len__(self):
        return len([name for name in os.listdir(HashCache.cachedir) if os.path.isfile(name)])

    def _cachefile(self, id):
        return os.path.join(HashCache.cachedir, id)


class HashedPhoto(object):
    def __init__(self, album, id, image_path, cache):
        self.id = id
        self._album = album
        self.key = str(id)
        self._image_path = image_path
        self._size = None
        self._cache = cache

    def _checksum(self, st):
        return reduce(lambda x, y:x + y, map(ord, st))

    @property
    def fingerprint(self):
        if self.key in self._cache:
            phash = self._cache[self.key]
            print "Reusing cached hash for %d" % self.id
        else:
            print "Generating hash for %d" % self.id
            f = open(self.image_path, 'rb')
            h = hashlib.sha1()
            h.update(f.read())
            phash = h.hexdigest()
            f.close()
            self._cache[self.key] = phash
        return phash

    @property
    def size(self):
        if self._size == None:
            self._size = os.path.getsize(self.image_path)
        return self._size

    @property
    def image_path(self):
        if self._image_path == None:
            self._image_path = self._album.photos.ID(self.id).image_path()
        return self._image_path

    @property
    def name(self):
        return self._album.photos.ID(self.id).name()

    @property
    def height(self):
        return self._album.photos.ID(self.id).height()

    @property
    def width(self):
        return self._album.photos.ID(self.id).width()

    @property
    def date(self):
        return self._album.photos.ID(self.id).date()


class DupFinder(object):
    def __init__(self, iPhoto, reporter):
        self._cache = HashCache()
        self._app = iPhoto
        self._reporter = reporter

    def clean(self):
        self._cache.clean()

    def find_dups(self):
        self._reporter.Report("Connecting to iPhoto")

        self._reporter.Report("Retrieving photo list from iPhoto")
        album = self._app.photo_library_album()

        filesizes = {}
        image_paths = album.photos.image_path.get()
        ids = album.photos.id.get()

        self._reporter.Target(len(ids))
        self._reporter.Report("Scanning %d photos supplied by iPhoto" % len(ids))

        for n in range(len(ids)):
            hp = HashedPhoto(album, ids[n], image_paths[n], self._cache)
            if hp.size not in filesizes:
                filesizes[hp.size] = []

            for prior in filesizes[hp.size]:
                if prior.fingerprint == hp.fingerprint:
                    print "Duplicate photo A (%s) %s %s" % (prior.id, prior.name, prior.image_path)
                    print "Duplicate photo B (%s) %s %s" % (hp.id, hp.name, hp.image_path)
                    yield(hp, prior)
            filesizes[hp.size].append(hp)
            self._reporter.Increment()


class ProgressReporter(object):
    """Generic progress reporter. The Report method should be overridden if progress
should be reported to GUI rather than stdout"""

    def __init__(self):
        self.count = 0
        self.target = 0

    def Report(self, progress):
        print progress

    def Increment(self):
        self.count = self.count + 1
        if self.count % 10 == 0:
            self.Report("Scanned %d of %d" % (self.count, self.target))

    def Target(self, target):
        self.target = target


class DubFinderTest(unittest.TestCase):
    def test_HashedPhoto(self):
        iPhoto = appscript.app('iPhoto')
        album = iPhoto.photo_library_album()
        photo1 = album.photos[0]
        x = HashedPhoto(album, photo1)
        x.fingerprint
        self.assertEquals(photo1.id(), x.id, "ID is correct")
        self.assertEquals(photo1.name(), x.name, "Name is correct")
        self.assertEquals(photo1.image_path(), x.image_path, "Image path is correct")
