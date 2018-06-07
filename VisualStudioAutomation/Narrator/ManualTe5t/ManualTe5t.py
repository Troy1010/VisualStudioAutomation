import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS
import VisualStudioAutomation.DTEUser
import VisualStudioAutomation.Narrator as SVNR


#---Open
vDTE = VS.InstantiateDTE()
vProj = VS.OpenProj(vDTE,"res\HelloWorld.vcxproj")
#---
SVNR.Proj(vProj)
#---Close
VS.QuitDTE(vDTE)
