import ctypes
from pprint import pprint
import TM_CommonPy as TM
import sys, os
import xml.etree.ElementTree
import win32com.client
import time
import VisualStudioAutomation as VS
import win32process
import psutil
import time
import logging
import retrying
from retrying import retry



@retry(retry_on_exception=VS.IsRetryableException,stop_max_delay=10000)
def examine_AddAndRemoveProjRef():
    sTestWorkspace = "TestWorkspace/"
    with TM.CopyContext("res/Examples_Backup",sTestWorkspace+TM.FnName(),bPostDelete=False):
        with VS.DTEWrapper() as vDTEWrapper, vDTEWrapper.OpenProj("HelloWorld.vcxproj") as vProjWrapper, vDTEWrapper.OpenProj("HelloWorld2.vcxproj") as vProjToReferenceWrapper:
            TM.Narrator.Print(vProjWrapper.vProj.Object.References)
            vProjWrapper.AddProjRef(vProjToReferenceWrapper.vProj)
            vProjWrapper.Save()
            print("`")
            TM.Narrator.Print(vProjWrapper.vProj.Object.References)
            print("`")
            cToRemove = []
            for vItem in vProjWrapper.vProj.Object.References:
                print(vItem.Name)
                if vItem.Name == vProjToReferenceWrapper.vProj.Name:
                    print("Match")
                    cToRemove.append(vItem)
                    #vItem.Remove()
                    #vRefToRemove = vItem
            #vRefToRemove.Remove()
            for vItem in cToRemove:
                vItem.Remove()
            print("````")
            TM.Narrator.Print(vProjWrapper.vProj.Object.References)
            #vProjWrapper.RemoveProjRef()

            #vProjWrapper.RemoveProjRef(vProjToReferenceWrapper.vProj)
            #vProjWrapper.Save()

examine_AddAndRemoveProjRef()
