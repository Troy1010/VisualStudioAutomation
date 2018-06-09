import ctypes
from pprint import pprint
import TM_CommonPy as TMC
import sys, os
import xml.etree.ElementTree

def _ElementFromGeneratedBuildInfoFile(sConsumerProjFile,sPropsFile):
    sRelPath=os.path.relpath(sPropsFile,os.path.dirname(sConsumerProjFile))
    return xml.etree.ElementTree.Element(r"Import", Project=sRelPath, Condition=r"Exists('"+sRelPath+r"')")

#------Public

def IntegrateProps(sConsumerProjFile,sPropsFile,sGenerator="visual_studio"):
    #---Filter
    if sGenerator == "visual_studio":
        pass
    else:
        print("HookBuildInfo|Does not yet support generator: "+sGenerator)
        return
    #---Open sConsumerProjFile
    vTree = xml.etree.ElementTree.parse(sConsumerProjFile)
    #---define vToInsert. example: <Import Project="..\packages\OBSEPluginDevPackage.1.0.1\build\native\OBSEPluginDevPackage.targets" Condition="Exists('..\packages\OBSEPluginDevPackage.1.0.1\build\native\OBSEPluginDevPackage.targets')" />
    vToInsert = _ElementFromGeneratedBuildInfoFile(sConsumerProjFile,sPropsFile)
    #---Find position of vElementToInsertAt
    vElemToInsertAt = TMC.FindElem(xml.etree.ElementTree.Element(r"ImportGroup", Label="ExtensionSettings"),vTree)
    #---Check if vToInsert already exists
    if not TMC.FindElem(vToInsert,vElemToInsertAt) is None:
        print ("HookBuildInfo|sConsumerProjFile already has the element we were going to insert")
        return
    #---Insert
    vElemToInsertAt.append(vToInsert)
    #---Export
    #-Register namespaces, otherwise ElementTree will prepend all elements with the namespace.
    for sKey, vValue in TMC.GetXMLNamespaces(sConsumerProjFile).items():
        xml.etree.ElementTree.register_namespace(sKey, vValue)
    vTree.write(sConsumerProjFile)

def IntegrateProps_Undo(sConsumerProjFile,sPropsFile,sGenerator="visual_studio"):
    #---Filter
    if sGenerator == "visual_studio":
        pass
    else:
        print("HookBuildInfo_Undo|Does not yet support generator: "+sGenerator)
        return
    #---Open sConsumerProjFile
    vTree = xml.etree.ElementTree.parse(sConsumerProjFile)
    #---Find vToRemoveFrom, vToRemove
    vToRemoveFrom = TMC.FindElem(xml.etree.ElementTree.Element(r"ImportGroup", Label="ExtensionSettings"),vTree)
    vToRemove = TMC.FindElem(_ElementFromGeneratedBuildInfoFile(sConsumerProjFile,sPropsFile),vToRemoveFrom)
    #---If not found, exit
    if vToRemove is None:
        print ("HookBuildInfo|WARN|Could not find vToRemove")
        return
    #---remove vToRemove
    vToRemoveFrom.remove(vToRemove)
    #---export
    # Register namespaces, otherwise ElementTree will prepend all elements with the namespace.
    for sKey, vValue in TMC.GetXMLNamespaces(sConsumerProjFile).items():
        xml.etree.ElementTree.register_namespace(sKey, vValue)
    vTree.write(sConsumerProjFile)
