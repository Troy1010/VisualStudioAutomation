import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys, os
import xml.etree.ElementTree

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

#For all configs
def SetOutputDir(sProj,sOutputDir):
    pass

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
