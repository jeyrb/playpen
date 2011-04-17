#!/usr/bin/env python

"""Detect duplicate photos in an iPhoto library, using SHA1 hashes to determine equality
"""

from appscript import app
import os.path
import unittest
import hashlib

__author__ = 'jey'

class HashedPhoto:
    def __init__(self,photo):
        self.photo_id = photo.id
        f = open(photo.image_path.get(),'rb')
        h = hashlib.sha1()
        h.update(f.read())
        f.close()
        self.fingerprint = h.hexdigest()

def find_dups():
    iPhoto = app('iPhoto')
    album=iPhoto.photo_library_album()
    fingerprints = {}
    for p in album.photos():
        hp = HashedPhoto(p)
        if hp.fingerprint in fingerprints:
            prior = fingerprints[hp.fingerprint]
            print "Duplicate photo A (%s) %s %s" % (prior.id,prior.name,prior.image_path)
            print "Duplicate photo B (%s) %s %s" % (p.id,p.name,p.image_path)
        else:
            fingerprints[hp.fingerprint] = hp

def main():
    find_dups()

class JPhotoTest(unittest.TestCase):
    def test_list(self):
        find_dups()