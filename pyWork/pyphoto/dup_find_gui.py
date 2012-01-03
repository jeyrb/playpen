
import wx
import wx.grid
import appscript
import sys

from pyphoto.dup_find import ProgressReporter,DupFinder

class DupFinderFrame(wx.Frame):

    def __init__(self, parent, title, iPhoto):
        wx.Frame.__init__(self, parent, title=title, size=(850, 300))
        panel = wx.Panel(self)
        self._define_toolbar()
        self._grid = DupFinderGridModel( wx.grid.Grid(panel), self.OnRightClickGrid )
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._grid.GetGrid(), 1, wx.EXPAND)
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

    def OnRightClickGrid(self,event):
        """
        Show a context menu on right-click on grid row
        """
        if event.GetRow() == 0:
            return

        if not hasattr(self, "row_rightclick_goto_a"):
            self.row_rightclick_goto_a = wx.NewId()
            self.row_rightclick_goto_b = wx.NewId()
        self.clicked_row = event.GetRow()
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.OnRightClickShowPhoto, menu.Append(self.row_rightclick_goto_a,"Goto Photo A"))
        self.Bind(wx.EVT_MENU, self.OnRightClickFlagPhoto, menu.Append(self.row_rightclick_goto_a,"Flag Photo A"))
        self.Bind(wx.EVT_MENU, self.OnRightClickShowPhoto, menu.Append(self.row_rightclick_goto_b,"Goto Photo B"))
        self.Bind(wx.EVT_MENU, self.OnRightClickFlagPhoto, menu.Append(self.row_rightclick_goto_b,"Flag Photo B"))
        self.PopupMenu(menu)
        menu.Destroy()

    def OnRightClickShowPhoto(self,event):

        if event.GetId() == self.row_rightclick_goto_a:
            id_col = 0
        else:
            id_col = 3
        id = self._grid.GetValue( self.clicked_row,id_col )
        self.iPhoto.photo_library_album().photos.ID(int(id)).select()
        self.iPhoto.reopen()

    def OnRightClickFlagPhoto(self,event):

            if event.GetId() == self.row_rightclick_goto_a:
                id_col = 0
            else:
                id_col = 3
            id = self._grid.GetValue( self.clicked_row,id_col )
            photo = self.iPhoto.photo_library_album().photos.ID(int(id)).select()
            photo.assign_keyword(u'POSSIBLE_DUPLICATE')

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
        self._grid.Clear()
        row = 0


        try:
            for (dup, prior) in self._df.find_dups():
                self._grid.AppendRow( ( str(dup.id),
                                            dup.name,
                                            dup.image_path,
                                            prior.id,
                                            prior.name,
                                            prior.image_path) )
        except:
            self.Report("Library scan aborted (%s)" % sys.exc_info()[1])
        self.Report("Scan completed")


class DupFinderGridModel( wx.grid.PyGridTableBase ):
    columns = [
                { 'label': { 'value': 'A ID'}, 'fontSize' : 8, 'fg': wx.GREEN, 'width' : 60 },
                { 'label': { 'value': 'A Name'}, 'fontSize': 10, 'fg': wx.GREEN,'width' : 150 },
                { 'label': { 'value': 'A Path'}, 'hAlign': wx.ALIGN_RIGHT, 'fontSize': 8, 'fg': wx.GREEN,'width' : 250 },
                { 'label': { 'value': 'B ID'}, 'fontSize': 8, 'fg': wx.BLUE,'width' : 60 },
                { 'label': { 'value': 'B Name'}, 'fontSize': 10, 'fg': wx.BLUE,'width' : 150 },
                { 'label': { 'value': 'B Path'}, 'hAlign': wx.ALIGN_RIGHT, 'fontSize': 8, 'fg': wx.BLUE,'width' : 250 }
            ]

    def __init__(self, grid, rightClickHandler ):
        super(DupFinderGridModel,self).__init__()
        self.ResetData()
        self._grid = grid
        self._grid.SetTable( self )
        self._grid.EnableEditing(False)
        self._grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,rightClickHandler)
        for ( col, config ) in enumerate(self.columns):
            if 'width' in config:
                self._grid.SetColSize( col, config['width'] )
            attr =  wx.grid.GridCellAttr()
            if 'hAlign' in config:
                attr.SetAlignment( config['hAlign'], wx.ALIGN_CENTRE_VERTICAL )
            if 'fontSize' in config:
                font = wx.Font(config['fontSize'], wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL )
                attr.SetFont( font )
            if 'fg' in config:
                attr.SetTextColour( config['fg'] )
            attr.SetReadOnly( True )
            self._grid.SetColAttr( col, attr)

    def UpdateValues(self ):
            msg = wx.grid.GridTableMessage( self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES )
            self._grid.ProcessTableMessage(msg)

    def GetNumberRows( self ):
        return len( self.data )

    def GetGrid(self ):
        return self._grid

    def GetNumberCols( self ):
        return len ( self.columns )

    def AppendRow ( self, row ):
        self.data.append( row )
        self.ResetView()

    def ResetData(self ):
        self.data = []
        self.currentRows = 0

    def Clear ( self ):
        self.ResetData()
        super(DupFinderGridModel,self).Clear()
        self.ResetView()

    def ResetView(self):
        """Trim/extend the control's rows and update all values"""
        self._grid.BeginBatch()
        if self.GetNumberRows() < self.currentRows:
            msg = wx.grid.GridTableMessage(
                            self,
                            wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                            self.GetNumberRows(),    # position
                            self.currentRows-self.GetNumberRows(),
                            )
            self._grid.ProcessTableMessage(msg)
        elif self.GetNumberRows() > self.currentRows:
            msg = wx.grid.GridTableMessage(
                            self,
                            wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                            self.GetNumberRows()-self.currentRows
                            )
            self._grid.ProcessTableMessage(msg)
        self.UpdateValues()
        self._grid.EndBatch()
        self.currentRows = self.GetNumberRows()

        h,w = self._grid.GetSize()
        self._grid.SetSize((h+1, w))
        self._grid.SetSize((h, w))
        self._grid.ForceRefresh()
        wx.Yield()

    def GetColLabelValue(self, col):
        return self.columns[ col ]['label']['value']

    def IsEmptyCell(self, row, col):
        return row >= len(self.data) or self.data[ row ] is None or self.data[ row ][ col ] is None

    def GetValue(self, row, col):
        cell = None
        if not self.IsEmptyCell( row, col ):
            cell = self.data[ row ][ col ]
        if cell:
            return cell
        else:
            return ''


class DupFinderGUI(object):
    def __init__(self):
        print "Starting up dup finder"

    def main(self):
        gui = wx.App(False)
        iPhoto = appscript.app('iPhoto')
        frame = DupFinderFrame(None, "iPhoto Dup Finder",iPhoto)
        gui.MainLoop()
        sys.exit()

