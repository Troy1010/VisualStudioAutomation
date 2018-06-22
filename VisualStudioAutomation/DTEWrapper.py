##region Reminders
#Filters could be exception handlers
##endregion
##region Imports
from VisualStudioAutomation.ProjWrapper import ProjWrapper
import VisualStudioAutomation as VS
#---Non-Local
import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
import sys
import xml.etree.ElementTree
import win32com.client, pywintypes
import time
import VisualStudioAutomation.Narrator
from retrying import retry
import win32process
import psutil
import logging, os
##endregion

class DTEWrapper():
    vDTE = None
    def __init__(self):
        self.vDTE = self._InstantiateDTE()
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.Close()
    def Close(self):
        if not self.vDTE is None:
            self._QuitDTE()
            self.vDTE = None

    def OpenProj(self, *args, **kwargs):
        return ProjWrapper(self, *args, **kwargs)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def OpenSolution(self,sSolution):
        #---Open
        sSolution = os.path.abspath(sSolution)
        #---Filter
        if not os.path.isfile(sSolution):
            raise OSError(2, 'No such Solution file', sSolution)
        #---
        self.vDTE.Solution.Open(sSolution)
        return self.vDTE.Solution

    ##region Private
    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def _InstantiateDTE(self):
        return win32com.client.Dispatch(VS.sVisualStudioDTE)

    @retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
    def _QuitDTE(self):
        self.vDTE.Solution.Close()
        iPID = win32process.GetWindowThreadProcessId(self.vDTE.ActiveWindow.HWnd)[1] #GetPID after Solution.Close() because Solution.Close() has to wait for GetPID, but not visaversa.
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