#-------Settings
sVisualStudioDTE = "VisualStudio.DTE.15.0"
#-------

import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
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
    TM.RunPowerShellScript(os.path.join(os.getcwd(),'..','..','res','Register.ps1'))

#------Public
#-VisualStudioDevTimeEnvironment
class OpenDTE():
    def __enter__(self):
        self.vDTE = self.InstantiateDTE()
        return self.vDTE
    def __exit__(self, type, value, traceback):
        self.QuitDTE(self.vDTE)
    def InstantiateDTE():
        global sVisualStudioDTE
        return win32com.client.Dispatch(sVisualStudioDTE)
    def QuitDTE(vDTE):
        vDTE.Solution.Close()
        vDTE.Quit()

class OpenProj():
    def __init__(self,sProjPath,bSave=True,vDTE=None):
        self.bSave = bSave
        self.sProjPath = sProjPath
        self.vDTE = vDTE
        self.bQuitDTE = False
    def __enter__(self):
        if self.vDTE is None:
            self.bQuitDTE = True
            self.vDTE = OpenDTE.InstantiateDTE()
        self.vProj = self.OpenProj(self.vDTE,self.sProjPath)
        return self.vProj
    def __exit__(self, type, value, traceback):
        if self.bSave:
            self.vProj.Save()
        if self.bQuitDTE:
            OpenDTE.QuitDTE(self.vDTE)
    def OpenProj(self,vDTE,sProjPath):
        #---Open
        sProjPath = os.path.abspath(sProjPath)
        #---Filter
        if not os.path.isfile(sProjPath):
            raise Exception("sProjPath does not exist:"+sProjPath)
        #---
        return vDTE.Solution.AddFromFile(sProjPath)

def AddFileToProj(vProj,sFileToAdd,sFilter=""):
    #---Open
    sFileToAdd = os.path.abspath(sFileToAdd)
    #---Filter
    if not os.path.isfile(sFileToAdd):
        raise Exception("sFileToAdd does not exist:"+sFileToAdd)
    #---
    if sFilter == "":
        return vProj.ProjectItems.AddFromFile(sFileToAdd)
    else:
        if vProj.Object.CanAddFilter(sFilter):
            vFilter = vProj.Object.AddFilter(sFilter)
        else:
            for i in range(1,vProj.Object.Filters.Count+1):
                if vProj.Object.Filters.item(i).Name == sFilter:
                    vFilter = vProj.Object.Filters.item(i)
        return vFilter.AddFile(sFileToAdd)

def AddFilterToProj(vProj,sFilterName):
    return vProj.Object.AddFilter(sFilterName)

def FilterProjectItem(vProjItem,sFilterName):
    vProj = vProjItem.ProjectItems.ContainingProject
    sFile = os.path.abspath(vProjItem.Name)
    vProj.Object.RemoveFile(vProjItem.Object)
    AddFileToProj(vProj,sFile,sFilterName)

def AddProjRef(vProj,vProjToReference):
    vProj.Object.AddProjectReference(vProjToReference)

#Nonfunctional
def ImportPropsToProj(vProj,sPropFile):
    pass
