# Copyright (c) 2015, Forschungszentrum Jülich GmbH
# All rights reserved.
# Contributors: Jonas Bühler, Daniel Pflugfelder, Siegfried Jahnke
# Address: Institute of Bio- and Geosciences, Plant Sciences (IBG-2), Forschungszentrum Jülich GmbH, 52428 Jülich, Germany
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors
#     may be used to endorse or promote products derived from this software without
#     specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.


#//----------------------------------------------------------------------------------
#//! Macro module phenoVein
#/*!
#// \file    phenoVein.py
#// \author  Jonas Buehler
#// \date    2014-03-10
#//
#// This is the phenoVein application module. 
#// COPYRIGHT: Forschungszentrum Jülich GmbH, Germany
#*/
#//----------------------------------------------------------------------------------


import mevis as ml
import os
from PythonQt import QtGui

def showPhenoVeinAboutDialog():
  ## not implemented yet
  return



def initPhenoVein():
  # load default settings
  ctx.field("SettingsManagerGeneralParameters.load").touch()
  
  # load application icon
  icon = QtGui.QIcon(ctx.expandFilename("$(LOCAL)/Logo/icon.png"))
  ctx.window().widget().setWindowIcon(icon)
  
  ##set transparencies
  #setTransparancyValuesActiveSkel()
  #setTransparancyValuesDeleteSkel()
  ctx.field("phenoVein_Skeletonization.loadThreshold").touch()
  ctx.field("phenoVein_WriteResultsToFiles.currentVersionNumber").setValue( ctx.field("currentVersionNumber").value )
  return


def loadExistingSettings():
  ctx.field("SettingsManagerCurrentSession.load").touch()
  # note  that SettingsManager also sets input filename which results in deleting all previous manual corrections
  # so, the filename has to be set before cso filenames are set in ManualCorrection module
  ml.MLAB.processEvents()
  
  localPVIDir = ctx.field("settingsFilename").value
  localPVIDir = os.path.split(localPVIDir)[0] + "/"

  # image file
  imageFilename = ctx.field("imageFilename").value
  basenameImageFile = os.path.split(imageFilename)[1]
  reloadFlag = 0
  
  if not os.path.exists(imageFilename):
    reloadFlag = 1
    print("Image file could not be found: " + imageFilename)
    newImageFilename = ml.MLABFileDialog.getOpenFileName(localPVIDir+"/"+basenameImageFile, "*.*", "Select original image file...")
    if os.path.exists(newImageFilename):
      ctx.field("imageFilename").setValue(newImageFilename)
    else:
      print("Error: file " + newImageFilename + " could not be found! Stop!")
      return 
    
  # manual correction files
  addCSOFilename       = ctx.field("phenoVein_ManualCorrection.addCSOFilename").value
  removeCSOFilename    = ctx.field("phenoVein_ManualCorrection.removeCSOFilename").value
  removeMarkerFilename = ctx.field("phenoVein_ManualCorrection.removeMarkerFilename").value
  
  reloadFlag = reloadFlag or (not os.path.exists(addCSOFilename)) or (os.path.exists(removeCSOFilename)) or (os.path.exists(removeMarkerFilename))
  
  if reloadFlag:
    # complete pvi filename - ".pvi"
    basePathAndFilename = ctx.field("settingsFilename").value[0:-4]
    ctx.field("phenoVein_ManualCorrection.outFilename").setValue(basePathAndFilename)
    # make phenoVein_ManualCorrection load CSO FILES
    ctx.field("phenoVein_ManualCorrection.loadManualCorrections").touch()
  
  if not os.path.exists(addCSOFilename):
    basenameAddCSOFile = os.path.split(addCSOFilename)[1]
    newAddCSOFile = localPVIDir + basenameAddCSOFile
    if os.path.exists(newAddCSOFile):
      ctx.field("phenoVein_ManualCorrection.addCSOFilename").setValue(newAddCSOFile)
    else:
      print("Error: file " + basenameAddCSOFile + " could not be found in local dir! Stop!")
      return 
  
  # removeCSO file
  if not os.path.exists(removeCSOFilename):
    basenameRemoveCSOFile = os.path.split(removeCSOFilename)[1]
    newRemoveCSOFile = localPVIDir + basenameRemoveCSOFile
    if os.path.exists(newRemoveCSOFile):
      ctx.field("phenoVein_ManualCorrection.removeCSOFilename").setValue(newRemoveCSOFile)
    else:
      print("Error: file " + basenameRemoveCSOFile + " could not be found in local dir! Stop!")
      return 
    
  return 


