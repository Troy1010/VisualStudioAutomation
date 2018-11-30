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
from VisualStudioAutomation._tests._Logger import VSLog_LogTests

vCounter = TM.Counter()

class Test_VisualStudioAutomation(unittest.TestCase):
    sTestWorkspace = "_TestWorkspace/"

    @classmethod
    def setUpClass(self):
        self.sOldCWD = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        TM.Delete(self.sTestWorkspace)

    @classmethod
    def tearDownClass(self):
        global bPostDelete
        if bPostDelete:
            TM.Delete(self.sTestWorkspace)
        os.chdir(self.sOldCWD)

    #------Tests

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_VSLog_LogTests_Header(self):
        VSLog_LogTests.info("Hi")
        VSLog_LogTests.debug("Hi")
        VSLog_LogTests.info("Hi")

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_AndAddRemoveProjFromSln(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            self.assertFalse(TM.IsTextInFile(r"HelloWorld2.vcxproj","HelloWorld.sln"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenSln("HelloWorld.sln"):
                vDTEWrapper.OpenProj("HelloWorld2.vcxproj")
            self.assertTrue(TM.IsTextInFile(r"HelloWorld2.vcxproj","HelloWorld.sln"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                vSlnWrapper.RemoveProj("HelloWorld2.vcxproj")
            self.assertFalse(TM.IsTextInFile(r"HelloWorld2.vcxproj","HelloWorld.sln"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_SaveSlnWithoutSmashingProjRelPaths(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_SaveSlnWithoutSmashingProjRelPaths_Backup",bPostDelete=False,bCDInto=True):
            self.assertFalse(TM.IsTextInFile(r"..\..\..\..","HelloWorld.sln"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper, vDTEWrapper.OpenProj("Folder/HelloWorld.vcxproj") as vProjWrapper:
                pass
            self.assertFalse(TM.IsTextInFile(r"..\..\..\..","HelloWorld.sln"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_RemoveSameNameFiles2(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_RemoveSameNameFiles_Backup",bPostDelete=False,bCDInto=True):
            self.assertTrue(TM.IsTextInFile("Folder\\HelloWorld.cpp","HelloWorld.vcxproj"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.RemoveFile("Folder\\HelloWorld.cpp")
            self.assertFalse(TM.IsTextInFile("Folder\\HelloWorld.cpp","HelloWorld.vcxproj"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_RemoveSameNameFiles(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_RemoveSameNameFiles_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.RemoveFile("HelloWorld.h")
            self.assertFalse(TM.IsTextInFile("HelloWorld.h","HelloWorld.vcxproj"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_IsFilterEmpty(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            self.assertFalse(os.path.isfile("HelloWorld.vcxproj.filters"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld2.cpp",sFilter="Filter54")
                self.assertFalse(vProjWrapper.IsFilterEmpty("Filter54"))
            self.assertTrue(TM.IsTextInFile("Filter54","HelloWorld.vcxproj.filters"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.RemoveFile("HelloWorld2.cpp")
                self.assertTrue(vProjWrapper.IsFilterEmpty("Filter54"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_AddAndRemoveFilter(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            self.assertFalse(os.path.isfile("HelloWorld.vcxproj.filters"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFilter("Filter54")
            self.assertTrue(os.path.isfile("HelloWorld.vcxproj.filters"))
            self.assertTrue(TM.IsTextInFile("Filter54","HelloWorld.vcxproj.filters"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.RemoveFilter("Filter54")
            self.assertFalse(TM.IsTextInFile("Filter54","HelloWorld.vcxproj.filters"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_RemoveNonexistantProjRef(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                    vProjWrapper.RemoveProjRef("NonexistantProject.vcxproj")

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_RemoveProjFromSlnWithoutProj_Ghost(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenSln("CompleteControl.sln") as vSlnWrapper:
                    sSlnFile = vSlnWrapper.sSlnFile
                    self.assertTrue("common.vcxproj" in TM.GetFileContent(sSlnFile))
                    vSlnWrapper.RemoveProj(vDTEWrapper.GetProjInSln("common"),bRemoveUnloadedPostDTE=True)
            self.assertFalse("common.vcxproj" in TM.GetFileContent(sSlnFile))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_GetProjInSln_ByName(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenSln("CompleteControl.sln") as vSlnWrapper:
                    VSLog_LogTests.info(TM.Narrate(vSlnWrapper.GetProjInSln("CompleteControl")))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_LogProjectList(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    VSLog_LogTests.info("HelloWorld Projects:"+TM.Narrate(vSlnWrapper.vSln.Projects,iRecursionThreshold=3))
                with vDTEWrapper.OpenSln("CompleteControl.sln") as vSlnWrapper:
                    VSLog_LogTests.info("CompleteControl Projects:"+TM.Narrate(vSlnWrapper.vSln.Projects,iRecursionThreshold=3))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_TwoDTEs(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with self.assertRaises(Exception):
                with VS.DTEWrapper() as vDTEWrapper:
                    with VS.DTEWrapper() as vDTEWrapper2:
                       pass

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_RemoveProjFromSlnByName(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    self.assertFalse(vDTEWrapper.GetProjInSln("HelloWorld") is None)
                    vSlnWrapper.RemoveProj(vDTEWrapper.GetProjInSln("HelloWorld"))
                    self.assertTrue(vDTEWrapper.GetProjInSln("HelloWorld") is None)

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_AddFileToProj(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld3.cpp")
            self.assertTrue(TM.IsTextInFile("HelloWorld3.cpp","HelloWorld.vcxproj"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_AddAndRemoveProjRef(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
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

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_AddAndRemoveProjRef_String(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper, vDTEWrapper.OpenProj("HelloWorld2.vcxproj") as vProjToReferenceWrapper:
                self.assertFalse(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))
                vProjWrapper.AddProjRef(vProjToReferenceWrapper.vProj)
                vProjWrapper.Save()
                self.assertTrue(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))
                vProjWrapper.RemoveProjRef("HelloWorld2.vcxproj")
                vProjWrapper.Save()
                self.assertFalse(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))
                vProjWrapper.AddProjRef(vProjToReferenceWrapper.vProj)
                vProjWrapper.Save()
                self.assertTrue(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))
                vProjWrapper.RemoveProjRef("HelloWorld2")
                vProjWrapper.Save()
                self.assertFalse(TM.IsTextInFile("HelloWorld2","HelloWorld.vcxproj"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_Add2FilesToProj(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld2.cpp","obse")
                vProjWrapper.AddFile("HelloWorld3.cpp","obse")
            self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            self.assertTrue(TM.IsTextInFile("HelloWorld3.cpp","HelloWorld.vcxproj"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_AddAndRemoveFileFromProj(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.AddFile("HelloWorld2.cpp","Filter67")
            self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            self.assertTrue(os.path.isfile("HelloWorld.vcxproj.filters"))
            self.assertTrue(TM.IsTextInFile("Filter67","HelloWorld.vcxproj.filters"))
            with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper:
                vProjWrapper.RemoveFile("HelloWorld2.cpp")
            self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_AddAndRemoveFileFromProj2(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
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

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_AddFile_FileDoesntExist(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper:
                with self.assertRaises(FileNotFoundError):
                    with vDTEWrapper.OpenProj("NonexistantProject.vcxproj") as vProjWrapper:
                        pass

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_GetProjInSlnFromProjString(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_Backup",bPostDelete=False,bCDInto=True):
            with VS.DTEWrapper() as vDTEWrapper:
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    vProj = vSlnWrapper.GetProjInSln("HelloWorld2.vcxproj")
                    self.assertIsNone(vProj)
                    vDTEWrapper.OpenProj("HelloWorld2.vcxproj")
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    vProj = vSlnWrapper.GetProjInSln("HelloWorld2.vcxproj")
                    self.assertIsNotNone(vProj)
                    vSlnWrapper.RemoveProj("HelloWorld2.vcxproj")
                with vDTEWrapper.OpenSln("HelloWorld.sln") as vSlnWrapper:
                    vProj = vSlnWrapper.GetProjInSln("HelloWorld2.vcxproj")
                    self.assertIsNone(vProj)
