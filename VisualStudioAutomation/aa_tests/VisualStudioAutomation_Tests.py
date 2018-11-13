##region Settings
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
from nose.plugins.attrib import attr

vCounter = TM.Counter()

class Test_VisualStudioAutomation(unittest.TestCase):
    sTestWorkspace = "TestWorkspace/"

    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('VisualStudioAutomation','aa_tests'))
        TM.Delete(self.sTestWorkspace)

    @classmethod
    def tearDownClass(self):
        global bPostDelete
        if bPostDelete:
            TM.Delete(self.sTestWorkspace)
        os.chdir(os.path.join('..','..'))

    #------Tests

    @unittest.skip("temporarily disabled")
    @attr(count=vCounter())
    def test_OpenDTE(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper:
                with VS.DTEWrapper() as vDTEWrapper2:
                    pass
                pass

    @unittest.skip("temporarily disabled")
    @attr(count=vCounter())
    def test_TwoDTEs(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                    with VS.DTEWrapper() as vDTEWrapper2:
                        with vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper2:
                            pass
                        pass
                    pass
                pass
            pass

    @attr(count=vCounter())
    def test_AddFileToProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld3.cpp")
            self.assertTrue(TM.IsTextInFile("HelloWorld3.cpp","HelloWorld.vcxproj"))

    @attr(count=vCounter())
    def test_AddFilterToProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFilter("Filter54")
            self.assertTrue(os.path.isfile("HelloWorld.vcxproj.filters"))
            self.assertTrue(TM.IsTextInFile("Filter54","HelloWorld.vcxproj.filters"))

    @attr(count=vCounter())
    def test_AddAndRemoveProjRef(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper, vDTEWrapper.OpenProj("HelloWorld2.vcxproj") as vProjToReferenceWrapper:
                self.assertFalse(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))
                vProjWrapper.AddProjRef(vProjToReferenceWrapper.vProj)
                vProjWrapper.Save()
                self.assertTrue(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))
                vProjWrapper.RemoveProjRef(vProjToReferenceWrapper.vProj)
                vProjWrapper.Save()
                self.assertFalse(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))
                vProjWrapper.AddProjRef(vProjToReferenceWrapper.vProj)
                vProjWrapper.Save()
                self.assertTrue(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))
                vProjWrapper.AddProjRef(vProjToReferenceWrapper.vProj)
                vProjWrapper.Save()
                self.assertTrue(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))

    @attr(count=vCounter())
    def test_Add2FilesToProj(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld2.cpp","obse")
                vProjWrapper.AddFile("HelloWorld3.cpp","obse")
            self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            self.assertTrue(TM.IsTextInFile("HelloWorld3.cpp","HelloWorld.vcxproj"))

    @attr(count=vCounter())
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

    @attr(count=vCounter())
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

    @attr(count=vCounter())
    def test_AddFile_FileDoesntExist(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper:
                with self.assertRaises(FileNotFoundError):
                    with vDTEWrapper.OpenProj("NonexistantProject.vcxproj") as vProjWrapper:
                        pass

    @attr(count=vCounter())
    def test_AddProjToSln(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenSln("HelloWorld.sln"):
                    with vDTEWrapper.OpenProj("HelloWorld2.vcxproj") as vProjWrapper:
                        pass

    @attr(count=vCounter())
    def test_RemoveProjFromSln(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    vSlnWrapper.RemoveProj("HelloWorld.vcxproj")

    @attr(count=vCounter())
    def test_GetProjInSlnFromProjString(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    vProj = vSlnWrapper.GetProjInSlnFromProjString("HelloWorld2.vcxproj")
                    self.assertIsNone(vProj)
                    vDTEWrapper.OpenProj("HelloWorld2.vcxproj")
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    vProj = vSlnWrapper.GetProjInSlnFromProjString("HelloWorld2.vcxproj")
                    self.assertIsNotNone(vProj)
                    vSlnWrapper.RemoveProj("HelloWorld2.vcxproj")
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    vProj = vSlnWrapper.GetProjInSlnFromProjString("HelloWorld2.vcxproj")
                    self.assertIsNone(vProj)