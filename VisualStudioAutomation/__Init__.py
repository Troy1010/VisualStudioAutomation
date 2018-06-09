#-------Settings
sVisualStudioDTE = "VisualStudio.DTE.15.0"
bDebug = False
#-------

import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
import sys, os
import xml.etree.ElementTree
import win32com.client
import time

#WARN!NG! Until MultithreadBugFix is complete, there is a race coniditon

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

vActiveDTE = None
#------Public
#-VisualStudioDevTimeEnvironment
class OpenDTE():
    def __enter__(self):
        self.bQuitDTE = False
        global vActiveDTE
        if vActiveDTE is None:
            self.bQuitDTE = True
            vActiveDTE = self.InstantiateDTE()
        else:
            raise Exception("There is already an active DTE.")
        return vActiveDTE
    def __exit__(self, type, value, traceback):
        global vActiveDTE
        if self.bQuitDTE:
            self.QuitDTE(vActiveDTE)
            vActiveDTE = None
    @staticmethod
    def InstantiateDTE():
        global sVisualStudioDTE
        return win32com.client.Dispatch(sVisualStudioDTE)
    @staticmethod
    def QuitDTE(vDTE):
        vDTE.Solution.Close()
        vDTE.Quit()

#Remember, if you "with OpenProj(), OpenProj()", you'll get a rejection error because of mutlithreading.
class OpenProj():
    def __init__(self,sProjPath,bSave=True,vDTE=None):
        #-
        self.bSave = bSave
        #-
        if sProjPath == "":
            raise ValueError('sProjPath is empty.')
        self.sProjPath = sProjPath
        #-
        self.bQuitDTE = False
        global vActiveDTE
        if vActiveDTE is None:
            self.bQuitDTE = True
            vActiveDTE = OpenDTE.InstantiateDTE()
    def __enter__(self):
        global vActiveDTE
        self.vProj = self.OpenProj(vActiveDTE,self.sProjPath)
        return self.vProj
    def __exit__(self, errtype, value, traceback):
        global vActiveDTE
        if not errtype:
            time.sleep(.300) #helps prevent race condition of multithread bug
            if self.bSave:
                self.vProj.Save()
            if self.bQuitDTE:
                OpenDTE.QuitDTE(vActiveDTE)
                vActiveDTE = None
    @staticmethod
    def OpenProj(vDTE,sProjPath):
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
