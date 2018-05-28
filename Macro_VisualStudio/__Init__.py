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

def QuitDTE(vDTE):
    vDTE.Solution.Close()
    vDTE.Quit()

#------Public

def AddProjObj(vDTE):
    #---Open
    sProjFile = os.path.abspath(sProjFile)
    #---Filter
    if not os.path.isfile(sProjFile):
        raise Exception("sProjFile does not exist:"+sProjFile)
    #---GetProjObj
    vDTE = InstantiateDTE() #Do the DTEs self-destruct?
    return vDTE.Solution.AddFromFile(sProjFile)

def Proj_LinkToProps(sProjFile,sProps):
    #---Open
    sProjFile = os.path.abspath(sProjFile)
    sProps = os.path.abspath(sProps)
    #---Filter
    if not os.path.isfile(sProjFile):
        raise Exception("sProjFile does not exist:"+sProjFile)
    if not os.path.isfile(sProps):
        raise Exception("sProps does not exist:"+sProps)
    #---LinkToProps
    #-Get vProject
    vDTE = InstantiateDTE() #Do the DTEs self-destruct?
    vProject = vDTE.Solution.AddFromFile(sProjFile)
    #-LinkToProps
    #vProject.
    #-Save
    vProject.Save()

#def ProjItem_Filter(sFilterName,vProjectItem,sFile):
#    vProj = vProjectItem.ContainingProject
#    for vFilter in vProj.Filters:
#        vFilter.AddFile(sFile)

#def ProjItem_Filter(sFile,vProjectItem):
#    vProj = vProjectItem.ContainingProject
#    for vFilter in vProj.Filters:
#        vFilter.AddFile(sFile)

#def ProjItem_Filter(sFilterName,vProjItem):
#    vProj = vProjItem.ProjectItems.ContainingProject
#    sProjItemName = vProjItem.Name
#    vFile = vProj.Object.Files.Item(sProjItemName)
#    vProj.Object.RemoveFile(vFile)
#    vFilter = vProj.Object.AddFilter(sFilterName)
#    vFilter.AddFile(sProjItemName)

def AddFilterToProjItem(sFilterName,vProjItem):
    sProjItemName = vProjItem.Name
    vProj = vProjItem.ProjectItems.ContainingProject
    vProj.Object.RemoveFile(vProjItem.Object)
    vFilter = vProj.Object.AddFilter(sFilterName)
    vFilter.AddFile(sProjItemName)

def Proj_Filter2(sFile,sFilterName,vProj):
    sFile = os.path.abspath(sFile)
    vFilter = vProj.Object.AddFilter(sFilterName)
    vFilter.AddFile(sFile)

def Proj_AddFiles(sProjFile,cFilesToAdd):
    cReturning = []
    for vValue in cFilesToAdd:
        vProjectItem = Proj_AddFile(sProjFile,vValue)
        cReturning.append(vProjectItem)
    return cReturning

def Proj_AddFile2(vProj,sFileToAdd):
    vProjectItem = vProj.ProjectItems.AddFromFile(sFileToAdd)
#    vProj.Save()
    return vProjectItem

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
    QuitDTE(vDTE)
    return vProjectItem

def Proj_Filter(sFilterName,vProject):
    vFilter = vProject.Object.project.AddFilter(sFilterName)
    vProject.Save()
    return vFilter
