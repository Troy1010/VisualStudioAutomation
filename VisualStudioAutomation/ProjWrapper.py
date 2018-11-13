##region Imports
import VisualStudioAutomation as VS
from VisualStudioAutomation._Logger import VSALog
import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys
import xml.etree.ElementTree
import win32com.client, pywintypes
import time
import VisualStudioAutomation as VS
from retrying import retry
import win32process
import psutil
import logging, os
##endregion

class ProjWrapper():
    vProj = None
    def __init__(self,vParentDTEWrapper,sProjFile,bSave=True,bRemove=False):
        self.vParentDTEWrapper = vParentDTEWrapper
        self.sProjFile = sProjFile
        self.bSave = bSave
        self.bRemove = bRemove
        try:
            self.vProj = self._RetryOpenProj(sProjFile)
        except:
            VSALog.error("Error while opening:" + os.path.abspath(sProjFile))
            raise
    def __enter__(self):
        return self
    def __exit__(self, errtype, value, traceback):
        self.Close()
    def Close(self):
        if not self.vProj is None:
            if self.bSave and hasattr(self.vProj,"Save"):
                self.Save()
            if self.bRemove:
                self.Remove()
            self.vProj = None

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def AddFile(self,sFileToAdd,sFilter=""):
        #---Open
        sFileToAdd = os.path.abspath(sFileToAdd)
        #---Filter
        if not os.path.isfile(sFileToAdd):
            raise OSError(2, 'No such sFileToAdd', sFileToAdd)
        #---
        if sFilter == "":
            return self.vProj.ProjectItems.AddFromFile(sFileToAdd)
        else:
            if self.vProj.Object.CanAddFilter(sFilter):
                vFilter = self.vProj.Object.AddFilter(sFilter)
            else:
                for i in range(1,self.vProj.Object.Filters.Count+1):
                    if self.vProj.Object.Filters.item(i).Name == sFilter:
                        vFilter = self.vProj.Object.Filters.item(i)
                        break
            return vFilter.AddFile(sFileToAdd)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def RemoveFile(self,sFileToRemove,bTry=True):
        #---Open
        sFileToRemove = os.path.abspath(sFileToRemove)
        #---Filter
        #The DTE raises useless exceptions, so we must look before we leap.
        if not os.path.isfile(sFileToRemove):
            if bTry:
                return
            else:
                raise OSError(2, 'No such sFileToRemove', sFileToRemove)
        #---
        try:
            vFile = self.vProj.Object.Files.Item(sFileToRemove)
        except Exception as e:
            if VS.IsRetryableException(e):
                raise
            else:
                s = "Could not retrieve vFile with sFileToRemove:"+sFileToRemove
                if not bTry:
                    s += "\nYou might be trying to remove a file that doesn't exist in the project."
                    s += "\nTry passing bTry=True a parameter to RemoveFile."
                raise type(e)(s) from e
        self.vProj.Object.RemoveFile(vFile)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def AddFilter(self,sFilterName):
        return self.vProj.Object.AddFilter(sFilterName)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def AddProjRef(self,vProjToReference):
        for vItem in self.vProj.Object.References:
            if vItem.Name == vProjToReference.Name:
                VSALog.debug("Project reference("+vProjToReference.Name+") already exists.")
                return
        self.vProj.Object.AddProjectReference(vProjToReference)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def RemoveProjRef(self,vProjToUnreference):
        cToRemove = []
        for vItem in self.vProj.Object.References:
            if vItem.Name == vProjToUnreference.Name:
                cToRemove.append(vItem)
        for vItem in cToRemove:
            vItem.Remove()

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def Save(self):
        VSALog.debug("Saving project.")
        self.vProj.Save()

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def Remove(self):
        self.vParentDTEWrapper.vDTE.Solution.Remove(self.vProj)

    ##region Private
    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def _RetryOpenProj(self,sProjFile):
        #---Open
        sProjFile = os.path.abspath(sProjFile)
        #---Filter
        #The DTE raises useless exceptions, so we must look before we leap.
        if not os.path.isfile(sProjFile):
            raise OSError(2, 'No such Project file', sProjFile)
        #---
        try:
            vProj = self.vParentDTEWrapper.vDTE.Solution.AddFromFile(sProjFile)
            return vProj
        except pywintypes.com_error as e:
            if e.hresult == -2147352567: #Generic error, presumably because Solution already has file.
                VSALog.debug("len(self.vParentDTEWrapper.vDTE.Solution.Projects):"+str(self.vParentDTEWrapper.vDTE.Solution.Projects.Count))
                for vItem in self.vParentDTEWrapper.vDTE.Solution.Projects:
                    VSALog.debug("vItem.Name:"+str(vItem.Name))
                    sProjectFile = ""
                    if hasattr(vItem,"ProjectFile"):
                        if vItem.ProjectFile == sProjFile:
                            return vItem
                    elif hasattr(vItem,"Properties") and "ProjectFile" in TM.COM.COMCollectionToDict(vItem.Properties).keys(): #hasattr(vItem.Properties,"ProjectFile") has unexpected results
                        VSALog.debug("COMPARE("+str(bool(TM.COM.COMCollectionToDict(vItem.Properties)['ProjectFile'] == sProjFile))+"):"+TM.COM.COMCollectionToDict(vItem.Properties)["ProjectFile"]+" : "+sProjFile)
                        VSALog.debug("TM.COM.COMCollectionToDict(vItem.Properties)['ProjectFile']:"+TM.Narrate(TM.COM.COMCollectionToDict(vItem.Properties)["ProjectFile"]))
                        if TM.COM.COMCollectionToDict(vItem.Properties)["ProjectFile"] == sProjFile:
                            return vItem
                    else:
                        VSALog.debug(TM.Narrate(TM.COM.COMCollectionToDict(vItem.Properties)))
                        print("bool1:"+str(hasattr(vItem,"Properties"))+" bool2:"+str(hasattr(vItem.Properties,"ProjectFile")))
                        #VSALog.debug("vItem.Properties(list):"+TM.Narrate(list(vItem.Properties))) #Produced error
                        #VSALog.debug("vItem.Properties:"+TM.Narrate(vItem.Properties))
                        if vItem.Properties is None:
                            VSALog.debug("vItem.Properties is None")
                        else:
                            VSALog.debug("vItem.Properties is NOT None`Open")
                            vVar = list(vItem.Properties)
                            VSALog.debug("vItem.Properties is NOT None`Mid")
                            VSALog.debug("vItem.Properties(list):"+TM.Narrate(vVar))
                            #VSALog.debug("vItem.Properties:"+TM.Narrate(vItem.Properties))
                            VSALog.debug("vItem.Properties is NOT None`Close")
                            #VSALog.debug("vItem.Properties:"+TM.Narrate(vItem.Properties))
                        #vVar = list(vItem.Properties)
                        #VSALog.debug("vItem.Properties(list):"+str(vVar))
                        #VSALog.debug("vItem.Properties.ProjectFile..")
                        #VSALog.debug(str(vItem.Properties.ProjectFile))
                        #VSALog.debug("vItem.Properties.ProjectFile^^")
                        # if sProjectFile != "":
                        #     VSALog.debug("sProjFile did not match:" + sProjectFile)
                        # else:
                        #     VSALog.debug("sProjectFile not found in vItem:" + TM.Narrate(vItem))
                else:
                    VSALog.debug("Error. Could not find:" + sProjFile +" in vDTE.Solution.Projects:" + TM.Narrate(self.vParentDTEWrapper.vDTE.Solution.Projects))
            raise
    ##endregion
