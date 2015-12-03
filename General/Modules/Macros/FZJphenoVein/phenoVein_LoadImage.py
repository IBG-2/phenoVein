# Copyright (c) 2015, Forschungszentrum J�lich GmbH
# All rights reserved.
# Contributors: Jonas B�hler, Daniel Pflugfelder, Siegfried Jahnke
# Address: Institute of Bio- and Geosciences, Plant Sciences (IBG-2), Forschungszentrum J�lich GmbH, 52428 J�lich, Germany
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


def getPixelSizeFromVector():
  pixelSize = ctx.field("PixelSizeFromVector.resultX").value
  ctx.field("ImagePropertyConvert_setVoxelSize_1.voxelSizeX").setValue(pixelSize)
  ctx.field("ImagePropertyConvert_setVoxelSize_1.voxelSizeY").setValue(pixelSize)
  ## The world matrix is automatically transferred to ImagePropertyConvert_setVoxelSize_2 by MeVisLab
  
  #ctx.field("ImagePropertyConvert_setVoxelSize_2.voxelSizeX").setValue(pixelSize)
  #ctx.field("ImagePropertyConvert_setVoxelSize_2.voxelSizeY").setValue(pixelSize)
  ctx.field("pixelSizeXY").setValue(pixelSize)
  return

def getPixelSizeFromImage():
  ctx.field("ImagePropertyConvert_setVoxelSize_1.getProps").touch()
  #ctx.field("ImagePropertyConvert_setVoxelSize_2.getProps").touch()
  pixelSize = ctx.field("ImagePropertyConvert_setVoxelSize_1.voxelSizeX").value
  ctx.field("pixelSizeXY").setValue(pixelSize)
  return

def setPixelSizeManually():
  newPixelSize = ctx.field("pixelSizeXY").value
  currentPixelSize = ctx.field("ImagePropertyConvert_setVoxelSize_1.voxelSizeX").value
  if newPixelSize != currentPixelSize: # change only if pixelSize has changed to avoid double setting from above functions
    ctx.field("ImagePropertyConvert_setVoxelSize_1.voxelSizeX").setValue(newPixelSize)
    ctx.field("ImagePropertyConvert_setVoxelSize_1.voxelSizeY").setValue(newPixelSize)
    #ctx.field("ImagePropertyConvert_setVoxelSize_2.voxelSizeX").setValue(newPixelSize)
    #ctx.field("ImagePropertyConvert_setVoxelSize_2.voxelSizeY").setValue(newPixelSize)
  return 
