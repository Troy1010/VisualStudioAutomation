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

import win32com.client

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

    #Working
#    def test_Proj_AddFile(self):
#        os.chdir('..')
#        TMC.Copy('Examples_Backup','Examples_Proj_AddFile',bPreDelete=True)
#        os.chdir('Examples_Proj_AddFile')
#        MVS.Proj_AddFile("HelloWorld.vcxproj","HelloWorld2.cpp")

    #Working
#    def test_NarrateProj(self):
#        vDTE = MVS.InstantiateDTE()
#        vProj = vDTE.Solution.AddFromFile(os.path.abspath("HelloWorld.vcxproj")).object
#        print(TMC.Narrator.Narrate(vProj,bIncludeProtected=True,bIncludePrivate=True))
#        MVS.QuitDTE(vDTE)
#        #self.assertTrue(False)

    #Working
#    def test_Proj_Filter(self):
#        #---Open
#        vDTE = MVS.InstantiateDTE()
#        #---
#        os.chdir('..')
#        TMC.Copy('Examples_Backup','Examples_Proj_Filter',bPreDelete=True)
#        os.chdir('Examples_Proj_Filter')
#        #---
#        vProject = vDTE.Solution.AddFromFile(os.path.abspath("HelloWorld.vcxproj"))
#        MVS.Proj_Filter("FilterName1",vProject)
#        #---Close
#        MVS.QuitDTE(vDTE)
#        #self.assertTrue(False)

    #Working
#    def test_NarrateProj(self):
#        vDTE = MVS.InstantiateDTE()
#        vProj = vDTE.Solution.AddFromFile(os.path.abspath("HelloWorld.vcxproj"))
#        vProj2 = vProj.Object.project
#        print(TMC.Narrator.Narrate(vProj2,bIncludeProtected=True,bIncludePrivate=True))
#        MVS.QuitDTE(vDTE)
#        self.assertTrue(False)

    #Working
#    def test_ProjItem_Filter(self):
#        #---Open
#        vDTE = MVS.InstantiateDTE()
#        #---
#        os.chdir('..')
#        TMC.Copy('Examples_Backup','Examples_ProjItem_Filter',bPreDelete=True)
#        os.chdir('Examples_ProjItem_Filter')
#        #--- Get vProj
#        vProj = vDTE.Solution.AddFromFile(os.path.abspath("HelloWorld.vcxproj"))
#        #--- Add File
#        vProjectItem = vProj.ProjectItems.AddFromFile(os.path.abspath("HelloWorld2.cpp"))
#        #--- Add Filter
#        vFilter = vProj.Object.AddFilter("Filter1")
#        #--- Add File to Filter
#        vFilter.AddFile(os.path.abspath("HelloWorld3.cpp"))
#        #--- Save
#        vProj.Save()
#        #--- Close
#        MVS.QuitDTE(vDTE)

    #Working
    def test_ProjItem_Filter(self):
        #---Open
        vDTE = MVS.InstantiateDTE()
        #---
        os.chdir('..')
        TMC.Copy('Examples_Backup','Examples_ProjItem_Filter',bPreDelete=True)
        os.chdir('Examples_ProjItem_Filter')
        #---Get vProj
        vProj = vDTE.Solution.AddFromFile(os.path.abspath("HelloWorld.vcxproj"))
        vProjItem = vProj.ProjectItems.AddFromFile("HelloWorld3.cpp")
        #    sFilterName    vProjItem
        MVS.AddFilterToProjItem("Filter7",vProjItem)
        #---Save
        vProj.Save()
        #---Close
        MVS.QuitDTE(vDTE)








#--- Add File
#        vProjectItem = vProj.ProjectItems.AddFromFile(os.path.abspath("HelloWorld2.cpp"))
#        vProjectItems = vProj.ProjectItems

#        vProj = vDTE.Solution.AddFromFile(os.path.abspath("HelloWorld.vcxproj"))
#        #--- Add File
#        sFileToAdd = "HelloWorld2.cpp"
#        sFileToAdd = os.path.abspath(sFileToAdd)
#        if not os.path.isfile(sFileToAdd):
#            raise Exception("sFileToAdd does not exist:"+sFileToAdd)
#        vProjectItem = vProj.ProjectItems.AddFromFile(sFileToAdd)
#        vFile = vProj.ProjectItems.AddFromFile(os.path.abspath("HelloWorld2.cpp"))
#        vProjectItem = vProj.ProjectItems.AddFromFile(os.path.abspath("HelloWorld2.cpp"))
#        vFile = vProj.ProjectItems.AddFromFile("HelloWorld2.cpp")
        #--- Add Filter
#        vFilter = vProj.Object.project.AddFilter("FilterName1")
        #--- Add File to Filter
#        vFilter.AddFile(os.path.abspath("HelloWorld2.cpp"))
        #--- Save
#        vProj.Object.project.Save()
        #---
#        for vFilter in vProj.Filters:
#            vFilter.AddFile(vFile)
#            break
#        vProjItems = vProj.ProjectItems
#        for vProjItem in vProjItems:
#            MVS.ProjItem_Filter(vProjItem.Name,vProjItem)
#            vProj = vProjectItem.ContainingProject
#            for vFilter in vProj.Filters:
#                vFilter.AddFile(sFile)
#            break
        #---Close
#        MVS.QuitDTE(vDTE)
#        self.assertTrue(False)

#    def test_Proj_LinkToProps(self):
#        os.chdir('..')
#        TMC.Copy('Examples_Backup','Examples_Proj_LinkToProps',bPreDelete=True)
#        os.chdir('Examples_Proj_LinkToProps')
#        MVS.Proj_LinkToProps("HelloWorld.vcxproj","conanbuildinfo.props")

#    def test_NarrateProj2(self):
#        vDTE = MVS.InstantiateDTE()
#        vProj = vDTE.Solution.AddFromFile(os.path.abspath("HelloWorld.vcxproj"))
#        print(TMC.Narrator.Narrate(vProj,bIncludeProtected=False))
#        MVS.QuitDTE(vDTE)
#        #self.assertTrue(False)

#    def test_NarrateProj2(self):
#        print(TMC.Narrator.Narrate(MVS.GetProjObj("HelloWorld.vcxproj"),bIncludeProtected=False))
#        self.assertTrue(False)

#    def test_Proj_AddFile(self):
#        MVS.Proj_AddFile("HelloWorld.vcxproj","HelloWorld2.cpp")

#    def test_2(self):
#        vDTE = win32com.client.Dispatch("VisualStudio.DTE.15.0")
#        vProject = vDTE.Solution.AddFromFile(os.path.abspath('HelloWorld.vcxproj'))
#        print(MVS.Narrator.NarrateProject(vProject))
#        vProjectItems = vProject.Projectitems
#        #print(MVS.Narrator.NarrateProject(vProject))
#        #print("Type:"+str(type(vProjectItems)))
#        #print("zz:"+str(vProjectItems))
#        #print("vProject.Projectitems.Count:"+str(vProject.Projectitems.Count))
#        self.assertTrue(False)

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
