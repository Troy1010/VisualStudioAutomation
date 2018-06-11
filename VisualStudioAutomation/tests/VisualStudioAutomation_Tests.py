##region Settings
bSkipSlowTests=False
##endregion
import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree

import TM_CommonPy as TM
import TM_CommonPy.Narrator as TM_NAR
import VisualStudioAutomation as VS
import subprocess, win32com

import win32com.client
import time
import pywintypes
from retrying import retry

bDoOnce = False

@unittest.skipIf(bSkipSlowTests,"SkipSlowTests Setting")
class Test_VisualStudioAutomation(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(Test_VisualStudioAutomation, self).__init__(*args, **kwargs)
        self.failfast = True

    def defaultTestResult(self, *args, **kwargs):
        result = super(Test_VisualStudioAutomation, self).defaultTestResult(*args, **kwargs)
        result.failfast = True
        return result

    def run(self, *args, **kwargs):
        args[0].failfast = True
        return super(Test_VisualStudioAutomation, self).run(*args, **kwargs)

    def tearDown(self):
        pass
        self._outcome.result.failfast = True
    #     global bDoOnce
    #     if not bDoOnce:
    #         bDoOnce = True
    #     else:
    #         self._outcome.result.stop()
    #
    #     #if self._resultForDoCleanups
    #
    #     self._outcome.result.failfast=True
    #
    #     #not self._outcome.result is None and
    # #    TM.MsgBox("self._resultForDoCleanups.wasSuccessful():"+str(self._resultForDoCleanups.wasSuccessful()))
    #     if not self._outcome.result is None and not self._outcome.success:
    #         self._outcome.result.stop()
    #
    #
    #     #self._outcome.failfast = True

    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('VisualStudioAutomation','tests','res'))

    @classmethod
    def tearDownClass(self):
        os.chdir(os.path.join('..','..','..'))

    # ------Tests

    def test_InstantiateAndQuitDTE(self):
        with VS.OpenDTE() as vDTE:
            pass

    def test_OpenProj(self):
        with TM.CopyContext('Examples_Backup',TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj",bSave=False) as vProj:
                pass

    def test_AddFileToProj(self):
        with TM.CopyContext('Examples_Backup',TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFileToProj(vProj,"HelloWorld3.cpp")

    def test_AddFileToProj_WithFilter(self):
        with TM.CopyContext('Examples_Backup',TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFileToProj(vProj,"HelloWorld3.cpp","Filter09")

    def test_FilterProjectItem(self):
        with TM.CopyContext('Examples_Backup',TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                vProjItem = VS.AddFileToProj(vProj,"HelloWorld3.cpp")
                VS.FilterProjectItem(vProjItem,"Filter45")

    def test_AddFilterToProj(self):
        with TM.CopyContext('Examples_Backup',TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFilterToProj(vProj,"Filter54")

    def test_AddProjRef(self):
        with TM.CopyContext('Examples_Backup',TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj, VS.OpenProj("HelloWorld2.vcxproj") as vProjToReference:
                VS.AddProjRef(vProj,vProjToReference)

    def test_AddFileToProj2(self):
        with TM.CopyContext('Examples_Backup',TM.FnName(),bPostDelete=False):
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFileToProj(vProj,"HelloWorld2.cpp","obse")
                VS.AddFileToProj(vProj,"HelloWorld3.cpp","obse")

    def test_AddAndRemoveFileFromProj(self):
        with TM.CopyContext('Examples_Backup',TM.FnName(),bPostDelete=False):
            self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.AddFileToProj(vProj,"HelloWorld2.cpp","obse")
            self.assertTrue(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
            with VS.OpenProj("HelloWorld.vcxproj") as vProj:
                VS.RemoveFileFromProj(vProj,"HelloWorld2.cpp")
            self.assertFalse(TM.IsTextInFile("HelloWorld2.cpp","HelloWorld.vcxproj"))
