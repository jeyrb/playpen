__author__ = 'jey'

import wx
import urllib

class Control(object):
    btype="Unknown Control"
    def __init__(self,imported_control):
        self.id=int(imported_control.attrib.get('controlID'))
        self.mock_control = imported_control
        self.position=(int(imported_control.attrib['x']),int(imported_control.attrib['y']))
        self.size=(int(imported_control.attrib['measuredW']),int(imported_control.attrib['measuredH']))
        print "Created control type %s size %d,%d position %d,%d" % (self.btype,self.size[0],self.size[1],self.position[0],self.position[1])
    def __str__(self):
        return "ID: %s Type:%s" % (self.id,self.btype)
    def Text(self):
        title=self.mock_control.findtext('controlProperties/text')
        return urllib.unquote(title)
    def _Font(self):
        if not hasattr(self,'_font'):
            self._font= wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
            self._font.SetPointSize(10)
        return self._font

    def Render(self,parent):
        wxcontrol=self._render(parent)
        if wxcontrol is not None:
            wxcontrol.SetFont(self._Font())
        return wxcontrol

class Button(Control):
    btype="com.balsamiq.mockups::Button"
    def _render(self,parent):
        return wx.Button(parent, self.id, self.Text(), self.position, self.size)

class TextInput(Control):
    btype="com.balsamiq.mockups::TextInput"
    def _render(self,parent):
        return wx.TextCtrl(parent, self.id, self.Text(), self.position, self.size)

class TextArea(Control):
    btype="com.balsamiq.mockups::TextArea"
    def _render(self,parent):
        return wx.TextCtrl(parent, self.id, self.Text(), self.position, self.size)

class DateChooser(Control):
    btype="com.balsamiq.mockups::DateChooser"
    def _render(self,parent):
        dt = wx.DateTime()
        dt.ParseDate(self.Text())
        if dt.GetCentury() < 0:
            dt.SetYear(dt.GetYear()+2000)
        return wx.DatePickerCtrl(parent, self.id, dt, self.position, self.size,style=wx.DP_DROPDOWN)

class ComboBox(Control):
    btype="com.balsamiq.mockups::ComboBox"
    def _render(self,parent):
        choices=self.mock_control.findtext('controlProperties/text').split('%0A')
        #ignore size for combo boxes
        return wx.ComboBox(parent, self.id, '', self.position, choices=choices,style=wx.CB_DROPDOWN)

class NumericChooser(Control):
    btype="com.balsamiq.mockups::NumericStepper"
    def _render(self,parent):
        choices=self.mock_control.findtext('controlProperties/text').split('%0A')
        #ignore size for combo boxes
        return wx.SpinCtrl(parent, self.id, self.Text(), self.position,min=0,max=999)

class CheckBox(Control):
    btype="com.balsamiq.mockups::CheckBox"
    def _render(self,parent):
        return wx.CheckBox(parent, self.id, label=self.Text(), pos=self.position,size=self.size)


class Label(Control):
    btype="com.balsamiq.mockups::Label"
    def _render(self,parent):
        return wx.StaticText(parent, self.id, self.Text(), self.position, self.size)

class Paragraph(Label):
    btype="com.balsamiq.mockups::Paragraph"

class TextBox(Control):
    btype="com.balsamiq.mockups::TextInput"
    def _render(self,parent):
        pass

class CheckBoxGroup(Control):
    btype="com.balsamiq.mockups::CheckBoxGroup"
    def _render(self,parent):
        pass
