##region Settings
bPause = True
##endregion

import TM_CommonPy as TM
import os
import subprocess

try:
    subprocess.run(['python','setup.py','nosetests','--tests','VisualStudioAutomation.aa_tests','--stop','--verbosity=3','-A','(count < 2 and VisualStudioAutomation_Tests) or (count < 5 and VSA_ConvenienceEtree_Tests)'])
except Exception as e:
    print(e)
    os.system('pause')
    raise
if bPause:
    print("\n\t\t\tDone\n")
    os.system('pause')
