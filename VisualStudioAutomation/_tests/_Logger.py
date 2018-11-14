import os, logging
##region Settings
bWriteLogFile = True
sLogFile = os.path.join(__file__,'..','VSLog_LogTests.log')
vMasterThreshold = logging.DEBUG
vConsoleHandlerThreshold = logging.WARNING
vFileHandlerThreshold = logging.DEBUG
##endregion

VSLog_LogTests = logging.getLogger(__name__)
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
