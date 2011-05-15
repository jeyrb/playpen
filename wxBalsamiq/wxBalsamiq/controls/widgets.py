__author__ = 'jey'

class Control(object):
    btype="Unknown Control"
    def __init__(self,imported_control):
        self.id=imported_control.attrib.get('controlID')

    def __str__(self):
        return "ID: %s Type:%s" % (self.id,self.btype)

class Button(Control):
    btype="com.balsamiq.mockups::Button"

class TextBox(Control):
    btype="com.balsamiq.mockups::TextInput"

class CheckBox(Control):
    btype="com.balsamiq.mockups::CheckBox"

class CheckBoxGroup(Control):
    btype="com.balsamiq.mockups::CheckBoxGroup"

class ComboBox(Control):
    btype="com.balsamiq.mockups::ComboBox"