##region Imports
from VisualStudioAutomation.ProjWrapper import ProjWrapper
from VisualStudioAutomation.SlnWrapper import SlnWrapper
import VisualStudioAutomation as VS
from VisualStudioAutomation._Logger import VSALog
#---Non-Local
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
##endregion

class DTEWrapper():
    def __init__(self):
        if self._IsDTEOpen():
            raise Exception("A VisualStudio DTE is already open.")
        self.vDTE = win32com.client.Dispatch(VS.sVisualStudioDTE)
        self.cSlnProjPairToDelete = []
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.Close()
    def Close(self):
        if not self.vDTE is None:
            self._QuitDTE()
            self.vDTE = None
        for vItem in self.cSlnProjPairToDelete:
            VS.RemoveProjectFromSlnFile(*vItem)

    def OpenProj(self, *args, **kwargs):
        return ProjWrapper(self, *args, **kwargs)

    def OpenSln(self, *args, **kwargs):
        return SlnWrapper(self, *args, **kwargs)

    def GetProjInSln(self, vProjToken):
        return VS.Find(self.vDTE.Solution.Projects,vProjToken)

    ##region Private
    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def _GetActiveDTE(self):
        try:
            return win32com.client.GetActiveObject(VS.sVisualStudioDTE)
        except pywintypes.com_error as e:
            if e.hresult == -2147221021: #Operation unavailable, presumably because no DTE is open
                return None
            raise

    def _IsDTEOpen(self):
        return self._GetActiveDTE() is not None

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def _QuitDTE(self):
        self.vDTE.Solution.Close()
        iPID = win32process.GetWindowThreadProcessId(self.vDTE.ActiveWindow.HWnd)[1] #GetPID after Solution.Close() because Solution.Close() has to wait for GetPID.
        self.vDTE.Quit()
        fTimer = VS.fClosePIDTimeout
        while psutil.pid_exists(iPID): #Maybe this could be replaced with _IsDTEOpen.
            try:
                self.vDTE.Solution.Close()
            except pywintypes.com_error as e:
                if e.hresult != -2147417848: #The object invoked has disconnected from its clients.
                    raise
            try:
                self.vDTE.Quit()
            except pywintypes.com_error as e:
                if e.hresult != -2147417848: #The object invoked has disconnected from its clients.
                    raise
            if fTimer < 0:
                raise TimeoutError("Timed out while waiting for PID to close:"+str(iPID))
            fTimer -= 1
            time.sleep(1)
    ##endregion
