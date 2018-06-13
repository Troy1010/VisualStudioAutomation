##region Imports
import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
import sys
import xml.etree.ElementTree
import win32com.client, pywintypes
import time
import VisualStudioAutomation.Narrator
import win32process
import psutil
import logging, os
from retrying import retry
import VisualStudioAutomation as VS
##endregion

def IsMutlithreadError(e):
    if isinstance(e,pywintypes.com_error):
        if hasattr(e,"hresult"):
            if e.hresult == -2147418111: #Call was rejected by callee.
                VS.VSALog.debug("Retrying after \"Call was rejected\" error")
                return True
    if isinstance(e,AttributeError):
        #Might be the mutlithread bug, might be a true attrib error.
        #VS.VSALog.warn("Might be multithread bug; might be true attrib error")
        return VS.bRetryAttribErrors
    return True
