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

#The Solution is actually just a collection object belonging to the DTE.
#It doesn't look like there can be multiple open at a time.
class SlnWrapper():
    vSln = None
    def __init__(self,vParentDTEWrapper,sSlnFile,bSave=True):
        self.vParentDTEWrapper = vParentDTEWrapper
        self.sSlnFile = sSlnFile
        self.bSave = bSave
        self.vSln = self._RetryOpenSln(sSlnFile)
    def __enter__(self):
        return self
    def __exit__(self, errtype, value, traceback):
        self.Close()
    def Close(self):
        if not self.vSln is None:
            if self.bSave:
                self.Save()
            self.vSln = None

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def Save(self):
        VSALog.debug("Saving solution.")
        #---Filter
        if not hasattr(self.vSln,"SaveAs"):
            VSALog.debug("Could not save: no SaveAs attr")
            return
        #---
        self.vSln.SaveAs(self.sSlnFile)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def GetProjInSlnByProjFile(self,sProjFile):
        #---Open
        sProjFile = os.path.abspath(sProjFile)
        #---
        for vItem in self.vSln.Projects:
            if hasattr(vItem.Object,"ProjectFile") and vItem.Object.ProjectFile == sProjFile:
                    return vItem

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def RemoveProj(self,vProj,bRemoveUnloaded=False):
        #---Open
        if isinstance(vProj,str):
            vProj = self.GetProjInSlnByProjFile(vProj)
            if vProj is None:
                VSALog.debug("RemoveProj`Could not find project to remove.")
                return
        #---
        try:
            self.vParentDTEWrapper.vDTE.Solution.Remove(vProj)
        except pywintypes.com_error as e:
            if e.hresult != -2147352567: #Generic error, presumably because vProj is unloaded
                raise
            if vProj.Object is None:
                if not bRemoveUnloaded:
                    raise Exception("You have attempted to remove an unloaded project, but the DTE com object has trouble doing that."
                                    "\nSet bRemoveUnloaded to true if you want the project to be removed after the DTE closes.")
                else:
                    self.vParentDTEWrapper.cSlnProjPairToDelete.append((self.sSlnFile,os.path.basename(vProj.UniqueName)))


    ##region Private
    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def _RetryOpenSln(self,sSlnFile):
        #---Open
        sSlnFile = os.path.abspath(sSlnFile)
        #---Filter
        #The DTE raises useless exceptions, so we must look before we leap.
        if not os.path.isfile(sSlnFile):
            raise OSError(2, 'No such Solution file', sSlnFile)
        #---
        self.vParentDTEWrapper.vDTE.Solution.Open(sSlnFile)
        return self.vParentDTEWrapper.vDTE.Solution
    ##endregion
