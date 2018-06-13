##region Settings
bWriteLog = True
sVisualStudioDTE = "VisualStudio.DTE.15.0"
fClosePIDTimeout = 30
bRetryAttribErrors = True
##endregion


import TM_CommonPy as TM
from VisualStudioAutomation.Global import IsMutlithreadError
from VisualStudioAutomation.DTEWrapper import DTEWrapper
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps_Undo
from VisualStudioAutomation.ConvenienceEtree import SetTMDefaultSettings
import logging, os
import TM_CommonPy as TM

__all__ = ["DTEWrapper"]

__version__ = '0.20.0'

##region Log init
#VisualStudioAutomationLog
VSALog = logging.getLogger('VisualStudioAutomation')
if bWriteLog:
    sLog = os.path.join(__file__,'..','VSALog.log')
    TM.Delete(sLog)
    VSALog.addHandler(logging.FileHandler(sLog))
##endregion
