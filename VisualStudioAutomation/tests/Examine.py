import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS

with VS.OpenProj("res\\Examples\\HelloWorld.vcxproj") as vProj:
    vProj.Properties[24].Value = "Beep"
    vProp = vProj.Properties[24]
#    vProp.Name = "BOOP"
    vProp.Value = "Biip"
    #vProj.Properties.add(5)
    #vName.append("Beep")
    TM.Narrator.Print(vProj.Properties,bIncludeProtected=True,bIncludePrivate=True,iRecursionThreshold=1)
