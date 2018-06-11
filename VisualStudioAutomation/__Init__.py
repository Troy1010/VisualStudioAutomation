##region Settings
sVisualStudioDTE = "VisualStudio.DTE.15.0"
bDebug = False
##endregion
##region Imports
import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
import sys, os
import xml.etree.ElementTree
import win32com.client, pywintypes
import time
import VisualStudioAutomation.Narrator
from retrying import retry
##endregion
##region Notes
#VisualStudio's DTE(DevelopTimeEnvironment) throws errors if it receives multiple requests.
#To get around this issue, I've decorated functions that use the DTE with retry.
##endregion

vActiveDTE = None
#------Public
class OpenDTE():
    def __enter__(self):
        self.bInstantiatedDTE = False
        global vActiveDTE
        if vActiveDTE is None:
            self.bInstantiatedDTE = True
            vActiveDTE = self.InstantiateDTE()
        else:
            raise Exception("There is already an active DTE.")
        return vActiveDTE
    def __exit__(self, type, value, traceback):
        global vActiveDTE
        if self.bInstantiatedDTE:
            self.QuitDTE(vActiveDTE)
            vActiveDTE = None
    @staticmethod
    @retry(stop_max_delay=10000)
    def InstantiateDTE():
        global sVisualStudioDTE
        return win32com.client.Dispatch(sVisualStudioDTE)
    @staticmethod
    @retry(stop_max_delay=10000)
    def QuitDTE(vDTE):
        vDTE.Solution.Close()
        vDTE.Quit()

class OpenProj():
    def __init__(self,sProjPath,bSave=True):
        self.bSave = bSave
        self.sProjPath = sProjPath
        #-
        self.bQuitDTE = False
        global vActiveDTE
        if vActiveDTE is None:
            self.bQuitDTE = True
            vActiveDTE = OpenDTE.InstantiateDTE()
    def __enter__(self):
        self.vProj = self.OpenProj(self.sProjPath)
        return self.vProj
    def __exit__(self, errtype, value, traceback):
        global vActiveDTE
        if not errtype:
            if self.bSave:
                self.vProj.Save()
            if self.bQuitDTE:
                OpenDTE.QuitDTE(vActiveDTE)
                vActiveDTE = None
    @staticmethod
    @retry(stop_max_delay=10000)
    def OpenProj(sProjPath):
        #---Open
        sProjPath = os.path.abspath(sProjPath)
        #---Filter
        if not os.path.isfile(sProjPath):
            raise ValueError("sProjPath does not exist:"+sProjPath)
        if vActiveDTE is None:
            raise Exception("vActiveDTE is None. Try using "+TM.FnName()+" within a context manager such as \"with OpenDTE():\"")
        #---
        return vActiveDTE.Solution.AddFromFile(sProjPath)

@retry(stop_max_delay=10000)
def OpenSolution(sSolution):
    #---Open
    sSolution = os.path.abspath(sSolution)
    #---Filter
    if not os.path.isfile(sSolution):
        raise ValueError("sSolution does not exist:"+sSolution)
    if vActiveDTE is None:
        raise Exception("vActiveDTE is None. Try using "+TM.FnName()+" within a context manager such as \"with OpenDTE():\"")
    #---
    vActiveDTE.Solution.Open(sSolution)
    return vActiveDTE.Solution


@retry(stop_max_delay=10000)
def AddFileToProj(vProj,sFileToAdd,sFilter=""):
    #---Open
    sFileToAdd = os.path.abspath(sFileToAdd)
    #---Filter
    if not os.path.isfile(sFileToAdd):
        raise ValueError("sFileToAdd does not exist:"+sFileToAdd)
    if not str(type(vProj)) == "<class 'win32com.client.CDispatch'>":
        raise ValueError("vProj is not the right type:"+str(type(vProj)))
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
                    break
        return vFilter.AddFile(sFileToAdd)

@retry(stop_max_delay=10000)
def RemoveFileFromProj(vProj,sFileToRemove,bTry=False):
    #---Open
    sFileToRemove = os.path.abspath(sFileToRemove)
    #---
    try:
        vFile = vProj.Object.Files.Item(sFileToRemove)
    except:
        if not bTry:
            raise Exception(TM.FnName()+"`Could not find file:"+sFileToRemove)
#    try:
    vProj.Object.RemoveFile(vFile)
#    except:
#        raise Exception(TM.FnName()+"`Could not remove file:"+sFileToRemove)

@retry(stop_max_delay=10000)
def AddFilterToProj(vProj,sFilterName):
    return vProj.Object.AddFilter(sFilterName)

