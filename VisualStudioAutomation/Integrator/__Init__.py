##region Settings
bDebug = False
##endregion
##region Imports
import ctypes
from pprint import pprint
import TM_CommonPy as TM
import TM_CommonPy.Narrator
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS
import TM_CommonPy as TM
##endregion



class Integrator:
    def __init__(self):
        self.cSolutionIntegrations = []
        self.cProjectIntegrations = []

    def Integrate(self):
        with VS.OpenDTE() as vDTE:
            for vSolutionIntegration in self.cSolutionIntegrations:
                VS.OpenSolution(sSolution)
                for sProj in TM.TryGetCollectionAttrib(vSolutionIntegration,"cProjsToIntegrate"):
                    VS.OpenProj.OpenProj(sProj)
            #for vProjectIntegration in self.cProjectIntegrations:



    class SolutionIntegration:
        def __init__(self,sSolution):
            self.sSolution = sSolution
            self.cProjsToIntegrate = []

    class ProjectIntegration:
        def __init__(self,sProj):
            self.sProj = sProj
            self.cToIntegrateProps = []
            self.cToIntegrateProjectReferences = []
            self.cToIntegrateFiles = []
