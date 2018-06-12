import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS
import win32process
import psutil
import time
import logging



#logging.basicConfig(filename='C:\TMinus1010_Local\Coding\Python\VisualStudioAutomation\VisualStudioAutomation\example.log',level=logging.DEtBUG)
#logging.debug("hi")


# fWaitDuration = -0.1
# while True: #psutil.pid_exists(PID):
#     fWaitDuration += 0.1
#     if fWaitDuration > 60:
#         raise Exception("Timed out while waiting for PID to close.")
#     time.sleep(0.1)


# with TM.CopyContext("res/Examples_Backup","res/Examine"):
#     print(os.popen("tasklist").readlines())
#     print("++++++++++++++++++++++")
#     with VS.OpenDTE() as vDTE:
#         print(os.popen("tasklist").readlines())
# #         #TM.Narrator.Print(vDTE.ActiveWindow,iRecursionThreshold=4)
# #         TM.Narrator.Print(vDTE.Debugger.LocalProcesses,iRecursionThreshold=2)
# #         #vDTE.GetObject("Debugger")
#         cPIDs = win32process.GetWindowThreadProcessId(vDTE.ActiveWindow.HWnd)
#         print(str(cPIDs))
# #
# #         if psutil.pid_exists(cPIDs[1]):
# #             print("EXISTS:"+str(cPIDs[1]))
# #         else:
# #             print("Does not exist")
# #         #vDTE.Windows.CreateToolWindow()
#     while psutil.pid_exists(cPIDs[1]):
#         print("waiting..")
#         time.sleep(0.1)
#     print("DONE WAITING!")
# # #Debug.ListProcesses
