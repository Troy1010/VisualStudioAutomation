##region Settings
bPause = True
##endregion

import TM_CommonPy as TM
import os
import subprocess

try:
    sEvalExr = '(count < 1 and VisualStudioAutomation_Tests) or (count < 0 and VSA_ConvenienceEtree_Tests)'
    subprocess.run(['python','setup.py','nosetests','--tests','VisualStudioAutomation._tests','--stop','--verbosity=3','--eval-attr',sEvalExr])
except Exception as e:
    print(e)
    os.system('pause')
    raise
if bPause:
    print("\n\t\t\tDone\n")
    os.system('pause')
