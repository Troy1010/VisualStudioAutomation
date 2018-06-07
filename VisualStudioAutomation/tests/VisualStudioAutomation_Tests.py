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

class Test_TM_CommonPy(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('VisualStudioAutomation','tests'))

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        TMC.Copy('Examples_Backup','Examples')
        os.chdir('Examples')

    def tearDown(self):
        os.chdir('..')
        #shutil.rmtree('Examples')

    # ------Tests

    def test_InstantiateAndQuit(self):
        vDTE = VSA.InstantiateDTE()
        VSA.QuitDTE(vDTE)

    def test_OpenProj(self):
        vDTE = VSA.InstantiateDTE()
        vProj = VSA.OpenProj(vDTE,"HelloWorld.vcxproj")
        VSA.QuitDTE(vDTE)

    def test_AddFileToProj(self):
        #---Open
        os.chdir('..')
        TMC.Copy('Examples_Backup','Examples_AddFileToProj',bPreDelete=True)
        os.chdir('Examples_AddFileToProj')
        vDTE = VSA.InstantiateDTE()
        #---
        vProj = VSA.OpenProj(vDTE,"HelloWorld.vcxproj")
        VSA.AddFileToProj(vProj,"HelloWorld3.cpp")
        #---Close
        vProj.Save()
        VSA.QuitDTE(vDTE)

    def test_AddFileToProj_WithFilter(self):
        #---Open
        os.chdir('..')
        TMC.Copy('Examples_Backup','Examples_AddFileToProj_WithFilter',bPreDelete=True)
        os.chdir('Examples_AddFileToProj_WithFilter')
        vDTE = VSA.InstantiateDTE()
        #---
        vProj = VSA.OpenProj(vDTE,"HelloWorld.vcxproj")
        VSA.AddFileToProj(vProj,"HelloWorld3.cpp","Filter09")
        #---Close
        vProj.Save()
        VSA.QuitDTE(vDTE)

    def test_FilterProjectItem(self):
        #---Open
        os.chdir('..')
        TMC.Copy('Examples_Backup','Examples_FilterProjectItem',bPreDelete=True)
        os.chdir('Examples_FilterProjectItem')
        vDTE = VSA.InstantiateDTE()
        #---
        vProj = VSA.OpenProj(vDTE,"HelloWorld.vcxproj")
        vProjItem = VSA.AddFileToProj(vProj,"HelloWorld3.cpp")
        VSA.FilterProjectItem(vProjItem,"Filter45")
        #---Close
        vProj.Save()
        VSA.QuitDTE(vDTE)

    def test_AddFilterToProj(self):
        #---Open
        os.chdir('..')
        TMC.Copy('Examples_Backup','Examples_AddFilterToProj',bPreDelete=True)
        os.chdir('Examples_AddFilterToProj')
        vDTE = VSA.InstantiateDTE()
        vProj = VSA.OpenProj(vDTE,"HelloWorld.vcxproj")
        #---
        VSA.AddFilterToProj(vProj,"Filter54")
        #---Close
        vProj.Save()
        VSA.QuitDTE(vDTE)

    def test_AddProjRef(self):
        #---Open
        os.chdir('..')
        TMC.Copy('Examples_Backup','Examples_AddProjRef',bPreDelete=True)
        os.chdir('Examples_AddProjRef')
        vDTE = VSA.InstantiateDTE()
        vProj = VSA.OpenProj(vDTE,"HelloWorld.vcxproj")
        vProfToReference = VSA.OpenProj(vDTE,"HelloWorld2.vcxproj")
        #---
        VSA.AddProjRef(vProj,vProfToReference)
        #---Close
        vProj.Save()
        VSA.QuitDTE(vDTE)

    def test_AddFileToProj2(self):
        #---Open
        os.chdir('..')
        TMC.Copy('Examples_Backup','Examples_AddFileToProj2',bPreDelete=True)
        os.chdir('Examples_AddFileToProj2')
        vDTE = VSA.InstantiateDTE()
        vProj = VSA.OpenProj(vDTE,"HelloWorld.vcxproj")
        #---
        VSA.AddFileToProj(vProj,"HelloWorld2.cpp","obse")
        VSA.AddFileToProj(vProj,"HelloWorld3.cpp","obse")
        #---Close
        vProj.Save()
        VSA.QuitDTE(vDTE)

    # def test_TriggerMultistring(self):
    #     pass
