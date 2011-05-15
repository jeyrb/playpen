import wx
import sys

class wxHiFiMockupFrame(wx.Frame):
    def __init__(self, parent,size,controls,title='wx Hifi Mockup'):
        wx.Frame.__init__(self, parent, size=size, title=title)

        panel = wx.Panel(self)
        font= wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(7)
        panel.SetFont(font)
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #panel.SetSizer(sizer)

        for control in controls:
            control.Render(panel)
        self.Show(True)

class wxHiFiMockup(object):
    def __init__(self,size,controls):
        self.controls = controls
        self.size=size

    def main(self):
        gui = wx.App(False)
        frame = wxHiFiMockupFrame(None,self.size,self.controls)
        gui.MainLoop()
        sys.exit()