from unittest import TestCase
import os
import subprocess
import shutil
import xml
from pprint import pprint

import TM_CommonPy as TM
import BuildInfoIntegration as BII

class Test_VSA_XML(TestCase):
    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('VisualStudioAutomation','XML','tests','res'))

    @classmethod
    def tearDownClass(self):
        os.chdir(os.path.join('..','..','..','..'))

    #----Tests

    def test_HookBuildInfo_AndUndo_Try(self):
        with TM.CopyContext("Examples_Backup","test_HookBuildInfo_AndUndo_Try",bPostDelete=False):
            BII.HookBuildInfo(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
            BII.HookBuildInfo_Undo(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')

    def test_HookBuildInfo_AndUndo_TryOnXMLWithBOM(self):
        with TM.CopyContext("Examples_Backup","test_HookBuildInfo_AndUndo_Try",bPostDelete=False):
            BII.HookBuildInfo('obse_plugin_example_RAW.vcxproj','conanbuildinfo.props')
            BII.HookBuildInfo_Undo('obse_plugin_example_RAW.vcxproj','conanbuildinfo.props')

    def test__ElementFromGeneratedBuildInfoFile_ByExample(self):
        with TM.CopyContext("Examples_Backup","test_HookBuildInfo_AndUndo_Try",bPostDelete=False):
            vElem = BII._ElementFromGeneratedBuildInfoFile(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
            #------Assert
            self.assertTrue(len(vElem.attrib.values()) == 2)
            self.assertTrue(vElem.tag == 'Import')
            self.assertTrue(vElem.attrib['Project'] == os.path.join('..','conanbuildinfo.props'))
            self.assertTrue(vElem.attrib['Condition'] == os.path.join('Exists(\'..','conanbuildinfo.props\')'))

    def test_HookBuildInfo_UseTwiceAndNoDupEntry(self):
        with TM.CopyContext("Examples_Backup","test_HookBuildInfo_AndUndo_Try",bPostDelete=False):
            BII.HookBuildInfo(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
            BII.HookBuildInfo(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
            BII.HookBuildInfo(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
            #---Make sure there is only 1 inserted element.
            #-Open sConsumerProjFile
            vTree = xml.etree.ElementTree.parse(os.path.join('HelloWorld','HelloWorld.vcxproj'))
            #-
            iCount = 0
            vElemTemplateToSearchFor = BII._ElementFromGeneratedBuildInfoFile(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
            for vItem in vTree.iter():
                if 'ImportGroup' in vItem.tag and 'Label' in vItem.attrib and vItem.attrib['Label'] == "ExtensionSettings":
                    bFound = True
                    for vItem2 in vItem:
                        if vElemTemplateToSearchFor.tag in vItem2.tag and vItem2.attrib == vElemTemplateToSearchFor.attrib:
                            iCount += 1
                    break
            #------Assert
            self.assertTrue(bFound)
            self.assertTrue(not iCount < 1)
            self.assertTrue(not iCount > 1)
            #self.assertTrue(False)

    def test_HookBuildInfo_Undo_OveruseProtocol_Try(self):
        with TM.CopyContext("Examples_Backup","test_HookBuildInfo_AndUndo_Try",bPostDelete=False):
            BII.HookBuildInfo(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
            BII.HookBuildInfo_Undo(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
            BII.HookBuildInfo_Undo(os.path.join('HelloWorld','HelloWorld.vcxproj'),'conanbuildinfo.props')
