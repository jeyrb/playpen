
import wx
import wx.grid
import appscript
import sys

from pyphoto.dup_find import ProgressReporter,DupFinder
import wx.grid.PyGridTableBase

class DupFinderFrame(wx.Frame):
    rowlimit=0

    def __init__(self, parent, title, iPhoto):
        wx.Frame.__init__(self, parent, title=title, size=(850, 300))
        panel = wx.Panel(self)
        self._define_toolbar()
        self._define_grid(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._grid, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        self.CreateStatusBar()
        self._define_menu()
        self._stopped = False
        self.iPhoto = iPhoto
        reporter = ProgressReporter()
        setattr(reporter,'Report',self.Report)
        self._df = DupFinder(self.iPhoto,reporter)
        self.Show(True)

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
        self._grid = wx.grid.Grid(panel)
        self._grid_model = DupFinderGridModel()
        self._grid.SetTable(self._grid_model)
        self._grid.CreateGrid(self.rowlimit, 6)
        self._grid.EnableEditing(False)
        #self.grid.AutoSizeColumns(True)
        #dup_colour = wx.Colour(255,239,213)
        #prior_colour = wx.Colour(238,210,238)

        self._grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
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
        id = self._grid.GetCellValue(self.cicked_row,id_col)
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
        menuExport = filemenu.Append(9903,"E&xport","Export results to a text file")
        self.Bind(wx.EVT_MENU, self.OnExport,menuExport)
        self.SetMenuBar(menuBar)

    def OnClean(self,event):
        self._df.clean()
        self.Report("Cache cleaned")

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "A utility to detect duplicate photos in iPhoto", "About iPhotoDupFind", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExport(self,event):
        pass

    def OnExit(self, event):
        print "Shutting down Dup Finder GUI"
        self._stopped = True
        self._df.stop()
        self.Close(True)

    def Report(self,progress):
        if self._stopped:
            print progress
        else:
            self.SetStatusText(progress)
            wx.Yield()

    def OnScan(self, event):
        self.Report("Starting scan of library ...")
        self._grid.ClearGrid()
        if self._grid.NumberRows>0:
            self._grid.DeleteRows(0,self._grid.NumberRows)
        wx.Yield()
        row = 0


        try:
            for (dup, prior) in self._df.find_dups():
                if row >= self.rowlimit:
                    self._grid.AppendRows(1)
                    self.rowlimit=self.rowlimit+1
                self._grid.SetCellValue(row,0,str(dup.id))
                self._grid.SetCellValue(row,1,dup.name)
                self._grid.SetCellValue(row,2,dup.image_path)
                self._grid.SetCellValue(row,3,str(prior.id))
                self._grid.SetCellValue(row,4,prior.name)
                self._grid.SetCellValue(row,5,prior.image_path)
                wx.Yield()
                row = row + 1
        except:
            self.Report("Library scan aborted (%s)" % sys.exc_info()[1])
        self.Report("Scan completed")

class DupFinderGridModel(wx.grid.PyGridTableBase):
        self.base_SetRowLabelSize(0)
        self.base_SetLabelBackgroundColour('MIDNIGHT BLUE')
        self._grid.SetLabelTextColour('WHITE')
        self._grid.SetColLabelValue(0, "A ID")
        self._grid.SetColLabelValue(1, "A Name")
        self._grid.SetColSize(1,150)
        self._grid.SetColLabelValue(2, "A Path")
        self._grid.SetColSize(2,200)
        self._grid.SetColLabelValue(3, "B ID")
        self._grid.SetColLabelValue(4, "B Name")
        self._grid.SetColSize(4,150)
        self._grid.SetColLabelValue(5, "B Path")
        self._grid.SetColSize(5,200)

class DupFinderGUI(object):
    def __init__(self):
        print "Starting up dup finder"

    def main(self):
        gui = wx.App(False)
        iPhoto = appscript.app('iPhoto')
        frame = DupFinderFrame(None, "iPhoto Dup Finder",iPhoto)
        gui.MainLoop()
        sys.exit()

