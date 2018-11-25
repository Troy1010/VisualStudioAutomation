##region Settings
bPostDelete=False
##endregion

from unittest import TestCase
import os
import subprocess
import shutil
import xml
from pprint import pprint
import unittest
import TM_CommonPy as TM
import VisualStudioAutomation as VS
from VisualStudioAutomation.ConvenienceEtree import _ElementFromGeneratedBuildInfoFile
from nose.plugins.attrib import attr
from VisualStudioAutomation._tests._Logger import VSLog_LogTests

vCounter = TM.Counter()

class Test_VSA_XML(TestCase):
    sTestWorkspace = "_TestWorkspace_XML/"

    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('VisualStudioAutomation','_tests'))
        TM.Delete(self.sTestWorkspace)

    @classmethod
    def tearDownClass(self):
        global bPostDelete
        if bPostDelete:
            TM.Delete(self.sTestWorkspace)
        os.chdir(os.path.join('..','..'))

    #------Tests

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_RemoveProjectFromSlnFile(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            self.assertTrue(TM.IsTextInFile('HelloWorld.vcxproj','HelloWorld.sln'))
            VS.RemoveProjectFromSlnFile('HelloWorld.sln','HelloWorld.vcxproj')
            self.assertFalse(TM.IsTextInFile('HelloWorld.vcxproj','HelloWorld.sln'))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_GetProjectGuid(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            vVar = VS.GetProjectGUID('HelloWorld.vcxproj')
            VSLog_LogTests.info("vVar:"+str(vVar))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_IntegrateProps_AndUndo(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            VS.IntegrateProps('HelloWorld.vcxproj','conanbuildinfo.props')
            self.assertTrue(TM.IsTextInFile('conanbuildinfo.props','HelloWorld.vcxproj'))
            VS.IntegrateProps_Undo('HelloWorld.vcxproj','conanbuildinfo.props')
            self.assertFalse(TM.IsTextInFile('conanbuildinfo.props','HelloWorld.vcxproj'))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_IntegrateProps_AndUndo_OnFileWithBOM(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            VS.IntegrateProps('obse_plugin_example_RAW.vcxproj','conanbuildinfo.props')
            self.assertTrue(TM.IsTextInFile('conanbuildinfo.props','obse_plugin_example_RAW.vcxproj'))
            VS.IntegrateProps_Undo('obse_plugin_example_RAW.vcxproj','conanbuildinfo.props')
            self.assertFalse(TM.IsTextInFile('conanbuildinfo.props','obse_plugin_example_RAW.vcxproj'))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test__ElementFromGeneratedBuildInfoFile_ByExample(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            vElem = _ElementFromGeneratedBuildInfoFile('HelloWorld.vcxproj','conanbuildinfo.props')
            #------Assert
            self.assertTrue(len(vElem.attrib.values()) == 2)
            self.assertTrue(vElem.tag == 'Import')
            self.assertTrue(vElem.attrib['Project'] == 'conanbuildinfo.props')
            self.assertTrue(vElem.attrib['Condition'] == 'Exists(\'conanbuildinfo.props\')')

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_IntegrateProps_UseTwiceAndNoDupEntry(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            VS.IntegrateProps('HelloWorld.vcxproj','conanbuildinfo.props')
            VS.IntegrateProps('HelloWorld.vcxproj','conanbuildinfo.props')
            VS.IntegrateProps('HelloWorld.vcxproj','conanbuildinfo.props')
            #---Make sure there is 1 inserted element.
            with TM.ElementTreeContext('HelloWorld.vcxproj') as vTree:
                iCount = 0
                vElemTemplateToSearchFor = _ElementFromGeneratedBuildInfoFile('HelloWorld.vcxproj','conanbuildinfo.props')
                for vItem in vTree.iter():
                    if 'ImportGroup' in vItem.tag and 'Label' in vItem.attrib and vItem.attrib['Label'] == "ExtensionSettings":
                        bFoundParent = True
                        for vItem2 in vItem:
                            if vElemTemplateToSearchFor.tag in vItem2.tag and vItem2.attrib == vElemTemplateToSearchFor.attrib:
                                iCount += 1
                        break
            self.assertTrue(bFoundParent)
            self.assertEqual(iCount,1)

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_IntegrateProps_Undo_OveruseProtocol_Try(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            VS.IntegrateProps('HelloWorld.vcxproj','conanbuildinfo.props')
            VS.IntegrateProps_Undo('HelloWorld.vcxproj','conanbuildinfo.props')
            VS.IntegrateProps_Undo('HelloWorld.vcxproj','conanbuildinfo.props')
            #---Make sure there are 0 inserted elements.
            with TM.ElementTreeContext('HelloWorld.vcxproj') as vTree:
                iCount = 0
                vElemTemplateToSearchFor = _ElementFromGeneratedBuildInfoFile('HelloWorld.vcxproj','conanbuildinfo.props')
                for vItem in vTree.iter():
                    if 'ImportGroup' in vItem.tag and 'Label' in vItem.attrib and vItem.attrib['Label'] == "ExtensionSettings":
                        bFoundParent = True
                        for vItem2 in vItem:
                            if vElemTemplateToSearchFor.tag in vItem2.tag and vItem2.attrib == vElemTemplateToSearchFor.attrib:
                                iCount += 1
                        break
            self.assertTrue(bFoundParent)
            self.assertEqual(iCount,0)

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_SetTMDefaultVSSettings(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            self.assertFalse(TM.IsTextInFile("OutDir",'HelloWorld.vcxproj'))
            VS.SetTMDefaultVSSettings.Do('HelloWorld.vcxproj')
            self.assertTrue(TM.IsTextInFile("OutDir",'HelloWorld.vcxproj'))
            VS.SetTMDefaultVSSettings.Undo('HelloWorld.vcxproj')
            self.assertFalse(TM.IsTextInFile("OutDir",'HelloWorld.vcxproj'))

    @attr(**{'count':vCounter(),__name__.rsplit(".",1)[-1]:True})
    def test_SetIncludeDir(self):
        with TM.WorkspaceContext(self.sTestWorkspace+TM.FnName(),sSource="res/Examples_XML_Backup",bPostDelete=False,bCDInto=True):
            VS.SetIncludeDir('HelloWorld.vcxproj',"C:\ADir")
            self.assertTrue(TM.IsTextInFile("C:\ADir",'HelloWorld.vcxproj'))
