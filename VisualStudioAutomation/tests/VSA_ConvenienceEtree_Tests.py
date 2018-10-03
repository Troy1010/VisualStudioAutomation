##region Settings
bSkip=True
bPostDelete=True
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

@unittest.skipIf(bSkip,"Skip Setting")
class Test_VSA_XML(TestCase):
    sTestWorkspace = "TestWorkspace_XML/"

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

    def test_IntegrateProps_AndUndo(self):
        with TM.CopyContext("res/Examples_XML_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            VS.IntegrateProps('HelloWorld.vcxproj','conanbuildinfo.props')
            self.assertTrue(TM.IsTextInFile('conanbuildinfo.props','HelloWorld.vcxproj'))
            VS.IntegrateProps_Undo('HelloWorld.vcxproj','conanbuildinfo.props')
            self.assertFalse(TM.IsTextInFile('conanbuildinfo.props','HelloWorld.vcxproj'))

    def test_IntegrateProps_AndUndo_OnFileWithBOM(self):
        with TM.CopyContext("res/Examples_XML_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            VS.IntegrateProps('obse_plugin_example_RAW.vcxproj','conanbuildinfo.props')
            self.assertTrue(TM.IsTextInFile('conanbuildinfo.props','obse_plugin_example_RAW.vcxproj'))
            VS.IntegrateProps_Undo('obse_plugin_example_RAW.vcxproj','conanbuildinfo.props')
            self.assertFalse(TM.IsTextInFile('conanbuildinfo.props','obse_plugin_example_RAW.vcxproj'))

    def test__ElementFromGeneratedBuildInfoFile_ByExample(self):
        with TM.CopyContext("res/Examples_XML_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            vElem = _ElementFromGeneratedBuildInfoFile('HelloWorld.vcxproj','conanbuildinfo.props')
            #------Assert
            self.assertTrue(len(vElem.attrib.values()) == 2)
            self.assertTrue(vElem.tag == 'Import')
            self.assertTrue(vElem.attrib['Project'] == 'conanbuildinfo.props')
            self.assertTrue(vElem.attrib['Condition'] == 'Exists(\'conanbuildinfo.props\')')

    def test_IntegrateProps_UseTwiceAndNoDupEntry(self):
        with TM.CopyContext("res/Examples_XML_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
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

    def test_IntegrateProps_Undo_OveruseProtocol_Try(self):
        with TM.CopyContext("res/Examples_XML_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
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

    def test_SetTMDefaultVSSettings(self):
        with TM.CopyContext("res/Examples_XML_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            self.assertFalse(TM.IsTextInFile("OutDir",'HelloWorld.vcxproj'))
            VS.SetTMDefaultVSSettings.Do('HelloWorld.vcxproj')
            self.assertTrue(TM.IsTextInFile("OutDir",'HelloWorld.vcxproj'))
            VS.SetTMDefaultVSSettings.Undo('HelloWorld.vcxproj')
            self.assertFalse(TM.IsTextInFile("OutDir",'HelloWorld.vcxproj'))
