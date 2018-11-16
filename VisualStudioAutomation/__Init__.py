##region Settings
sVisualStudioDTE = "VisualStudio.DTE.15.0"
fClosePIDTimeout = 30
bRetryAttribErrors = True
##endregion

import TM_CommonPy as TM
import VisualStudioAutomation as VS
from VisualStudioAutomation.Misc import IsRetryableException
from VisualStudioAutomation.Misc import RemoveProjectFromSlnFile
from VisualStudioAutomation.Misc import GetProjInContainer
from VisualStudioAutomation.DTEWrapper import DTEWrapper
from VisualStudioAutomation.ProjWrapper import ProjWrapper
from VisualStudioAutomation.SlnWrapper import SlnWrapper
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps
from VisualStudioAutomation.ConvenienceEtree import IntegrateProps_Undo
from VisualStudioAutomation.ConvenienceEtree import SetTMDefaultVSSettings
from VisualStudioAutomation.ConvenienceEtree import SetIncludeDir
from VisualStudioAutomation.ConvenienceEtree import GetProjectGUID

__version__ = '0.20.0'
