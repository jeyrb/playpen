__author__ = 'jey'

import wx
import sys

class wxHiFiMockup(object):
       def main(self):
        gui = wx.App(False)
        frame = wxHiFiMockupFrame(None)
        gui.MainLoop()
        sys.exit()

class wxHiFiMockupFrame(wx.Frame)

    def __init__(self, parent,title='wx Hifi Mockup'):
        wx.Frame.__init__(self, parent, title=title, size=(850, 300))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._grid, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        self.Show(True)