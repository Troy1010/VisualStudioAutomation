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
    def __init__(self,method):
        self.method=method
        self.sLastFnName=""
        self.bFirstCall=True
    def __call__(self,*args,**kwargs):
        if self.sLastFnName != TM.FnName(1):
            self.sLastFnName = TM.FnName(1)
            if self.bFirstCall:
                self.bFirstCall=False
                self.method("-------"+TM.FnName(1))
            else:
                self.method("\n\n-------"+TM.FnName(1))
        self.method(*args,**kwargs)

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
