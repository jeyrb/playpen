__author__ = 'jey'

from xml.etree import ElementTree
import wxBalsamiq.controls.widgets
import wxBalsamiq.hifi.wx

control_classes={}
for widget in dir(wxBalsamiq.controls.widgets):
    control_class = getattr(wxBalsamiq.controls.widgets,widget)
    if hasattr(control_class,'btype'):
        print "Registered %s for mockup ID %s" % (control_class,control_class.btype)
        control_classes[control_class.btype]=control_class

bdom = ElementTree.parse('fixtures/photo.bmml')
controls=[]
for bcontrol in bdom.getiterator('control'):
    type = bcontrol.attrib['controlTypeID']
    if type in control_classes:
        control = control_classes[type](bcontrol)
        controls.append(control)
        print control
    else:
        print "Ignoring unsupported control %s" % type

mockup = wxHiFiMockup()
mockup.main()