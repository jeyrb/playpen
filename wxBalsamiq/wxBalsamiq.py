__author__ = 'jey'

from xml.etree import ElementTree
import wxBalsamiq.controls.widgets
from wxBalsamiq.hifi.wxhifi import wxHiFiMockup

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

mockup=bdom.getroot()
size=(int(mockup.attrib['mockupW']),int(mockup.attrib['mockupH']))
print "Mockup is size %d by %d" % (size[0],size[1])
mockup = wxHiFiMockup(size,controls)
mockup.main()