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


import numpy as np
from mevis import *

def init():
  ctx.field("Bypass.noBypass").setBoolValue(True)
  ctx.field("isUpToDate").setBoolValue(False)
  
  return

def autoUpdateChanged():
  autoUpdate = ctx.field("autoUpdate").value
  isUpToDate = ctx.field("isUpToDate").value
  if autoUpdate and not isUpToDate:
    update()
  return

def inputChanged():
  ctx.field("isUpToDate").setBoolValue(False)
  autoUpdate = ctx.field("autoUpdate").value
  if autoUpdate:
    update()  
  return

def update():
  # set kernel of convolution module
  vs_x = ctx.field("Info.voxelSizeX").value
  vs_y = ctx.field("Info.voxelSizeY").value  
  d    = str(0.5 * 0.9481 * np.sqrt(vs_x*vs_x + vs_y*vs_y))
  x    = str(0.5 * 0.9481 * vs_x)
  y    = str(0.5 * 0.9481 * vs_y)
  kernel = "(*,0,0,0,0,0):    " + d + ",     " + y + ",   " + d + "\n(*,1,0,0,0,0):    " + x + ",    0,    " + x + "\n(*,2,0,0,0,0):    " + d + ",     " + y + ",   " + d
  ctx.field("Convolution.externalKernel").setStringValue(kernel)
  
  # enable bypass
  ctx.field("Bypass.noBypass").setBoolValue(False)
  MLAB.processEvents()

  ########################################
  # calculate skel length
  ########################################
  conv_ml = ctx.field("Convolution.output0").image()
  mask_ml = ctx.field("ImagePropertyConvert.output0").image()
  
  if conv_ml and mask_ml:
    
    conv = conv_ml.getTile((0,0,0,0,0,0), conv_ml.imageExtent())
    mask = mask_ml.getTile((0,0,0,0,0,0), mask_ml.imageExtent())

    #calc totalLength
    totalLength  = np.sum(conv[mask==1.0])
    ctx.field("totalSkeletonLength").setDoubleValue(totalLength)

    # set isUpToDate to True
    ctx.field("isUpToDate").setBoolValue(True )


  # disable bypass
  ctx.field("Bypass.noBypass").setBoolValue(True)
  
  return




