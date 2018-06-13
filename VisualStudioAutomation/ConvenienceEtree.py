##region Imports
import TM_CommonPy as TM
import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
import sys
import xml.etree.ElementTree
import win32com.client, pywintypes
import time
import VisualStudioAutomation.Narrator
from retrying import retry
import win32process
import psutil
import logging, os
##endregion
##region Private
def _ElementFromGeneratedBuildInfoFile(sProjFile,sPropsFile):
    sRelPath=os.path.relpath(sPropsFile,os.path.dirname(sProjFile))
    return xml.etree.ElementTree.Element(r"Import", Project=sRelPath, Condition=r"Exists('"+sRelPath+r"')")
##endregion

class SetTMDefaultSettings:
    @staticmethod
    def Do(sProj):
        with TM.ElementTreeContext(sProj) as vTree:
            TM.AppendElemIfAbsent(*SetTMDefaultSettings._OutDir_ArgsForAppendRemove(vTree))
            TM.AppendElemIfAbsent(*SetTMDefaultSettings._IntDir_ArgsForAppendRemove(vTree))
    @staticmethod
    def Undo(sProj):
        with TM.ElementTreeContext(sProj) as vTree:
            TM.RemoveElem(*SetTMDefaultSettings._OutDir_ArgsForAppendRemove(vTree))
            TM.RemoveElem(*SetTMDefaultSettings._IntDir_ArgsForAppendRemove(vTree))

    @staticmethod
    def _OutDir_ArgsForAppendRemove(vTree):
        vElemGlobalsTemplate = xml.etree.ElementTree.Element(r"PropertyGroup", Label="Globals") #<PropertyGroup Label="Globals">
        vElemGlobals = TM.FindElem(vElemGlobalsTemplate,vTree)
        vOutDirElem = xml.etree.ElementTree.Element(r"OutDir") #<OutDir>$(SolutionDir)bin\$(Platform)\$(Configuration)\</OutDir>
        vOutDirElem.text = r"$(SolutionDir)bin\$(Platform)\$(Configuration)\\"
        return (vOutDirElem,vElemGlobals)

    @staticmethod
    def _IntDir_ArgsForAppendRemove(vTree):
        vElemGlobalsTemplate = xml.etree.ElementTree.Element(r"PropertyGroup", Label="Globals") #<PropertyGroup Label="Globals">
        vElemGlobals = TM.FindElem(vElemGlobalsTemplate,vTree)
        vIntDirElem = xml.etree.ElementTree.Element(r"IntDir") #<IntDir>$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\</IntDir>
        vIntDirElem.text = r"$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\\"
        return (vIntDirElem,vElemGlobals)


def IntegrateProps(sProjFile,sPropsFile):
    with TM.ElementTreeContext(sProjFile) as vTree:
        #---define vToInsert. example: <Import Project="..\packages\OBSEPluginDevPackage.1.0.1\build\native\OBSEPluginDevPackage.targets" Condition="Exists('..\packages\OBSEPluginDevPackage.1.0.1\build\native\OBSEPluginDevPackage.targets')" />
        vToInsert = _ElementFromGeneratedBuildInfoFile(sProjFile,sPropsFile)
        #---Find position of vElementToInsertAt
        vElemToInsertAt = TM.FindElem(xml.etree.ElementTree.Element(r"ImportGroup", Label="ExtensionSettings"),vTree)
        #---Check if vToInsert already exists
        if not TM.FindElem(vToInsert,vElemToInsertAt) is None:
            return
        #---Insert
        vElemToInsertAt.append(vToInsert)

def IntegrateProps_Undo(sProjFile,sPropsFile):
    with TM.ElementTreeContext(sProjFile) as vTree:
        #---Find vToRemoveFrom, vToRemove
        vToRemoveFrom = TM.FindElem(xml.etree.ElementTree.Element(r"ImportGroup", Label="ExtensionSettings"),vTree)
        vToRemove = TM.FindElem(_ElementFromGeneratedBuildInfoFile(sProjFile,sPropsFile),vToRemoveFrom)
        #---If not found, exit
        if vToRemove is None:
            return
        #---remove vToRemove
        vToRemoveFrom.remove(vToRemove)
