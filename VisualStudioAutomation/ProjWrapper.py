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
                vFilter = VS.Find(self.vProj.Object.Filters,sFilter)
                if vFilter is None:
                    VSALog.debug(TM.FnName()+"`Could not find filter:"+sFilter)
                    return
            return vFilter.AddFile(sFileToAdd)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def RemoveFile(self,sFileToRemove):
        vFile = VS.FindByPath(self.vProj.Object.Files,sFileToRemove)
        if vFile is None:
            VSALog.debug(TM.FnName()+"`File:"+sFileToRemove+" already doesn't exists.")
            return
        self.vProj.Object.RemoveFile(vFile)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def AddFilter(self,sFilterName):
        if VS.Find(self.vProj.Object.Filters,sFilterName) is not None:
            VSALog.debug("AddFilter`Filter:"+sFilterName+" already exists.")
            return
        return self.vProj.Object.AddFilter(sFilterName)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def IsFilterEmpty(self,sFilterName):
        vFilter = VS.Find(self.vProj.Object.Filters,sFilterName)
        if vFilter is None:
            VSALog.debug(TM.FnName()+"`Filter:"+sFilterName+" doesn't exists.")
            return
        return vFilter.Files.Count == 0

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def RemoveFilter(self,sFilterName):
        vFilter = VS.Find(self.vProj.Object.Filters,sFilterName)
        if vFilter is None:
            VSALog.debug(TM.FnName()+"`Filter:"+sFilterName+" already doesn't exists.")
            return
        return self.vProj.Object.RemoveFilter(vFilter)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def AddProjRef(self,vProjToReference):
        if VS.Find(self.vProj.Object.References,vProjToReference) is not None:
            VSALog.debug("AddProjRef`Project reference already exists.")
            return
        self.vProj.Object.AddProjectReference(vProjToReference)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def RemoveProjRef(self,vProjToUnreference):
        if VS.Find(self.vProj.Object.References,vProjToUnreference) is None:
            VSALog.debug("RemoveProjRef`Project reference already doesn't exists.")
            return
        VS.Find(self.vProj.Object.References,vProjToUnreference).Remove()

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
                    VSALog.debug("Solution already had project:" + vItem.Name)
                    return vItem
            else:
                VSALog.debug("Could not match sProjectGUID:" + sProjectGUID)
            raise
    ##endregion
