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


import mevis as ml
import os
import time
from PythonQt import QtGui
import numpy as np
#import phenoVein_getCurrentVersion


#####################################
## CURRENT VERSION
#####################################
def phenoVein_getCurrentVersion():
  ver = ctx.field("currentVersionNumber").value
  return ver
#####################################
#####################################





def updateInputs():
  ctx.field("MinMaxScan0.update").touch()
  ctx.field("MinMaxScan1.update").touch()
  ctx.field("MinMaxScan2.update").touch()
  return

def updateResultImages():
  #ctx.field("SoLUTEditor_overlay.applyNewRange").touch()
  #ml.MLAB.processEvents()
  #ctx.field("SoLUTEditor_overlay.resetToRamp").touch()
  #ctx.field("SegmentedAreoles.update").touch()
  #ml.MLAB.processEvents()
  ctx.field("SkeletonTotalLength.update").touch()
  ctx.field("SkeletonEndPoints.update").touch()
  ctx.field("SkeletonBranchingPoints.update").touch()
  ctx.field("numberOfSkeletonPieces.update").touch()
  ctx.field("TotalLeafArea.update").touch()
  ctx.field("OffscreenRenderer.update").touch()
  ctx.field("OffscreenRenderer1.update").touch()
  ctx.field("OffscreenRenderer2.update").touch()
  ml.MLAB.processEvents()
  return

def updateAreoleImage():
  ctx.field("OffscreenRenderer1.update").touch()
  


def writeResultsToFile():
  # ensure that all result images are up-to-date
  updateResultImages()
  ml.MLAB.processEvents()

  # create outfilename
  outfilename = ctx.field("outFilename").value

  csvOutfilename = outfilename + ".csv"
  res = writeToCSVFile(csvOutfilename)

  messageStr = ""

  if res == 0: # file did not exist previously and has been created
    saveImages = 1
    messageStr += "File <" + csvOutfilename + "> has been written successfully."
    ctx.field("pyResultStr").setStringValue(messageStr)

  elif res == QtGui.QMessageBox.Save: # file existed and was overwritten
    saveImages = 1
    messageStr += "File <" + csvOutfilename + "> has been overwritten successfully."
    ctx.field("pyResultStr").setStringValue(messageStr)

  elif res == QtGui.QMessageBox.Cancel: # file existed but user aborted write operation, nothing happened
    saveImages = 0
    messageStr += "Writing canceled! No files written!"
    ctx.field("pyResultStr").setStringValue(messageStr)
    return

  elif res == -1: # file open error
    saveImages = 0
    messageStr += "ERROR! File <" + csvOutfilename + "> could not be opened! File not written! (maybe opened in excel?)"
    ctx.field("pyResultStr").setStringValue(messageStr)
    print(messageStr)
    QtGui.QMessageBox.warning(0, "File open error", messageStr)
    return

  if saveImages == 1:
    ## save aeriole sizes
    ctx.field("SaveAreoleSizes.filename").setStringValue(outfilename + "_AreoleSizes.png")
    #ctx.field("SaveAreoleSizes.startTask").touch()
    ctx.field("SaveAreoleSizes.save").touch()
  
    ## save skeleton mask
    ctx.field("SaveSkeleton.filename").setStringValue(outfilename + "_skeleton.png")
    #ctx.field("SaveSkeleton.startTask").touch()
    ctx.field("SaveSkeleton.save").touch()
  
    ## save leaf mask
    ctx.field("SaveLeafMask.filename").setStringValue(outfilename + "_LeafMask.png")
    #ctx.field("SaveLeafMask.startTask").touch()
    ctx.field("SaveLeafMask.save").touch()
  
    ## save image+overlay
    ctx.field("SaveSkelOverlay.filename").setStringValue(outfilename + "_SkelOverlay.jpg")
    ml.MLAB.processEvents()
    #ctx.field("SaveSkelOverlay.startTask").touch()
    ctx.field("SaveSkelOverlay.save").touch()
  
    ## save original image (maybe cropped)
    ctx.field("SaveMaskedOriginal.filename").setStringValue(outfilename + "_croppedOriginal.tif")
    #ctx.field("SaveMaskedOriginal.startTask").touch()
    ctx.field("SaveMaskedOriginal.save").touch()
  
    ## save colorbar
    ctx.field("SaveAreoleSizesColorbar.filename").setStringValue(outfilename + "_AreoleSizes_Colorbar.png")
    #ctx.field("SaveAreoleSizesColorbar.startTask").touch()
    ctx.field("SaveAreoleSizesColorbar.save").touch()
  


  return




