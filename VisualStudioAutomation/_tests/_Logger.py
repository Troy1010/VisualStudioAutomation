import os, logging
##region Settings
bWriteLogFile = True
sLogFile = os.path.join(__file__,'..','VSLog_LogTests.log')
vMasterThreshold = logging.DEBUG
vConsoleHandlerThreshold = logging.WARNING
vFileHandlerThreshold = logging.DEBUG
##endregion
import TM_CommonPy as TM

class HeaderDecorator:
    """Decorator to add a header"""
    bFirstCall=True
    sLastFnName=""
    def __init__(self,method):
        self.method=method
    def __call__(self,*args,**kwargs):
        if __class__.sLastFnName != TM.FnName(1):
            __class__.sLastFnName = TM.FnName(1)
            if __class__.bFirstCall:
                __class__.bFirstCall=False
                self.method("-------"+__class__.sLastFnName)
            else:
                self.method("\n\n-------"+__class__.sLastFnName)
        self.method(*args, **kwargs)

VSLog_LogTests = logging.getLogger(__name__)
VSLog_LogTests.info = HeaderDecorator(VSLog_LogTests.info)
VSLog_LogTests.debug = HeaderDecorator(VSLog_LogTests.debug)
VSLog_LogTests.setLevel(vMasterThreshold)
vFormatter = logging.Formatter('%(message)s')
#---FileHandler
try:
    os.remove(sLogFile)
except (PermissionError,FileNotFoundError):
    pass
if bWriteLogFile:
    bLogFileIsOpen = False
    try:
        os.rename(sLogFile,sLogFile)
    except PermissionError:
        bLogFileIsOpen = True
    except FileNotFoundError:
        pass
    if not bLogFileIsOpen:
        vFileHandler = logging.FileHandler(sLogFile)
        vFileHandler.setFormatter(vFormatter)
        vFileHandler.setLevel(vFileHandlerThreshold)
        VSLog_LogTests.addHandler(vFileHandler)
