#!/usr/bin/env python

"""Detect duplicate photos in an iPhoto library, using SHA1 hashes to determine equality
"""

import appscript
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

class HashCache(object):
    cachedir='/tmp/iphotoduphashcache'
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
        f = open(file,'w')
        f.write(value)
        f.close()
    def __contains__(self,item):
        file = self._cachefile(item)
        if os.path.exists(file):
            return True
        else:
            return False

    def __getitem__(self,key):
        file = self._cachefile(key)
        if os.path.exists(file):
            f = open(file,"r")
            hash = f.read()
            f.close()
            return hash
        else:
            return None
    def __len__(self):
        return len([name for name in os.listdir(HashCache.cachedir) if os.path.isfile(name)])

    def _cachefile(self,id):
        return os.path.join(HashCache.cachedir,id)

class HashedPhoto(object):
    cache = HashCache()
    def __init__(self, album, id, image_path):
        self.id = id
        self._album = album
        self.key = str(id)
        self._image_path = image_path
        self._size = None

    def _checksum(self,st):
        return reduce(lambda x,y:x+y, map(ord, st))

    @property
    def fingerprint(self):
        if self.key in HashedPhoto.cache:
            phash = HashedPhoto.cache[self.key]
            print "Reusing cached hash for %d" % self.id
        else:
            print "Generating hash for %d" % self.id
            f = open(self.image_path, 'rb')
            h = hashlib.sha1()
            h.update(f.read())
            phash = h.hexdigest()
            f.close()
            HashedPhoto.cache[self.key]=phash
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
        return self._album.photos.ID(self.ID).height()
    @property
    def width(self):
        return self._album.photos.ID(self.ID).width()
    @property
    def date(self):
        return self._album.photos.ID(self.ID).date()

def find_dups(iPhoto,progressreporter):
    progressreporter.Report("Connecting to iPhoto")

    progressreporter.Report("Retrieving photo list from iPhoto")
    album = iPhoto.photo_library_album()

    filesizes = {}
    image_paths = album.photos.image_path.get()
    ids = album.photos.id.get()

    progressreporter.Target(len(ids))
    progressreporter.Report("Scanning %d photos supplied by iPhoto" % len(ids))

    for n in range(len(ids)):
        hp = HashedPhoto(album,ids[n],image_paths[n])
        if hp.size not in filesizes:
            filesizes[hp.size] = []

        for prior in filesizes[hp.size]:
            if prior.fingerprint == hp.fingerprint:
                print "Duplicate photo A (%s) %s %s" % (prior.id, prior.name, prior.image_path)
                print "Duplicate photo B (%s) %s %s" % (hp.id, hp.name, hp.image_path)
                yield(hp, prior)
        filesizes[hp.size].append(hp)
        progressreporter.Increment()

class ProgressReporter(object):
    def __init__(self):
        self.count = 0
        self.target = 0

    def Report(self,progress):
        print progress

    def Increment(self):
        self.count = self.count + 1
        if self.count % 10 == 0:
            self.Report("Scanned %d of %d" % (self.count,self.target))

    def Target(self,target):
        self.target = target

