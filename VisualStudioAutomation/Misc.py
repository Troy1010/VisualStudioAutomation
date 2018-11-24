##region Imports
import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys
import xml.etree.ElementTree
import win32com.client, pywintypes
import time
import win32process
import psutil
import logging, os
from retrying import retry
import VisualStudioAutomation as VS
from VisualStudioAutomation._Logger import VSALog
##endregion

class CorruptSolution(Exception):
    """Solution wasn't loaded correctly"""

def IsRetryableException(e):
    """Some of these might be real errors or they might be a product of a multithread error."""
    """Since we can't tell the difference, we might want to retry them all."""
    if isinstance(e,CorruptSolution):
        VSALog.debug("Retrying "+e.__class__.__name__+" exception:"+str(e))
        return True
    elif isinstance(e,pywintypes.com_error):
        if hasattr(e,"hresult"):
            if e.hresult == -2147418111: #Call was rejected by callee.
                return True
            elif e.hresult == -2147023170: #The remote procedure call failed.
                return True
            elif e.hresult == -2146959355: #Server execution failed
                return True
            elif VS.bRetryGenericCOMErrors and e.hresult == -2147352567: #GenericCOMError
                VSALog.debug("Retrying GenericCOMError")
                return True
    elif isinstance(e,AttributeError):
        #Might be the mutlithread bug, might be a true attrib error.
        if VS.bRetryAttribErrors:
            return True
        else:
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
    elif VS.bRetryTypeErrors and isinstance(e,TypeError):
        VSALog.debug("Retrying TypeError")
        return True
    return False

def MakeProjectPathsRelativeInSlnFile(sSlnFile):
    with open(sSlnFile, 'r+') as vSlnFile:
        cLines = vSlnFile.readlines()
        vSlnFile.seek(0)
        bStartSkipping = False
        for sLine in cLines:
            if "Project" == sLine[:7]:
                iDoubleQuotesPos = sLine.find("\"",sLine.find(","))
                sOldPath = sLine[iDoubleQuotesPos+1:sLine.find("\"",iDoubleQuotesPos+1)]
                sNewPath = os.path.relpath(sOldPath)
                sLine = sLine.replace(sOldPath,sNewPath,1)
            vSlnFile.write(sLine)
        vSlnFile.truncate()

def RemoveProjectFromSlnFile(sSlnFile, sProjFile):
    with open(sSlnFile, 'r+') as vSlnFile:
        cLines = vSlnFile.readlines()
        vSlnFile.seek(0)
        bStartSkipping = False
        for sLine in cLines:
            if "Project" == sLine[:7] and os.path.basename(sProjFile) in sLine:
                bStartSkipping = True
            elif bStartSkipping:
                bStartSkipping = False
                if not "EndProject" in sLine:
                    VSALog.warning("Expected EndProject at line:"+sLine)
            else:
                vSlnFile.write(sLine)
        vSlnFile.truncate()

@retry(retry_on_exception=IsRetryableException,stop_max_delay=10000)
def FindByPath(vContainer,vItem):
    if isinstance(vItem,str):
        vItem = os.path.abspath(vItem)
    else:
        vItem = os.path.abspath(vItem.RelativePath)
    vItemReturning = None
    for vPossibleMatch in vContainer:
        if hasattr(vPossibleMatch,"RelativePath") and os.path.abspath(vPossibleMatch.RelativePath) == vItem:
            if vItemReturning is None:
                vItemReturning = vPossibleMatch
            else:
                VSALog.warning(TM.FnName()+"`matched multiple times.")
    return vItemReturning

@retry(retry_on_exception=IsRetryableException,stop_max_delay=10000)
def Find(vContainer,vItem):
    if isinstance(vItem,str):
        vItem = os.path.splitext(os.path.basename(vItem))[0]
    else:
        vItem = vItem.Name
    vItemReturning = None
    for vPossibleMatch in vContainer:
        if os.path.splitext(vPossibleMatch.Name)[0] == vItem:
            if vItemReturning is None:
                vItemReturning = vPossibleMatch
            else:
                VSALog.warning(TM.FnName()+"`matched multiple times.")
    return vItemReturning
