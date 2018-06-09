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
            time.sleep(.500) #helps prevent race condition of multithread bug
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



##region XML
def _ElementFromGeneratedBuildInfoFile(sConsumerProjFile,sPropsFile):
    sRelPath=os.path.relpath(sPropsFile,os.path.dirname(sConsumerProjFile))
    return xml.etree.ElementTree.Element(r"Import", Project=sRelPath, Condition=r"Exists('"+sRelPath+r"')")
#------Public

##region Convenience
def SetTMDefaultSettings(sProj):
    with TM.ElementTreeContext(sProj) as vTree:
        ##region OutDir,IntDir
        vElemGlobalsTemplate = xml.etree.ElementTree.Element(r"PropertyGroup", Label="Globals") #<PropertyGroup Label="Globals">
        vElemGlobals = TM.FindElem(vElemGlobalsTemplate,vTree)
        vElemToInsert1 = xml.etree.ElementTree.Element(r"OutDir") #<OutDir>$(SolutionDir)bin\$(Platform)\$(Configuration)\</OutDir>
        vElemToInsert1.text = "$(SolutionDir)bin\$(Platform)\$(Configuration)\\"
        vElemToInsert2 = xml.etree.ElementTree.Element(r"IntDir") #<IntDir>$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\</IntDir>
        vElemToInsert2.text = "$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\\"
        TM.AppendIfAbsent(vElemToInsert1,vElemGlobals)
        TM.AppendIfAbsent(vElemToInsert2,vElemGlobals)
        ##endregion
##endregion

def IntegrateProps(sConsumerProjFile,sPropsFile):
    with TM.ElementTreeContext(sConsumerProjFile) as vTree:
        #---define vToInsert. example: <Import Project="..\packages\OBSEPluginDevPackage.1.0.1\build\native\OBSEPluginDevPackage.targets" Condition="Exists('..\packages\OBSEPluginDevPackage.1.0.1\build\native\OBSEPluginDevPackage.targets')" />
        vToInsert = _ElementFromGeneratedBuildInfoFile(sConsumerProjFile,sPropsFile)
        #---Find position of vElementToInsertAt
        vElemToInsertAt = TM.FindElem(xml.etree.ElementTree.Element(r"ImportGroup", Label="ExtensionSettings"),vTree)
        #---Check if vToInsert already exists
        if not TM.FindElem(vToInsert,vElemToInsertAt) is None:
            print ("HookBuildInfo|sConsumerProjFile already has the element we were going to insert")
            return
        #---Insert
        vElemToInsertAt.append(vToInsert)

def IntegrateProps_Undo(sConsumerProjFile,sPropsFile):
    with TM.ElementTreeContext(sConsumerProjFile) as vTree:
        #---Find vToRemoveFrom, vToRemove
        vToRemoveFrom = TM.FindElem(xml.etree.ElementTree.Element(r"ImportGroup", Label="ExtensionSettings"),vTree)
        vToRemove = TM.FindElem(_ElementFromGeneratedBuildInfoFile(sConsumerProjFile,sPropsFile),vToRemoveFrom)
        #---If not found, exit
        if vToRemove is None:
            print ("HookBuildInfo|WARN|Could not find vToRemove")
            return
        #---remove vToRemove
        vToRemoveFrom.remove(vToRemove)
##endregion
