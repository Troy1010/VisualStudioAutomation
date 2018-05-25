import unittest
from nose.tools import *
import os
import shutil
import sys
import xml.etree.ElementTree

import TM_CommonPy as TMC
import TM_CommonPy.Narrator as TMC_NAR
import Macro_VisualStudio as MVS
import Macro_VisualStudio.Narrator
import subprocess, win32com

class Test_TM_CommonPy(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('Macro_VisualStudio','tests'))

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        TMC.Copy('Examples_Backup','Examples')
        os.chdir('Examples')

    def tearDown(self):
        os.chdir('..')
        #shutil.rmtree('Examples')

    #------Tests

#    def test_Proj_AddFile(self):
#        MVS.Proj_AddFile("HelloWorld.vcxproj","HelloWorld2.cpp")

    def test_2(self):
        vDTE = win32com.client.Dispatch("VisualStudio.DTE.15.0")
        vProject = vDTE.Solution.AddFromFile(os.path.abspath('HelloWorld.vcxproj'))
        print(MVS.Narrator.NarrateProject(vProject))
        vProjectItems = vProject.Projectitems
        #print(MVS.Narrator.NarrateProject(vProject))
        #print("Type:"+str(type(vProjectItems)))
        #print("zz:"+str(vProjectItems))
        #print("vProject.Projectitems.Count:"+str(vProject.Projectitems.Count))
        self.assertTrue(False)

#    def test_1(self):
#        #---Run HookMultiThreadMessageHandler
#        #sScriptFile = os.path.join(os.getcwd(),'..','..','res','HookMultiThreadMessageHandler.ps1')
#        #subprocess.Popen(["powershell.exe","-executionpolicy ","bypass","-file",sScriptFile])#, shell=True)
#        #---Do something to get call rejected
#        vDTE = win32com.client.Dispatch("VisualStudio.DTE.15.0")
#        vProject = vDTE.Solution.AddFromFile(os.path.abspath('HelloWorld.vcxproj'))
#        sReturning = "Project.\n"
#        sReturning += "FileName:"+vProject.FileName
#        sReturning += "CodeModel.\n"
#        sReturning += "CodeElements..\n"
#        vCodeElements = vProject.CodeModel.CodeElements
#        sReturning += "vCodeModel.CodeElements.Count:"+str(vCodeElements.Count)
#        print (sReturning)
#        #---Add Filter
#        vProject.Object.project.AddFilter("wewt")
#        vProject.Save()
#        #vProjectObject = vProject.Object
#        #vVCProject = vProjectObject.project





        #print(MVS.Narrator.NarrateProject(MVS.InstantiateDTE().Solution.AddFromFile(os.path.abspath('HelloWorld.vcxproj'))))
#        self.assertTrue(False)

#    def test_NarrateProject(self):
#        print(MVS.Narrator.NarrateProject(MVS.InstantiateDTE().Solution.AddFromFile(os.path.abspath('HelloWorld.vcxproj'))))
#        self.assertTrue(False)
