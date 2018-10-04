##region Imports
import TM_CommonPy as TM
import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys
import xml.etree.ElementTree
import win32com.client, pywintypes
import time
from retrying import retry
import win32process
import psutil
import logging, os
from VisualStudioAutomation._Logger import VSALog
##endregion
##region Private
def _ElementFromGeneratedBuildInfoFile(sProjFile,sPropsFile):
    sRelPath=os.path.relpath(sPropsFile,os.path.dirname(sProjFile))
    return xml.etree.ElementTree.Element(r"Import", Project=sRelPath, Condition=r"Exists('"+sRelPath+r"')") #<Import Condition="Exists('..\conanbuildinfo.props')" Project="..\conanbuildinfo.props" />
##endregion

class SetTMDefaultVSSettings:
    @classmethod
    def Do(myClass,sProj):
        with TM.ElementTreeContext(sProj) as vTree:
            TM.AppendElemIfAbsent(*myClass._OutDir_ForBothDoAndUndo(vTree))
            TM.AppendElemIfAbsent(*myClass._IntDir_ForBothDoAndUndo(vTree))
    @classmethod
    def Undo(myClass,sProj):
        with TM.ElementTreeContext(sProj) as vTree:
            TM.RemoveElem(*myClass._OutDir_ForBothDoAndUndo(vTree))
            TM.RemoveElem(*myClass._IntDir_ForBothDoAndUndo(vTree))

    @staticmethod
    def _OutDir_ForBothDoAndUndo(vTree):
        vElemGlobalsTemplate = xml.etree.ElementTree.Element(r"PropertyGroup", Label="Globals") #<PropertyGroup Label="Globals">
        vElemGlobals = TM.FindElem(vElemGlobalsTemplate,vTree)
        vOutDirElem = xml.etree.ElementTree.Element(r"OutDir") #<OutDir>$(SolutionDir)bin\$(Platform)\$(Configuration)\</OutDir>
        vOutDirElem.text = r"$(SolutionDir)bin\$(Platform)\$(Configuration)\\"
        return (vOutDirElem,vElemGlobals)

    @staticmethod
    def _IntDir_ForBothDoAndUndo(vTree):
        vElemGlobalsTemplate = xml.etree.ElementTree.Element(r"PropertyGroup", Label="Globals") #<PropertyGroup Label="Globals">
        vElemGlobals = TM.FindElem(vElemGlobalsTemplate,vTree)
        vIntDirElem = xml.etree.ElementTree.Element(r"IntDir") #<IntDir>$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\</IntDir>
        vIntDirElem.text = r"$(SolutionDir)bin\intermediates\$(Platform)\$(Configuration)\\"
        return (vIntDirElem,vElemGlobals)

def IntegrateProps(sProjFile,sPropsFile):
    with TM.ElementTreeContext(sProjFile) as vTree:
        vToInsert = _ElementFromGeneratedBuildInfoFile(sProjFile,sPropsFile)
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

def SetIncludeDir(sProjFile,sIncludeDir):
    with TM.ElementTreeContext(sProjFile) as vTree:
        #---Create insertable elem
        vElemToInsert = xml.etree.ElementTree.Element("ItemDefinitionGroup")
        xml.etree.ElementTree.SubElement(vElemToInsert, "ClCompile")
        xml.etree.ElementTree.SubElement(vElemToInsert[0], "AdditionalIncludeDirectories")
        vElemToInsert[0][0].text = sIncludeDir
        VSALog.debug("SetIncludeDir`vElemToInsert:"+TM.Narrate(vElemToInsert))
        #---Find where to insert
        vElemToInsertAt = vTree.getroot()
        #---Insert
        TM.AppendElemIfAbsent(vElemToInsert,vElemToInsertAt)
