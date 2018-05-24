import ctypes
from pprint import pprint
import TM_CommonPy as TMC
import sys, os
import xml.etree.ElementTree
import win32com.client

def Proj_AddProps():
    pass

def Proj_AddFile():
    pass

def InstantiateDTE():
    return win32com.client.Dispatch("VisualStudio.DTE.15.0")