def writeToCSVFile(csvOutfilename):
  
  if os.path.exists(csvOutfilename):
    #qmb = QtGui.QMessageBox
    res = QtGui.QMessageBox.question(0, "Overwrite?", "The file <" + csvOutfilename + "> already exists! Overwrite? (Also respective result images will be overwrittten)", QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
  else:
    res = 0

  if not res == QtGui.QMessageBox.Cancel:

    try:
      d = open(csvOutfilename, 'w')
    except:
      res = -1
      return res
    
    voxelSizeX = ctx.field("PixelSizes.voxelSizeX").value
    voxelSizeY = ctx.field("PixelSizes.voxelSizeY").value
    
    # update fields
    #ctx.field("TotalLeafArea.update").touch()
    #ctx.field("SkeletonTotalLength.update").touch()
    #ctx.field("SkeletonEndPoints.update").touch()
    #ctx.field("SkeletonBranchingPoints.update").touch()
    #ctx.field("numberOfSkeletonPieces.update").touch()
    #ml.MLAB.processEvents()

    # get values
    totalLeafArea        = ctx.field("TotalLeafArea.innerVolume").value
    if totalLeafArea == 0: # to avoid division by zero below
      totalLeafArea = -1;
    totalSkeletonLength   = ctx.field("SkeletonTotalLength.totalSkeletonLength").value
    numberEndPoints        = ctx.field("SkeletonEndPoints.numberEndPoints").value
    numberBranchingPoints  = ctx.field("SkeletonBranchingPoints.numberBranchingPoints").value
    numberSkeletonPieces   = ctx.field("numberOfSkeletonPieces.numberOfClusters").value
    numberOfAerioles       = ctx.field("SegmentedAreoles.numberOfClusters").value
    aerioleSizes_pixel     = ctx.field("Histogram_objectSizes.outputHistogramCurve").object().getYSlice(0)
    factor                 = voxelSizeX * voxelSizeY
    aerioleSizes_mm2       = tuple([ factor*x for x in aerioleSizes_pixel])
    veinLengthAndWidth     = ctx.field("veinLengthAndWidth").value
    
    
    
    d.write(("Input file:; " + ctx.field("sourceFilename").value + u"\n").encode('iso-8859-15'))
    d.write(("Analysis name:;" + ctx.field("analysisName").value + "\n").encode('iso-8859-15'))
    
    d.write("VoxelSize_X:;" + str(voxelSizeX) + ";[mm];" + "VoxelSize_Y:;" + str(voxelSizeY) + ";[mm]\n")
  
    d.write("Number of leaf pixels:;" + str(ctx.field("TotalLeafArea.innerVoxels").value) + "\n")
    d.write("Total leaf area (from mask):;" + str(totalLeafArea) + ";[mm^2]\n")
    
    d.write("Total skeleton length:;" + str(totalSkeletonLength) + ";[mm]\n")
    
    d.write("Average vein density:;" + str(totalSkeletonLength/totalLeafArea) + ";[mm mm^-2]\n")
    d.write("Number of skeleton pieces:;" + str(numberSkeletonPieces) + "\n")
    d.write("Number of skeleton end points:;" + str(numberEndPoints) + "\n")
    d.write("Number of skeleton branching points:;" + str(numberBranchingPoints) + "\n")

    d.write("Number of areoles:;" + str(numberOfAerioles) + "\n")
    d.write("Areole Pixels:;")
    for asPx in aerioleSizes_pixel:
      d.write(str(asPx) + ";")
    d.write("\n")
    d.write("Aeriole [mm^2]:;")
    for as2mm in aerioleSizes_mm2:
      d.write(str(as2mm) + ";")
    d.write("\n")
    # add aeriole sizes here

    d.write(veinLengthAndWidth)

    d.write("\nThis file was created with phenoVein version " + phenoVein_getCurrentVersion())

    d.close()
  
  
    # try to append results also in single csv file in dataDir
    dataDir = os.path.split(ctx.field("sourceFilename").value)[0]
    collectedResultsFilename = dataDir + "/" + "collectedResults.csv"
    try:
      if not os.path.exists(collectedResultsFilename):
        f = open(collectedResultsFilename, 'w')
        f.write("Input filename;Analysis name;Voxel size [mm];total leaf area [mm^2];total skeleton length [mm];Mean vein density [mm mm^-2];No of single vein pieces;No skeleton end points; No skeleton branching points;No areoles;Mean areole area; Std areole area;timepoint of image analysis;phenoVein version;\n")
        f.close
        
      meanAreoleArea   = np.mean(aerioleSizes_mm2)
      stdAreoleArea    = np.std(aerioleSizes_mm2)
      currentTimepoint = time.ctime()

      
      
      f = open(collectedResultsFilename, 'a')
      f.write(ctx.field("sourceFilename").value)
      f.write(";")
      f.write(ctx.field("analysisName").value)
      f.write(";")
      f.write(str(voxelSizeX))
      f.write(";")
      f.write(str(totalLeafArea))
      f.write(";")
      f.write(str(totalSkeletonLength))
      f.write(";")
      f.write(str(totalSkeletonLength/totalLeafArea))
      f.write(";")
      f.write(str(numberSkeletonPieces))
      f.write(";")
      f.write(str(numberEndPoints))
      f.write(";")
      f.write(str(numberBranchingPoints))
      f.write(";")
      f.write(str(numberOfAerioles))
      f.write(";")
      f.write(str(meanAreoleArea))
      f.write(";")
      f.write(str(stdAreoleArea))
      f.write(";")
      f.write(str(currentTimepoint))
      f.write(";")
      
      f.write(phenoVein_getCurrentVersion())
      
      f.write("\n")
      f.close()
    except:
       print("Error in WriteResultsToFile: Could not open: " + collectedResultsFilename + " Maybe opened in Excel?")
      
  
  
  return res