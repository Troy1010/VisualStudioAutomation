import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS

#dev
def Proj(vProj):
    cPossibleKeys = ["Name"
        #,"Collection"
        ,"ProjectItems"]
    TM.Narrator.Print(vProj,cCOMSearchMembers=cPossibleKeys,iRecursionThreshold=4)
