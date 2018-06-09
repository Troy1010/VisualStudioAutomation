import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree

import TM_CommonPy as TM
import TM_CommonPy.Narrator as TM_NAR
import VisualStudioAutomation as VSA
import subprocess, win32com

import win32com.client
import time


class Test_VisualStudioAutomation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('VisualStudioAutomation','tests','res'))

    @classmethod
    def tearDownClass(self):
        os.chdir(os.path.join('..','..','..'))

    # ------Tests

    def test_InstantiateAndQuitDTE(self):
        with VSA.OpenDTE() as vDTE:
            pass

    def test_OpenProj(self):
        with TM.CopyContext('Examples_Backup','test_OpenProj',bPostDelete=False):
            with VSA.OpenProj("HelloWorld.vcxproj",bSave=False) as vProj:
                pass

    def test_AddFileToProj(self):
        with TM.CopyContext('Examples_Backup','test_AddFileToProj',bPostDelete=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                VSA.AddFileToProj(vProj,"HelloWorld3.cpp")

    def test_AddFileToProj_WithFilter(self):
        with TM.CopyContext('Examples_Backup','test_AddFileToProj_WithFilter',bPostDelete=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                VSA.AddFileToProj(vProj,"HelloWorld3.cpp","Filter09")

    def test_FilterProjectItem(self):
        with TM.CopyContext('Examples_Backup','test_FilterProjectItem',bPostDelete=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                vProjItem = VSA.AddFileToProj(vProj,"HelloWorld3.cpp")
                VSA.FilterProjectItem(vProjItem,"Filter45")

    def test_AddFilterToProj(self):
        with TM.CopyContext('Examples_Backup','test_AddFilterToProj',bPostDelete=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                VSA.AddFilterToProj(vProj,"Filter54")

    def test_AddProjRef(self):
        with TM.CopyContext('Examples_Backup','test_AddProjRef',bPostDelete=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                with VSA.OpenProj("HelloWorld2.vcxproj") as vProfToReference:
                    VSA.AddProjRef(vProj,vProfToReference)

    def test_AddFileToProj2(self):
        with TM.CopyContext('Examples_Backup','test_AddFileToProj2',bPostDelete=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                VSA.AddFileToProj(vProj,"HelloWorld2.cpp","obse")
#                VSA.AddFileToProj(vProj,"HelloWorld3.cpp","obse")
