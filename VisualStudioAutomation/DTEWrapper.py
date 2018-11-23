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

bDTEOpen = False

class DTEWrapper():
    def __init__(self):
        global bDTEOpen
        if bDTEOpen:
            raise Exception("Only one DTE can be open at a time.")
        bDTEOpen = True
        self.vDTE = self._InstantiateDTE()
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
        global bDTEOpen
        bDTEOpen = False

    def OpenProj(self, *args, **kwargs):
        return ProjWrapper(self, *args, **kwargs)

    def OpenSln(self, *args, **kwargs):
        return SlnWrapper(self, *args, **kwargs)

    def GetProjInSln(self, vProjToken):
        return VS.Find(self.vDTE.Solution.Projects,vProjToken)

    ##region Private
    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def _InstantiateDTE(self):
        return win32com.client.Dispatch(VS.sVisualStudioDTE)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def _QuitDTE(self):
        self.vDTE.Solution.Close()
        iPID = win32process.GetWindowThreadProcessId(self.vDTE.ActiveWindow.HWnd)[1] #GetPID after Solution.Close() because Solution.Close() has to wait for GetPID.
        self.vDTE.Quit()
        fTimer = VS.fClosePIDTimeout
        while psutil.pid_exists(iPID):
            try:
                self.vDTE.Solution.Close()
            except Exception as e:
                if e.hresult == -2147417848: #The object invoked has disconnected from its clients.
                    pass
                else:
                    raise
            try:
                self.vDTE.Quit()
            except Exception as e:
                if e.hresult == -2147417848: #The object invoked has disconnected from its clients.
                    pass
                else:
                    raise
            if fTimer < 0:
                raise TimeoutError("Timed out while waiting for PID to close:"+str(iPID))
            fTimer -= 1
            time.sleep(1)
    ##endregion
