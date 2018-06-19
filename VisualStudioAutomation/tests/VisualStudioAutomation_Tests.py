##region Settings
bSkip=False
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
import time

@unittest.skipIf(bSkip,"Skip Setting")
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

    def test_AddFileToProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld3.cpp")
            self.assertTrue(TM.IsTextInFile("HelloWorld3.cpp","HelloWorld.vcxproj"))

    def test_AddFilterToProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFilter("Filter54")
            self.assertTrue(os.path.isfile("HelloWorld.vcxproj.filters"))
            self.assertTrue(TM.IsTextInFile("Filter54","HelloWorld.vcxproj.filters"))

    def test_AddProjRef(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper, vDTEWrapper.OpenProj("HelloWorld2.vcxproj") as vProjToReferenceWrapper:
                vProjWrapper.AddProjRef(vProjToReferenceWrapper.vProj)

    def test_Add2FilesToProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld2.cpp","obse")
                vProjWrapper.AddFile("HelloWorld3.cpp","obse")
            self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            self.assertTrue(TM.IsTextInFile("HelloWorld3.cpp","HelloWorld.vcxproj"))

    def test_AddAndRemoveFileFromProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld2.cpp","Filter67")
            self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            self.assertTrue(os.path.isfile("HelloWorld.vcxproj.filters"))
            self.assertTrue(TM.IsTextInFile("Filter67","HelloWorld.vcxproj.filters"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.RemoveFile("HelloWorld2.cpp")
            self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))

    def test_AddAndRemoveFileFromProj2(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                    self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
                    vProjWrapper.AddFile("HelloWorld2.cpp","Filter45")
                    vProjWrapper.Save()
                    self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
                    self.assertTrue(os.path.isfile("HelloWorld.vcxproj.filters"))
                    self.assertTrue(TM.IsTextInFile("Filter45","HelloWorld.vcxproj.filters"))
                    vProjWrapper.RemoveFile("HelloWorld2.cpp")
                    vProjWrapper.Save()
                    self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))

    def test_AddFile_FileDoesntExist(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper:
                with self.assertRaises(FileNotFoundError):
                    with vDTEWrapper.OpenProj("ZZZZZZZZZHelloWorld.vcxproj") as vProjWrapper:
                        pass
