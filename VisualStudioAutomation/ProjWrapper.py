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
        if VS.GetProjInContainer(self.vProj.Object.References,vProjToReference) is not None:
            VSALog.debug("Project reference("+vProjToReference.Name+") already exists.")
            return
        self.vProj.Object.AddProjectReference(vProjToReference)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def RemoveProjRef(self,vProjToUnreference):
        VS.GetProjInContainer(self.vProj.Object.References,vProjToUnreference).Remove()

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
            if e.hresult != -2147352567: #Generic error, presumably because Solution already has project with the same GUID.
                raise
            sProjectGUID = VS.GetProjectGUID(sProjFile)
            for vItem in self.vParentDTEWrapper.vDTE.Solution.Projects:
                if hasattr(vItem,"object") and hasattr(vItem.object,"ProjectGUID") and vItem.object.ProjectGUID == sProjectGUID:
                    return vItem
            else:
                VSALog.debug("Could not match sProjectGUID:" + sProjectGUID)
            raise
    ##endregion
