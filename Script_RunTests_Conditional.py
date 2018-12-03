import TM_CommonPy as TM
TM.devtools.RunTests(sTestPath="VisualStudioAutomation/_tests", bPause=False, iVerbosity=3,
    sEval='(count < 3 and VisualStudioAutomation_Tests) or (count < 1 and VSA_ConvenienceEtree_Tests)')
