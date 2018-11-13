##region Settings
bPause = True
##endregion

import TM_CommonPy as TM
import os
import subprocess

try:
    subprocess.run(['python','setup.py','nosetests','--stop','--verbosity=3','-A','count < 2'])
except Exception as e:
    print(e)
    os.system('pause')
    raise
if bPause:
    print("\n\t\t\tDone\n")
    os.system('pause')
