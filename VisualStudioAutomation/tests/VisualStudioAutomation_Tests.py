##region Settings
bSkipSlowTests=False
bPostDelete=False
##endregion
import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree
import TM_CommonPy as TM
import VisualStudioAutomation as VS

@unittest.skipIf(bSkipSlowTests,"SkipSlowTests Setting")
class Test_VisualStudioAutomation(unittest.TestCase):
    sTestWorkspace = "TestWorkspace/"

    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('VisualStudioAutomation','tests'))
        TM.Delete(self.sTestWorkspace)

    @classmethod
    def tearDownClass(self):
        global bPostDelete
        if bPostDelete:
            TM.Delete(self.sTestWorkspace)
        os.chdir(os.path.join('..','..'))

    # ------Tests

    def test_InstantiateAndQuitDTE(self):
        with VS.OpenDTE() as vDTE:
            pass

    def test_OpenProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj",bSave=False) as vProj:
                pass

    def test_AddFileToProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFileToProj(vProj,"HelloWorld3.cpp")

    def test_AddFileToProj_WithFilter(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFileToProj(vProj,"HelloWorld3.cpp","Filter09")

    def test_FilterProjectItem(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                vProjItem = VS.AddFileToProj(vProj,"HelloWorld3.cpp")
                VS.FilterProjectItem(vProjItem,"Filter45")

    def test_AddFilterToProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFilterToProj(vProj,"Filter54")

    def test_AddProjRef(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                with VS.OpenProj("HelloWorld2.vcxproj") as vProjToReference:
                    VS.AddProjRef(vProj,vProjToReference)

    def test_AddFileToProj2(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFileToProj(vProj,"HelloWorld2.cpp","obse")
                VS.AddFileToProj(vProj,"HelloWorld3.cpp","obse")
            self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            self.assertTrue(TM.IsTextInFile("HelloWorld3.cpp","HelloWorld.vcxproj"))

    def test_AddAndRemoveFileFromProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFileToProj(vProj,"HelloWorld2.cpp","obse")
            self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.RemoveFileFromProj(vProj,"HelloWorld2.cpp")
            self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