@retry(stop_max_delay=10000)
def FilterProjectItem(vProjItem,sFilterName):
    vProj = vProjItem.ProjectItems.ContainingProject
    sFile = os.path.abspath(vProjItem.Name)
    vProj.Object.RemoveFile(vProjItem.Object)
    AddFileToProj(vProj,sFile,sFilterName)

@retry(stop_max_delay=10000)
def AddProjRef(vProj,vProjToReference):
    vProj.Object.AddProjectReference(vProjToReference)



##region XML
def _ElementFromGeneratedBuildInfoFile(sConsumerProjFile,sPropsFile):
    sRelPath=os.path.relpath(sPropsFile,os.path.dirname(sConsumerProjFile))
    return xml.etree.ElementTree.Element(r"Import", Project=sRelPath, Condition=r"Exists('"+sRelPath+r"')")
#------Public

##region Convenience
class SetTMDefaultSettings:
    @staticmethod
    def Do(sProj):
        with TM.ElementTreeContext(sProj) as vTree:
            TM.AppendElemIfAbsent(*SetTMDefaultSettings._OutDir_ArgsForAppend(vTree))
            TM.AppendElemIfAbsent(*SetTMDefaultSettings._IntDir_ArgsForAppend(vTree))
    @staticmethod
    def Undo(sProj):
        with TM.ElementTreeContext(sProj) as vTree:
            TM.RemoveElem(*SetTMDefaultSettings._OutDir_ArgsForAppend(vTree))
            TM.RemoveElem(*SetTMDefaultSettings._IntDir_ArgsForAppend(vTree))

    @staticmethod
    def _OutDir_ArgsForAppend(vTree):
        vElemGlobalsTemplate = xml.etree.ElementTree.Element(r"PropertyGroup", Label="Globals") #<PropertyGroup Label="Globals">
        vElemGlobals = TM.FindElem(vElemGlobalsTemplate,vTree)
        vOutDirElem = xml.etree.ElementTree.Element(r"OutDir") #<OutDir>$(SolutionDir)bin\$(Platform)\$(Configuration)\</OutDir>
        vOutDirElem.text = r"$(SolutionDir)bin\$(Platform)\$(Configuration)\\"
        return (vOutDirElem,vElemGlobals)

    @staticmethod
    def _IntDir_ArgsForAppend(vTree):
        vElemGlobalsTemplate = xml.etree.ElementTree.Element(r"PropertyGroup", Label="Globals") #<PropertyGroup Label="Globals">
        vElemGlobals = TM.FindElem(vElemGlobalsTemplate,vTree)
        vIntDirElem = xml.etree.ElementTree.Element(r"IntDir") #<IntDir>$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\</IntDir>
        vIntDirElem.text = r"$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\\"
        return (vIntDirElem,vElemGlobals)


# def SetTMDefaultSettings(sProj):
#     with TM.ElementTreeContext(sProj) as vTree:
#         ##region OutDir,IntDir
#         vElemGlobalsTemplate = xml.etree.ElementTree.Element(r"PropertyGroup", Label="Globals") #<PropertyGroup Label="Globals">
#         vElemGlobals = TM.FindElem(vElemGlobalsTemplate,vTree)
#         vElemToInsert1 = xml.etree.ElementTree.Element(r"OutDir") #<OutDir>$(SolutionDir)bin\$(Platform)\$(Configuration)\</OutDir>
#         vElemToInsert1.text = "$(SolutionDir)bin\$(Platform)\$(Configuration)\\"
#         vElemToInsert2 = xml.etree.ElementTree.Element(r"IntDir") #<IntDir>$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\</IntDir>
#         vElemToInsert2.text = "$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\\"
#         TM.AppendIfAbsent(vElemToInsert1,vElemGlobals)
#         TM.AppendIfAbsent(vElemToInsert2,vElemGlobals)
#         ##endregion
##endregion

def IntegrateProps(sConsumerProjFile,sPropsFile):
    with TM.ElementTreeContext(sConsumerProjFile) as vTree:
        #---define vToInsert. example: <Import Project="..\packages\OBSEPluginDevPackage.1.0.1\build\native\OBSEPluginDevPackage.targets" Condition="Exists('..\packages\OBSEPluginDevPackage.1.0.1\build\native\OBSEPluginDevPackage.targets')" />
        vToInsert = _ElementFromGeneratedBuildInfoFile(sConsumerProjFile,sPropsFile)
        #---Find position of vElementToInsertAt
        vElemToInsertAt = TM.FindElem(xml.etree.ElementTree.Element(r"ImportGroup", Label="ExtensionSettings"),vTree)
        #---Check if vToInsert already exists
        if not TM.FindElem(vToInsert,vElemToInsertAt) is None:
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
            return
        #---remove vToRemove
        vToRemoveFrom.remove(vToRemove)
##endregion
