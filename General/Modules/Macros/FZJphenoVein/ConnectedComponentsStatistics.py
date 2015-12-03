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
import numpy


def applyUpdateMode():
  updateMode = ctx.field("updateMode").value
  if updateMode == "autoUpdate":
    updateStatistics()
  elif updateMode == "autoClear":
    clearStatistics()
  else:
    pass


def clearStatistics():
  ctx.field("cchistMarkerListContainer.deleteAll").touch()



def updateStatistics():
  ctx.field("BaseBypass.bypass").setBoolValue(False)
  imageExtent = ctx.field("input0").image().imageExtent()
  print(imageExtent)
  clearStatistics()
  updateWeightImage(imageExtent)
  updateHistograms()
  objectSizes = getObjectSizes()
  centroids   = getCentroids(objectSizes, imageExtent)
  addMarkersForConnectedComponents(centroids, objectSizes)
  ctx.field("BaseBypass.bypass").setBoolValue(True)
  


def updateWeightImage(imageExtent):
  weightModules = {"XRamp":imageExtent[0], "YRamp":imageExtent[1], "ZRamp":imageExtent[2]}
  for moduleName in weightModules.keys():
    setWeightImage(moduleName, weightModules[moduleName], imageExtent)


def setWeightImage(moduleName, maxValue, imageExtent):
  ctx.field(moduleName + ".fillValue").value = 1
  ctx.field(moduleName + ".fillValue2").value = maxValue
  ctx.field(moduleName + ".sizeX").value = imageExtent[0]
  ctx.field(moduleName + ".sizeY").value = imageExtent[1]
  ctx.field(moduleName + ".sizeZ").value = imageExtent[2]
  ctx.field(moduleName + ".apply").touch()
  
  
def updateHistograms():
  ctx.field("Histogram_objectSizes.update").touch()
  ctx.field("Histogram1.update").touch()
  ctx.field("Histogram2.update").touch()
  ctx.field("Histogram3.update").touch()


def getObjectSizes():
  objectSizes = ctx.field("Histogram_objectSizes.outputHistogramCurve").object().getYSlice(0)
  objectSizes = numpy.array(objectSizes)
  return objectSizes


def getCentroids_2D(objectSizes, imageExtent):
  X = ctx.field("Histogram1.outputHistogramCurve").object().getYSlice(0)
  X = numpy.array(X)
  X = X / objectSizes * imageExtent[0]

  Y = ctx.field("Histogram2.outputHistogramCurve").object().getYSlice(0)
  Y = numpy.array(Y)
  Y = Y / objectSizes * imageExtent[1]

  return (X, Y)

def getCentroids_3D(objectSizes, imageExtent):
  X = ctx.field("Histogram1.outputHistogramCurve").object().getYSlice(0)
  X = numpy.array(X)
  X = X / objectSizes * imageExtent[0]

  Y = ctx.field("Histogram2.outputHistogramCurve").object().getYSlice(0)
  Y = numpy.array(Y)
  Y = Y / objectSizes * imageExtent[1]

  Z = ctx.field("Histogram3.outputHistogramCurve").object().getYSlice(0)
  Z = numpy.array(Z)
  Z = Z / objectSizes * imageExtent[2]
  return (X, Y, Z)



def addMarkersForConnectedComponents(centroids, objectSizes):
  for clusterId in range(len(objectSizes)):
    pos = (float(centroids[0][clusterId]),  float(centroids[1][clusterId]),   float(centroids[2][clusterId]) )
    addMarker(pos, objectSizes[clusterId])


def addMarker(pos, numVoxels):
  ctx.field("cchistMarkerListContainer.add").touch()
  position = mapVoxelToWorld(pos)  
  ctx.field("cchistMarkerListContainer.posXYZ").value = position
  ctx.field("cchistMarkerListContainer.type").value = numVoxels


def mapVoxelToWorld(voxelPosition):
  return ctx.field("ConnectedComponents.output0").mapVoxelToWorld(voxelPosition)

  
  