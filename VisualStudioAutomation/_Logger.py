##region Settings
import os
bWriteLog = True
sLogFile = os.path.join(__file__,'..','VSALog.log')
##endregion
##region LogInit
import logging
VSALog = logging.getLogger(__name__)
VSALog.setLevel(logging.DEBUG)
try:
    os.remove(sLogFile)
except (PermissionError,FileNotFoundError):
    pass
if bWriteLog:
    bLogFileIsOpen = False
    try:
        os.rename(sLogFile,sLogFile)
    except PermissionError:
        bLogFileIsOpen = True
    except FileNotFoundError:
        pass
    if not bLogFileIsOpen:
        VSALog.addHandler(logging.FileHandler(sLogFile))
##endregion
