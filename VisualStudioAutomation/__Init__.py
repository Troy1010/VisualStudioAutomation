##region Settings
bWriteLog = True
sVisualStudioDTE = "VisualStudio.DTE.15.0"
fClosePIDTimeout = 30
bRetryAttribErrors = True
##endregion

##region LogInit
import logging, os
sLogFile = os.path.join(__file__,'..','VSALog.log')
VSALog = logging.getLogger(__name__)
VSALog.setLevel(logging.DEBUG)
try:
    os.remove(sLogFile)
except (PermissionError,FileNotFoundError):
    pass
if bWriteLog:
    for vHandler in VSALog.handlers:
        try:
            if vHandler.baseFilename == os.path.abspath(sLogFile):
                break
        except AttributeError:
            pass
    else:
        VSALog.addHandler(logging.FileHandler(sLogFile))
##endregion

##region LogInit
import logging, os
sLogFile = os.path.join(__file__,'..','VSALog.log')
if 'VSALog' in locals():
    print("VSALog is in locals")
if 'VSALog' in globals():
    print("VSALog is in globals")
VSALog = logging.getLogger(__name__)
VSALog.setLevel(logging.DEBUG)
bPermissionError = False
try:
    os.remove(sLogFile)
#except (PermissionError,FileNotFoundError):
#    pass
except FileNotFoundError:
    print("FileNotFoundError")
    pass
except PermissionError:
    print("PermissionError")
    bPermissionError = True
else:
    print("Successfully removed")
    if bWriteLog:
        VSALog.addHandler(logging.FileHandler(sLogFile))
VSALog.debug("VSALog init complete")
if bPermissionError:
    VSALog.debug("!!Logging PermissionError")
else:
    VSALog.debug("No PermissionError")
##endregion
import TM_CommonPy as TM
import VisualStudioAutomation as VS
from VisualStudioAutomation.Global import IsRetryableException
from VisualStudioAutomation.DTEWrapper import DTEWrapper
from VisualStudioAutomation.ProjWrapper import ProjWrapper
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps_Undo
from VisualStudioAutomation.ConvenienceEtree import SetTMDefaultVSSettings


__all__ = ["DTEWrapper"]

__version__ = '0.20.0'

VSALog.debug("VSA Init complete")
