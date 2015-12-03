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


from mevis import *
import numpy as np
from PythonQt import QtGui

def reset():
  ctx.field("veinLengthAndWidth").setValue('')
  ctx.field("veinThickness.clear").touch()
  
  return

def updateInputs():
  ctx.field("MinMaxScan0.update").touch()
  ctx.field("MinMaxScan1.update").touch()
  ctx.field("MinMaxScan2.update").touch()
  ctx.field("MinMaxScan3.update").touch()
  ctx.field("SkeletonBranchingPoints.update").touch()
  ctx.field("ConnectedComponents.update").touch()
  return

def calcCurrentVeinLengthAndWidth():
  ctx.field("veinThickness.calcVeinThickness").touch()
  ctx.field("SkeletonTotalLength.update").touch()

  



def calcAllVeinLengthAndWidth():
  #updateInputs()
  ctx.field("calculationStopped").setValue(0)
  ctx.field("chooseVeinManually").setValue(0) # allow for automatic vein selection
  
  noVeins = ctx.field("ConnectedComponents.numberOfClusters").value
  
  veinLength = "vein Length [mm]:;"
  veinWidth  = "vein Width [mm]:;"
  widthChiSqr = "vein Width chi square [a.u.]:;"
  
  for i in range(0, noVeins):
  #for i in range(1, 25):
    ctx.field("selectedSingleVein.threshCenter").setValue(i+1)
    ctx.field("SkeletonTotalLength.update").touch()
    ctx.field("veinThickness.calcVeinThickness").touch()
    
    MLAB.processEvents(True)
    if ctx.field("calculationStopped").value:
      print("Stop")
      break 
    
    #if (MLAB.shouldStop()):
    #  print("Stop")
    #  break 
      
    
    # get values
    length = ctx.field("SkeletonTotalLength.totalSkeletonLength").value
    width  = ctx.field("veinThickness.fittedVeinThickness").value
    chiSqr = ctx.field("veinThickness.fittedVeinWidthChiSqr").value
    
    status = (float(i)+1)/float(noVeins);
    ctx.field("status").setValue(status)
    
    veinLength  = veinLength  + str(length) + ";"
    veinWidth   = veinWidth   + str(width)  + ";"
    widthChiSqr = widthChiSqr + str(chiSqr) + ";"
    
  veinLengthAndWidth = veinLength + "\n" + veinWidth + "\n" + widthChiSqr + "\n"
  
  ctx.field("veinLengthAndWidth").setValue(veinLengthAndWidth)
  #ctx.field("veinLength").setValue(veinLength)
  #ctx.field("veinWidth").setValue(veinWidth)
    
  
  return veinLengthAndWidth



def copyResultsToClipboard():
  veinLengthAndWidth = ctx.field("veinLengthAndWidth").value
  QtGui.QApplication.clipboard().setText(veinLengthAndWidth)


