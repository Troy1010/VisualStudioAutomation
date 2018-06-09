import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator as TM_Nar
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS


with VS.OpenProj("res\\HelloWorld.vcxproj") as vProj:
    TM_Nar.Print(vProj,iRecursionThreshold=3)
