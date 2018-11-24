##region Settings
sVisualStudioDTE = "VisualStudio.DTE.15.0"
fClosePIDTimeout = 30
bRetryAttribErrors = True
bRetryGenericCOMErrors = True
bRetryTypeErrors = True
##endregion

from .Misc import IsRetryableException
from .Misc import RemoveProjectFromSlnFile
from .Misc import Find
from .Misc import FindByPath
from .Misc import CorruptSolution
from .Misc import MakeProjectPathsRelativeInSlnFile
from .DTEWrapper import DTEWrapper
from .ProjWrapper import ProjWrapper
from .SlnWrapper import SlnWrapper
from .ConvenienceEtree import IntegrateProps
from .ConvenienceEtree import IntegrateProps_Undo
from .ConvenienceEtree import SetTMDefaultVSSettings
from .ConvenienceEtree import SetIncludeDir
from .ConvenienceEtree import GetProjectGUID

__version__ = '0.20.0'
