import ctypes
from pprint import pprint
import TM_CommonPy as TMC
import sys, os
import xml.etree.ElementTree
import win32com.client
import time

#Remember to use () for all DTE methods. Instead of throwing an exception, they just fizzle.

def ActivateMsgHandler():
    #print("os.getcwd(:"+os.getcwd())
    #print("here:"+os.path.join(os.getcwd(),'..','..','res','HookMultiThreadMessageHandler.ps1'))
    #TMC.RunPowerShellScript(os.path.join(os.getcwd(),'..','..','res','HookMultiThreadMessageHandler.ps1'))
    sScriptFile = os.path.join(os.getcwd(),'..','..','res','HookMultiThreadMessageHandler.ps1')
    subprocess.Popen(["powershell.exe","-executionpolicy ","bypass","-file",sScriptFile], shell=True)

def Register():
    TMC.RunPowerShellScript(os.path.join(os.getcwd(),'..','..','res','Register.ps1'))

def InstantiateDTE():
    return win32com.client.Dispatch("VisualStudio.DTE.15.0")

#------Public

def Proj_AddProps():
    pass

def ProjItem_Filter(vProjectItem):
    #vProjectItem.AddFilter()
    pass

def Proj_AddFiles(sProjFile,cFilesToAdd):
    cReturning = []
    for vValue in cFilesToAdd:
        vProjectItem = Proj_AddFile(sProjFile,vValue)
        cReturning.append(vProjectItem)
    return cReturning

def Proj_AddFile(sProjFile,sFileToAdd):
    #---Open
    sProjFile = os.path.abspath(sProjFile)
    sFileToAdd = os.path.abspath(sFileToAdd)
    #---Filter
    if not os.path.isfile(sProjFile):
        raise Exception("sProjFile does not exist:"+sProjFile)
    if not os.path.isfile(sFileToAdd):
        raise Exception("sFileToAdd does not exist:"+sFileToAdd)
    #---
    vDTE = InstantiateDTE() #Do the DTEs self-destruct?
    vProject = vDTE.Solution.AddFromFile(sProjFile)
    vProjectItem = vProject.ProjectItems.AddFromFile(sFileToAdd)
    vProject.Save()
    return vProjectItem

def Filter(vProjectItem):
    pass
