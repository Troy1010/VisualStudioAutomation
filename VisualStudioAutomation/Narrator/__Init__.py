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
    cPossibleKeys = ["qwer"
        ,"Object"
        ,"Properties"
        ,"Files"
        ,"Filters"
        #,"ProjectItems"
        ]
        #,cCOMSearchMembers=cPossibleKeys
    TM.Narrator.Print(vProj,cCOMSearchMembers=cPossibleKeys,iRecursionThreshold=3,bHideDuplications=False)