class DupFinderFrame(wx.Frame):
    rowlimit=0

    def __init__(self, parent, title, iPhoto):
        wx.Frame.__init__(self, parent, title=title, size=(850, 300))
        panel = wx.Panel(self)
        self._define_toolbar()
        self._define_grid(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        self.CreateStatusBar()
        self._define_menu()
        self.Show(True)
        self.iPhoto = iPhoto

    def _define_toolbar(self):
        TOOL_ID_SCAN = wx.NewId()
        TOOL_ID_DELETE = wx.NewId()
        TOOL_ID_EXIT = wx.NewId()
        
        tb = wx.ToolBar(self,-1)
        self.SetToolBar(tb)
        tb.AddLabelTool(TOOL_ID_SCAN,'Scan',wx.Bitmap('icons/scan.png'), wx.NullBitmap,wx.ITEM_NORMAL,'Scan iPhoto for duplicates')
        self.Bind(wx.EVT_TOOL,self.OnScan,id=TOOL_ID_SCAN)
        tb.AddLabelTool(TOOL_ID_DELETE,'Delete',wx.Bitmap('icons/delete.png'), wx.NullBitmap,wx.ITEM_NORMAL,'Delete selected duplicates')
        tb.AddSeparator()
        tb.AddLabelTool(TOOL_ID_EXIT,'Exit',wx.Bitmap('icons/exit.png'), wx.NullBitmap,wx.ITEM_NORMAL,'Exit the dup finder tool')
        self.Bind(wx.EVT_TOOL,self.OnExit,id=TOOL_ID_EXIT)
        tb.Realize()


    def _define_grid(self, panel):
        self.grid = wx.grid.Grid(panel)
        self.grid.CreateGrid(self.rowlimit, 6)
        self.grid.EnableEditing(False)
        #self.grid.AutoSizeColumns(True)
        dup_colour = wx.Colour(255,239,213)
        prior_colour = wx.Colour(238,210,238)
        self.grid.SetRowLabelSize(0)
        self.grid.SetLabelBackgroundColour('MIDNIGHT BLUE')
        self.grid.SetLabelTextColour('WHITE')
        self.grid.SetColLabelValue(0, "A ID")
        self.grid.SetColLabelValue(1, "A Name")
        self.grid.SetColSize(1,150)
        self.grid.SetColLabelValue(2, "A Path")
        self.grid.SetColSize(2,200)
        self.grid.SetColLabelValue(3, "B ID")
        self.grid.SetColLabelValue(4, "B Name")
        self.grid.SetColSize(4,150)
        self.grid.SetColLabelValue(5, "B Path")
        self.grid.SetColSize(5,200)

        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
                       self.OnRightClickGrid)

    def OnRightClickGrid(self,event):
        """
        Show a context menu on right-click on grid row
        """
        if event.GetRow() == 0:
            return
        
        if not hasattr(self, "row_rightclick_goto_a"):
            self.row_rightclick_goto_a = wx.NewId()
            self.row_rightclick_goto_b = wx.NewId()
        self.cicked_row = event.GetRow()
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.OnRightClickMenuItem, menu.Append(self.row_rightclick_goto_a,"Goto Photo A"))
        self.Bind(wx.EVT_MENU, self.OnRightClickMenuItem, menu.Append(self.row_rightclick_goto_b,"Goto Photo B"))
        self.PopupMenu(menu)
        menu.Destroy()

    def OnRightClickMenuItem(self,event):

        if event.GetId() == self.row_rightclick_goto_a:
            id_col = 0
        else:
            id_col = 3
        id = self.grid.GetCellValue(self.cicked_row,id_col)
        print "MENU: ID %s PHOTO %s" % (event.GetId(),id)
        self.iPhoto.photo_library_album().photos.ID(int(id)).select()
        self.iPhoto.reopen()


    def _define_menu(self):
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
        self.Report("Cache cleaned")

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "A utility to detect duplicate photos in iPhoto", "About iPhotoDupFind", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def Report(self,progress):
        self.SetStatusText(progress)
        wx.Yield()

    def OnScan(self, event):
        self.Report("Starting scan of library ...")
        self.grid.ClearGrid()
        if self.grid.NumberRows>0:
            self.grid.DeleteRows(0,self.grid.NumberRows)
        wx.Yield()
        row = 0
        reporter = ProgressReporter()
        setattr(reporter,'Report',self.Report)
        try:
            for (dup, prior) in find_dups(self.iPhoto,reporter):
                if row >= self.rowlimit:
                    self.grid.AppendRows(1)
                    self.rowlimit=self.rowlimit+1
                self.grid.SetCellValue(row,0,str(dup.id))
                self.grid.SetCellValue(row,1,dup.name)
                self.grid.SetCellValue(row,2,dup.image_path)
                self.grid.SetCellValue(row,3,str(prior.id))
                self.grid.SetCellValue(row,4,prior.name)
                self.grid.SetCellValue(row,5,prior.image_path)
                wx.Yield()
                row = row + 1
        except:
            self.Report("Library scan aborted (%s)" % sys.exc_info()[1])
        self.Report("Scan completed")


class DupFinder(object):
    def __init__(self):
        print "Starting up dup finder"

    def main(self):
        app = wx.App(False)
        iPhoto = appscript.app('iPhoto')
        frame = DupFinderFrame(None, "iPhoto Dup Finder",iPhoto)
        app.MainLoop()


class DubFinderTest(unittest.TestCase):
    def test_HashedPhoto(self):
        iPhoto = app('iPhoto')
        album = iPhoto.photo_library_album()
        photo1 = album.photos[0]
        x = HashedPhoto(album,photo1)
        x.fingerprint
        self.assertEquals(photo1.id(),x.id,"ID is correct")
        self.assertEquals(photo1.name(),x.name,"Name is correct")
        self.assertEquals(photo1.image_path(),x.image_path,"Image path is correct")

if __name__ == "__main__":
    DupFinder().main()