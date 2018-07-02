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
from VisualStudioAutomation._Logger import VSALog
##endregion

def IsRetryableException(e):
    if isinstance(e,pywintypes.com_error):
        if hasattr(e,"hresult"):
            if e.hresult == -2147418111: #Call was rejected by callee.
                #VSALog.debug("Retrying after \"Call was rejected\" error")
                return True
            elif e.hresult == -2147023170: #The remote procedure call failed.
                return True
    if isinstance(e,AttributeError):
        #Might be the mutlithread bug, might be a true attrib error.
        if VS.bRetryAttribErrors:
            return True
        else:
            VSALog.debug("MaybeRetryableAttribError:"+TM.Narrator.Narrate(e))
            try:
                sOldMsg = e.args[0]
            except AttributeError:
                sOldMsg = "<CouldntExtractOldMsg>"
            raise type(e)(
                sOldMsg
                +"\nMight be the mutlithread bug, might be a true attrib error."
                +"\nUntil an effective \"Look before you leap\" strategy is developed for this issue,"
                +"\nSetting bRetryAttribErrors=True is recommended. If the exception reoccurs, it is a true attrib error."
                ) from e
    return False
