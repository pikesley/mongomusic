#!/usr/bin/env python

from pymongo import Connection
import yaml
import tagpy
import sys
import hashlib
import os
import re

class Track(dict):
    def __init__(self, path, verbose=False):
        self.verbose = verbose
        self['path'] = path
        self.fileref = tagpy.FileRef(self['path'])

        self.tags = self.fileref.tag()

        self['artist'] = self.tags.artist
        self['track'] = self.tags.track
        self['title'] = self.tags.title
        self['album'] = self.tags.album
        self['year'] = self.tags.year
        self['_id'] = hashlib.md5(self['path']).hexdigest()
        self['file_type'] = self['path'].split('.')[-1]
        self['full_name'] = '/'.join([self['artist'], self['album'], self['title']])
        self['size'] = os.path.getsize(self['path'])

    def is_in(self, collection):
        f = collection.find({'_id': self['_id']})
        return len(list(f)) > 0

    def store(self, collection):
        if not self.is_in(collection):
            if self.verbose: print "Storing '%s'" % self['full_name']
            collection.insert(self)
        else:
            if self.verbose: print "'%s' already stored" % self['full_name']

def populate(drop_first=False, music_path=None, verbose=None):
    if drop_first:
        clxn.drop()

    if music_path:
        mp = music_path
    else:
        mp = y['paths']['music']

    for d in os.walk(mp):
        for t in d[2]:
            if t.endswith("ogg") or t.endswith("mp3"):
                track = Track(os.path.join(d[0], t), verbose)
                track.store(clxn)

def index(verbose=None):
    t = clxn.find_one()
    for k in t.keys():
        if verbose: print "Creating index '%s'" % (k)
        clxn.create_index(k)

def purge(verbose=False):
    results = clxn.find()
    for res in list(results):
        if not os.path.exists(res['path']):
            if verbose: print "Deleting '%s'" % res['path']
            clxn.remove(res["_id"])

yamlpath = 'config/config.yaml'
f = open(yamlpath, 'r')
y = yaml.load(f)
d = y['mongo']

cnxn = Connection(d['host'], d['port'])

db = cnxn[d['db']]
clxn = db[d['collection']]

if __name__ == '__main__':
    from options import options

    if options.action == "update":
        populate(drop_first=False, music_path=options.music_path, verbose=options.verbose)
        purge(verbose=options.verbose)

    if options.action == "scratch":
        populate(drop_first=True, music_path=options.music_path, verbose=options.verbose)

    if options.action == "purge":
        purge(verbose=options.verbose)

    if options.action == "index":
        index(verbose=options.verbose)

