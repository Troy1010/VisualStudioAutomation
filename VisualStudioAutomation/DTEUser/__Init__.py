import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys, os
import xml.etree.ElementTree
import win32com.client
import time

#dev
def SetTMDefaultSettings(sProj):
    #---Open
    vDTE = InstantiateDTE()
    vProj = OpenProj(vDTE,sProj)
    #---
    vProj.Properties
    #---Close
    QuitDTE(vDTE)
