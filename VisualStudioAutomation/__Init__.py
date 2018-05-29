import ctypes
from pprint import pprint
import TM_CommonPy as TMC
import sys, os
import xml.etree.ElementTree
import win32com.client
import time

#Remember to use () for all DTE methods. Instead of throwing an exception, they just fizzle.
#MultithreadBugFix isn't complete, so be wary of that.

#---MultithreadBugFix
#VisualStudio's DTE throws an error if multiple threads make requests to it.
#With more work, these functions would reroute those errors so that the DTE is continually prompted until it's ready.

#Nonfunctional
def ActivateMsgHandler():
    sScriptFile = os.path.join(os.getcwd(),'..','..','res','HookMultiThreadMessageHandler.ps1')
    subprocess.Popen(["powershell.exe","-executionpolicy ","bypass","-file",sScriptFile], shell=True)

#Nonfunctional
def Register():
    TMC.RunPowerShellScript(os.path.join(os.getcwd(),'..','..','res','Register.ps1'))

#------Public

def InstantiateDTE():
    return win32com.client.Dispatch("VisualStudio.DTE.15.0")

def QuitDTE(vDTE):
    vDTE.Solution.Close()
    vDTE.Quit()

def OpenProj(vDTE,sProjFile):
    #---Open
    sProjFile = os.path.abspath(sProjFile)
    #---Filter
    if not os.path.isfile(sProjFile):
        raise Exception("sProjFile does not exist:"+sProjFile)
    #---
    return vDTE.Solution.AddFromFile(sProjFile)

def AddFileToProj(vProj,sFileToAdd):
    #---Open
    sFileToAdd = os.path.abspath(sFileToAdd)
    #---Filter
    if not os.path.isfile(sFileToAdd):
        raise Exception("sFileToAdd does not exist:"+sFileToAdd)
    #---
    return vProj.ProjectItems.AddFromFile(sFileToAdd)

def AddFilterToProj(vProj,sFilterName):
    return vProj.Object.AddFilter(sFilterName)

def FilterProjectItem(vProjItem,sFilterName):
    sProjItemName = vProjItem.Name
    vProj = vProjItem.ProjectItems.ContainingProject
    vProj.Object.RemoveFile(vProjItem.Object)
    vFilter = vProj.Object.AddFilter(sFilterName)
    vFilter.AddFile(sProjItemName)

def AddProjRef(vProj,vProjToReference):
    vProj.Object.AddProjectReference(vProjToReference)

#Nonfunctional
def ImportPropsToProj(vProj,sPropFile):
    pass
