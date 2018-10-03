##region Settings
bWriteLog = True
sVisualStudioDTE = "VisualStudio.DTE.15.0"
fClosePIDTimeout = 30
bRetryAttribErrors = True
##endregion

import TM_CommonPy as TM
import VisualStudioAutomation as VS
from VisualStudioAutomation.Global import IsRetryableException
from VisualStudioAutomation.DTEWrapper import DTEWrapper
from VisualStudioAutomation.ProjWrapper import ProjWrapper
from VisualStudioAutomation.SlnWrapper import SlnWrapper
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps_Undo
from VisualStudioAutomation.ConvenienceEtree import SetTMDefaultVSSettings

__version__ = '0.20.0'
