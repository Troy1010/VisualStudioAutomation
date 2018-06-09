import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree

import TM_CommonPy as TMC
import TM_CommonPy.Narrator as TMC_NAR
import VisualStudioAutomation as VSA
import subprocess, win32com

import win32com.client
import time

class CopyContext:
    def __init__(self,sFolder,sSource='Examples_Backup',bDeleteAfter=True,bCDInto=True):
        if bCDInto and not os.path.isdir(sSource):
            raise ValueError("bCDInto is true but sSource is not a directory:"+sSource)
        self.bCDInto = bCDInto
        self.bDeleteAfter = bDeleteAfter
        self.sFolder = sFolder
        self.sSource = sSource
    def __enter__(self):
        TMC.Copy(self.sSource,self.sFolder,bPreDelete=True)
        if self.bCDInto:
            os.chdir(self.sFolder)
    def __exit__(self,errtype,value,traceback):
        if self.bCDInto:
            os.chdir('..')
        if self.bDeleteAfter:
            shutil.rmtree(self.sFolder)


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
        with CopyContext('test_OpenProj',bDeleteAfter=False):
            with VSA.OpenProj("HelloWorld.vcxproj",bSave=False) as vProj:
                pass

    def test_AddFileToProj(self):
        with CopyContext('test_AddFileToProj',bDeleteAfter=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                VSA.AddFileToProj(vProj,"HelloWorld3.cpp")

    def test_AddFileToProj_WithFilter(self):
        with CopyContext('test_AddFileToProj_WithFilter',bDeleteAfter=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                VSA.AddFileToProj(vProj,"HelloWorld3.cpp","Filter09")

    def test_FilterProjectItem(self):
        with CopyContext('test_FilterProjectItem',bDeleteAfter=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                vProjItem = VSA.AddFileToProj(vProj,"HelloWorld3.cpp")
                VSA.FilterProjectItem(vProjItem,"Filter45")

    def test_AddFilterToProj(self):
        with CopyContext('test_AddFilterToProj',bDeleteAfter=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                VSA.AddFilterToProj(vProj,"Filter54")

    def test_AddProjRef(self):
        with CopyContext('test_AddProjRef',bDeleteAfter=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                with VSA.OpenProj("HelloWorld2.vcxproj") as vProfToReference:
                    VSA.AddProjRef(vProj,vProfToReference)

    def test_AddFileToProj2(self):
        with CopyContext('test_AddFileToProj2',bDeleteAfter=False):
            with VSA.OpenProj("HelloWorld.vcxproj") as vProj:
                VSA.AddFileToProj(vProj,"HelloWorld2.cpp","obse")
#                VSA.AddFileToProj(vProj,"HelloWorld3.cpp","obse")
