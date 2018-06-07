import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS
import VisualStudioAutomation.Complex


#---Open
vDTE = VS.InstantiateDTE()
vProj = VS.OpenProj(vDTE,"res\HelloWorld.vcxproj")
#---
#print("Props:"+TM.Narrator.Narrate(vProj.Properties, iRecursionThreshold=1))
#print("~:"+TM.Narrator.Narrate(vProj, iRecursionThreshold=2))
def GetMembers_COM(vObj):
    cMembers = {}
    cPossibleKeys = ["Name"]
    for vKey in cPossibleKeys:
        if hasattr(vObj,vKey):
            vValue = getattr(vObj,vKey)
            cMembers[vKey] = vValue
    return cMembers



#print("Members:"+TM.Narrator.Narrate(GetMembers_COM(vProj), iRecursionThreshold=2))
#print("vProj:"+TM.Narrator.Narrate_COM_Object(vProj))
print("vProj.Object:"+TM.Narrator.Narrate_COM_Object(vProj.Object))
print("type(vProj.Object):"+str(type(vProj.Object)))





#---Close
VS.QuitDTE(vDTE)
