import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS

with TM.CopyContext("res/Examples_Backup","res/Examine"):
    vCommandSet = VS.CommandSet()
    vCommandSet.Que([IntegrateProps,IntegrateProps_Undo],["HelloWorld.vcxproj","conanbuildinfo.props"])
    vCommandSet.Execute()
