import VisualStudioAutomation as VS
import TM_CommonPy as TM


with TM.CopyContext("res/Examples_Backup","res/Examine"):
    VS.Integrator.Integrator().Integrate()
