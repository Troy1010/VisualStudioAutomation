import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS

with VS.OpenProj("Examples_Backup - Copy\\HelloWorld.vcxproj") as vProj:
    TM.Narrator.Print(vProj.Name)
