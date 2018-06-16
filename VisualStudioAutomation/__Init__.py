##region Settings
bWriteLog = True
sVisualStudioDTE = "VisualStudio.DTE.15.0"
fClosePIDTimeout = 30
bRetryAttribErrors = True
##endregion


##region Log init
#VisualStudioAutomationLog
import logging, os
VSALog = logging.getLogger('VisualStudioAutomation')
if bWriteLog:
    sLogFile = os.path.join(__file__,'..','VSALog.log')
    if os.path.exists(sLogFile):
        os.remove(sLogFile)
    VSALog.addHandler(logging.FileHandler(sLogFile))
##endregion
import TM_CommonPy as TM
from VisualStudioAutomation.Global import IsRetryableException
from VisualStudioAutomation.DTEWrapper import DTEWrapper
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps_Undo
from VisualStudioAutomation.ConvenienceEtree import SetTMDefaultVSSettings

__all__ = ["DTEWrapper"]

__version__ = '0.20.0'
