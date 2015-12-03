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


def updateInputs():
  ctx.field("MinMaxScan0.update").touch()
  ctx.field("MinMaxScan1.update").touch()
  ctx.field("MinMaxScan2.update").touch()
  return

#def setInputUpToDate():
#  inputUpToDate0 = ctx.field("MinMaxScan0.upToDate").value
#  inputUpToDate1 = ctx.field("MinMaxScan1.upToDate").value
#  ctx.field("inputUpToDate").setValue(inputUpToDate0 and inputUpToDate1)
#  return 


def saveManualCorrections():
  basicFilename = ctx.field("outFilename").value
  
  # save adding CSOs
  addCSOFilename = basicFilename + "_addCSO.cso"
  ctx.field("SaveAddCSO.fileName").setStringValue(addCSOFilename)
  ctx.field("SaveAddCSO.apply").touch()
  
  # save removing CSOs
  removeCSOFilename = basicFilename + "_removeCSO.cso"
  ctx.field("SaveRemoveCSO.fileName").setStringValue(removeCSOFilename)
  ctx.field("SaveRemoveCSO.apply").touch()

  # save removing Marker
  removeMarkerFilename = basicFilename + "_removeMarker.xml"
  ctx.field("SaveRemoveMarker.filename").setStringValue(removeMarkerFilename)
  ctx.field("SaveRemoveMarker.save").touch()
  return



def loadManualCorrections():
  basicFilename = ctx.field("outFilename").value

  # load adding CSOs
  addCSOFilename = basicFilename + "_addCSO.cso"
  ctx.field("LoadAddCSO.fileName").setStringValue(addCSOFilename)
  ctx.field("LoadAddCSO.apply").touch()
  
  # save removing CSOs
  removeCSOFilename = basicFilename + "_removeCSO.cso"
  ctx.field("LoadRemoveCSO.fileName").setStringValue(removeCSOFilename)
  ctx.field("LoadRemoveCSO.apply").touch()
  
  # load removing Marker
  removeMarkerFilename = basicFilename + "_removeMarker.xml"
  ctx.field("LoadRemoveMarker.filename").setStringValue(removeMarkerFilename)
  ctx.field("LoadRemoveMarker.load").touch()

  return



def calcSkelEndPoints():
  ctx.field("SkeletonizationMacro0.update").touch()
  ctx.field("SkeletonEndPoints.update").touch()
  return 

def calcSkelBranchingPoints():
  ctx.field("SkeletonizationMacro1.update").touch()
  ctx.field("SkeletonBranchingPoints.update").touch()
  return 

def calcSkelLength():
  ctx.field("SkeletonizationMacro2.update").touch()
  ctx.field("SkeletonTotalLength.update").touch()
  return
