#!/usr/bin/env python

"""Detect duplicate photos in an iPhoto library, using SHA1 hashes to determine equality
"""

from appscript import app
import os.path
import unittest
import hashlib
import wx
import wx.grid
import sys
import os
import shutil
import os.path

__author__ = 'jey'

class HashCache:
    cachedir='/tmp/iphotoduphashcache'
    def __init__(self):
        if not os.path.exists(HashCache.cachedir):
            os.makedirs(HashCache.cachedir)
    def clean(self):
        if os.path.exists(HashCache.cachedir):
            shutil.rmtree(HashCache.cachedir)
            os.makedirs(HashCache.cachedir)
            
    def add(self,id,hash):
        file = self.cachefile(id)
        f = open(file,'w')
        f.write(hash)
        f.close()
    def get(self,id):
        file = self.cachefile(id)
        if os.path.exists(file):
            f = open(file,"r")
            hash = f.read()
            f.close()
            return hash
        else:
            return None
    def cachefile(self,id):
        return os.path.join(HashCache.cachedir,str(id))

class HashedPhoto:
    cache = HashCache()
    def __init__(self, photo):
        self.id = photo.id.get()
        self.name = photo.name().get()
        self.image_path = photo.image_path().get()
        phash = HashedPhoto.cache.get(self.id)
        if phash == None:
            f = open(photo.image_path.get(), 'rb')
            h = hashlib.sha1()
            h.update(f.read())
            phash = h.hexdigest()
            f.close()
            HashedPhoto.cache.add(self.id,phash)
        self.fingerprint = phash

def find_dups():
    iPhoto = app('iPhoto')
    album = iPhoto.photo_library_album()
    fingerprints = {}
    for p in album.photos():
        hp = HashedPhoto(p)
        if hp.fingerprint in fingerprints:
            prior = fingerprints[hp.fingerprint]
            print "Duplicate photo A (%s) %s %s" % (prior.id, prior.name, prior.image_path)
            print "Duplicate photo B (%s) %s %s" % (hp.id, hp.name, hp.image_path)
            yield(hp, prior)
        else:
            fingerprints[hp.fingerprint] = hp


class DupBrowserFrame(wx.Frame):
    rowlimit=10
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(700, 300))
        panel = wx.Panel(self)
        self.control = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.grid = wx.grid.Grid(panel)
        self.grid.CreateGrid(self.rowlimit,6)
        self.grid.EnableEditing(False)
        self.grid.SetColLabelValue(0,"Dup ID")
        self.grid.SetColLabelValue(1,"Dup Name")
        self.grid.SetColLabelValue(2,"Dup Path")
        self.grid.SetColLabelValue(3,"Prior ID")
        self.grid.SetColLabelValue(4,"Prior Name")
        self.grid.SetColLabelValue(5,"Prior Path")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        sizer.Add(self.control,2,wx.EXPAND)
        panel.SetSizer(sizer)
        self.CreateStatusBar()
        self.DefineMenu()
        self.Show(True)

    def DefineMenu(self):
        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuScan = filemenu.Append(9001, "&Scan", "Scan iPhoto Library")
        self.Bind(wx.EVT_MENU, self.OnScan, menuScan)
        menuClean = filemenu.Append(9002, "&Clean", "Clean out the duplicate scanning cache")
        self.Bind(wx.EVT_MENU, self.OnClean, menuClean)
        self.SetMenuBar(menuBar)

    def OnClean(self,event):
        HashCache().clean()
        self.SetStatusText("Cache cleaned")

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "A utility to detect duplicate photos in iPhoto", "About iPhotoDupFind", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def OnScan(self, event):
        self.SetStatusText("Starting scan of library ...")
        self.control.AppendText("Scanning ...\n")
        row = 0
        try:
            for (dup, prior) in find_dups():
                if row > self.rowlimit:
                    self.grid.AppendRows(5)
                    self.rowlimit=self.rowlimit+5
                self.grid.SetCellValue(row,0,str(dup.id))
                self.grid.SetCellValue(row,1,dup.name)
                self.grid.SetCellValue(row,2,dup.image_path)
                self.grid.SetCellValue(row,3,str(prior.id))
                self.grid.SetCellValue(row,4,prior.name)
                self.grid.SetCellValue(row,5,prior.image_path)
                row = row + 1
        except:
            self.control.AppendText("Scan aborted with error:\n")
            map(self.control.AppendText,sys.exc_info())
            self.SetStatusText("Library scan aborted")
        self.SetStatusText("Scan completed")


class DupBrowser():
    def __init__(self):
        print ""

    def main(self):
        app = wx.App(False)
        frame = DupBrowserFrame(None, "iPhoto Dup Browser")
        app.MainLoop()


class JPhotoTest(unittest.TestCase):
    def test_list(self):
        find_dups()

if __name__ == "__main__":
    DupBrowser().main()