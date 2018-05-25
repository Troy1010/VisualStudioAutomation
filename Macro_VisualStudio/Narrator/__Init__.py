import ctypes
from pprint import pprint
import TM_CommonPy as TMC
import TM_CommonPy.Narrator as TMC_NAR
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import collections


__self = sys.modules[__name__]
iIndent = 0
sIndent = "-"

def __Indent():
    return __self.sIndent * __self.iIndent

#Indented NewLine
def __NL():
    return "\n"+__Indent()

#------Public

#Remember to use () for all DTE methods. Instead of throwing an exception, they just fizzle.

def NarrateProject(vProject):
    return TMC_NAR.NarrateUnknown(vProject,('FileName','ProjectItems'))
#    sReturning = __Indent() + "Project.\n"
#    sReturning += __NL() + "FileName:"+vProject.FileName
#    sReturning += __NL() + "ProjectItems.."
#    sReturning += __NL() + TMC.Narrator.NarrateCollection(vProject.ProjectItems)
    #for i in range(vProject.ProjectItems.Count):
    #    sReturning += vProject.ProjectItems[i]
    #for vValue in vProject.ProjectItems:
    #    print("vValue:"+str(vValue))
    #sReturning +=TMC.Narrator.NarrateCollection(vProject.Properties)
#    return sReturning

def NarrateProjectItems(vProjectItems):
    pass
