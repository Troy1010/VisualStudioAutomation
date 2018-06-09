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
import VisualStudioAutomation.Narrator as VS_NaR


with VS.OpenProj("res\HelloWorld.vcxproj") as vProj:
    #VS_NaR.Proj(vProj)
    #5:project 24:Configurations vProj.Properties[5].Collection[24]
    vConfig = vProj.ConfigurationManager[0]
    TM.Narrator.Print(vConfig,iRecursionThreshold=2,bHideDuplications=False)
