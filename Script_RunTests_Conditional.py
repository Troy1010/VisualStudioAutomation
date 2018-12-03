import TM_CommonPy as TM
sEval = '(count < 3 and VisualStudioAutomation_Tests) or (count < 1 and VSA_ConvenienceEtree_Tests)'
TM.devtools.RunTests(sTestPath="VisualStudioAutomation/_tests", sEval=sEval, bPause=False)