def skel_updateAndSaveThreshold():
  ctx.field("phenoVein_Skeletonization.skeletonUpdate").touch()
  ctx.field("phenoVein_Skeletonization.saveThreshold").touch()
  return


def QuickSaveInManualCorrection():
  ctx.field("phenoVein_ReSkeletonization.updateInputs").touch()
  ctx.field("phenoVein_WriteResultsToFiles.updateInputs").touch()
  WTF_Autofilename_Save()
  return

def QuickSaveInSkeletonization():
  ctx.field("phenoVein_ManualCorrection.updateInputs").touch()
  ctx.field("phenoVein_ReSkeletonization.updateInputs").touch()
  ctx.field("phenoVein_WriteResultsToFiles.updateInputs").touch()
  WTF_Autofilename_Save()
  return 

def WTF_Save():
  outfilename = ctx.field("WTF_outFilename").value
  # check for directory, if it doesn't exist: create it
  outfileDirectory = os.path.abspath(outfilename+"\\..")

  # check for existing pvi file, if exists, ask for overwriting
  pviOutfilename = outfilename + ".pvi"
  if os.path.exists(pviOutfilename):
    overwriteFlag = QtGui.QMessageBox.question(0, "Overwrite?", "The file <" + pviOutfilename + "> already exists! Overwrite? (Also respective result images and csv files will be overwrittten)", QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
  else:
    overwriteFlag = 0

  if not overwriteFlag == QtGui.QMessageBox.Cancel:
    if not os.path.exists(outfileDirectory):
      os.mkdir(outfileDirectory)
  
    # write manual corrections to file
    ctx.field("phenoVein_ManualCorrection.saveManualCorrections").touch()
  
    # write .csv files & write result images
    ctx.field("phenoVein_WriteResultsToFiles.writeResultsToFile").touch()
    
    # save network parameters
    ctx.field("SettingsManagerCurrentSession.filename").setStringValue(outfilename + ".pvi")
    ctx.field("SettingsManagerCurrentSession.save").touch()
  return


def WTF_Autofilename_Save():
  ctx.field("WTF_getAutoFilename").touch()
  WTF_Save()
  return

def WTF_VeinAnalysis_Autofilename_Save():
  ctx.field("phenoVein_VeinWidth.updateInputs").touch()
  ctx.field("phenoVein_VeinWidth.calcAllVeins").touch()
  WTF_Autofilename_Save()


def deleteAllManualCorrections(field):
  print("Deleting all manual corrections for new image...")
  ctx.field("phenoVein_ManualCorrection.deleteRemoveAreas").touch()
  ctx.field("phenoVein_ManualCorrection.deleteRemoveMarker").touch()
  ctx.field("phenoVein_ManualCorrection.removeAllAddedVeins").touch()
  return  



########################################################################################
# Set Transparencies for all viewers
########################################################################################
def setTransparancyValuesActiveSkel():
  alphaFactor = ctx.field("transparencyActiveSkel").value
  ctx.field("phenoVein_Skeletonization.transparencyActiveSkel").setValue(alphaFactor)
  ctx.field("phenoVein_ManualCorrection.transparencyActiveSkel").setValue(alphaFactor)
  ctx.field("phenoVein_ReSkeletonization.transparencyActiveSkel").setValue(alphaFactor)
  ctx.field("phenoVein_VeinWidth.transparencyActiveSkel").setValue(alphaFactor)
  return

def setTransparancyValuesDeleteSkel():
  alphaFactor = ctx.field("transparencyDeleteSkel").value
  ctx.field("phenoVein_Skeletonization.transparencyDeleteSkel").setValue(alphaFactor)
  ctx.field("phenoVein_ManualCorrection.transparencyDeleteSkel").setValue(alphaFactor)
  ctx.field("phenoVein_ReSkeletonization.transparencyDeleteSkel").setValue(alphaFactor)
  return
########################################################################################
########################################################################################



########################################################################################
# TAB UPDATE SECTION
########################################################################################

def updateTab_LeafBackgroundSegmentation():
  inputUpToDate = ctx.field("phenoVein_LeafBackgroundSegmentation.inputUpToDate").value
  if (not inputUpToDate):
    ctx.field("phenoVein_LeafBackgroundSegmentation.updateInput").touch()
    ctx.field("phenoVein_LeafBackgroundSegmentation.resetLUT").touch()
  return

def updateTab_FrangiFiltering():
  inputUpToDate = ctx.field("phenoVein_FrangiFiltering.inputUpToDate").value
  if (not inputUpToDate):
    ctx.field("phenoVein_FrangiFiltering.updateInputs").touch()
    ctx.field("phenoVein_FrangiFiltering.resetLUTs").touch()
  return

def updateTab_Skeletonization():
  inputUpToDate = ctx.field("phenoVein_Skeletonization.inputUpToDate").value
  if (not inputUpToDate):
    ctx.field("phenoVein_Skeletonization.updateInputs").touch()
    ctx.field("phenoVein_Skeletonization.resetLUTs").touch()
  return

def updateTab_ManualCorrection():
  ctx.field("phenoVein_ManualCorrection.updateInputs").touch()
  ctx.field("phenoVein_ManualCorrection.resetLUT").touch()
  return

def updateTab_ReSkeletonization():
  ctx.field("phenoVein_ReSkeletonization.updateInputs").touch()
  ctx.field("phenoVein_ReSkeletonization.resetLUT").touch()
  return

def updateTab_VeinWidth():
  ctx.field("phenoVein_VeinWidth.updateInputs").touch()
  ctx.field("phenoVein_VeinWidth.resetLUT").touch()
  return

def updateTab_WriteResultsToFile():
  ctx.field("phenoVein_WriteResultsToFiles.updateInputs").touch()
  ml.MLAB.processEvents()
  ctx.field("phenoVein_WriteResultsToFiles.updateResultImages").touch()
  return

########################################################################################
########################################################################################



########################################################################################
# HELP section - for pop up help dialogs
########################################################################################

def showHelpWindow_Tab01():
  message = ""
  message = message + "<b><big>In this tab the input image is preprocessed</big></b>"
  message = message + "<br><br>It is important to understand that the following segmentation process needs a <b>gray value image</b> where the veins appear brighter than the surrounding areoles! For this reason color images need to be converted to gray value images. phenoVein supports image conversion to <a href=\"http://en.wikipedia.org/wiki/RGB_color_model\">RGB</a>, <a href=\"http://en.wikipedia.org/wiki/YUV\">YUV</a> and <a href=\"http://en.wikipedia.org/wiki/HSL_and_HSV\">HSV</a> (Wikipedia). It depends on the image characteristics which color channel gives an optimal vein/background contrast. Without any further information, just try different channels and use the one that works best for you."
  message = message + "<br><br>For length and area measurements, the <b>image pixel size</b> needs to be set as precise as possible.<br>1: If the pixel size is known it can be set directly in units of mm/pixel.<br>2: If the pixel size is set correctly in the image meta-data (usually defined as dpi). Click \"Get pixel size from image\" to adopt this value into phenoVein.<br>3: The pixel size can be measured from objects in the image which have a known size. Use Strg + Left Mouse to draw the measuring vector. Set the vector length (=object size) and click \"Get pixel size from vector\"."
  message = message + "<br><br>For convenience, most numeric parameters in the menus can be adjusted by scrolling the mouse wheel while the cursor is over the respective field."
  message = message + "<br><br>The viewer options, like brightness, contrast and zooming are only for visualization purposes and have no effect on the processed image data."
  QtGui.QMessageBox.question(0, "Help", message, QtGui.QMessageBox.Ok)
  return

def showHelpWindow_Tab03():
  message = ""
  message = message + "<b><big>This tab serves to enhance the veins</big></b>"
  message = message + "<br><br>Lower and Upper Sigma define the minimum and maximum vein widths in units of pixels that should be enhanced. The number of steps tell the filter algorithm with how many scales the filtering should be done. For more information see the MeVisLab help on the module \"Vesselness\". For direct leaf photographs, the following default values for sigma gave reasonable results<br>low: 2-6<br>high: 4-12<br>Minimum number of steps: 3<br>A high number of steps does not necessarily improve image quality but definitely results in higher computation times. It is difficult to suggest optimal values for all scenarios, so empirical testing is recommended."
  message = message + "<br><br>The closing kernel size controls the morphologic operation that closes undesired disruptions at branching points. Also here, testing for the optimal value is recommended. The default value is 5."
  message = message + "<br><br>The parameter Boundary Erosion is the distance from the boundary in which pixels are ignored for filtering."
  QtGui.QMessageBox.question(0, "Help", message, QtGui.QMessageBox.Ok)
  return

########################################################################################
########################################################################################




