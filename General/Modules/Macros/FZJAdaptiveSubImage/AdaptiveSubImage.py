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



def input0Changed():
  if (ctx.field("autoUpdate").value):
    update()
  return

def valueChanged():
  autoUpdate = ctx.field("autoUpdate").value
  if autoUpdate:
    update()
  #ctx.field("SubImage0.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage1.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage2.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage3.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage4.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage5.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage6.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage7.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage8.autoApply").setBoolValue(autoUpdate)
  #ctx.field("SubImage9.autoApply").setBoolValue(autoUpdate)
  return
  


def update():
  input0_ml = ctx.field("input0").image()

  if not input0_ml:
    #print("here_1")
    return
  
  input0    = input0_ml.getTile((0,0,0,0,0,0), input0_ml.imageExtent())
  idx = np.where(input0 > 0)
  
  if (len(idx[5]) == 0) or (len(idx[4]) == 0) :
    #print("here_2")
    return

  paddingSize = ctx.field("paddingSize").value
  minX = min(idx[5]) - paddingSize
  maxX = max(idx[5]) + paddingSize
  minY = min(idx[4]) - paddingSize
  maxY = max(idx[4]) + paddingSize
  if ctx.field("2DOnly").value:
    minZ = 0
    maxZ = 0
  else:
    minZ = min(idx[3]) - paddingSize
    maxZ = max(idx[3]) + paddingSize
    
  # deactivate autoUpdate
  #autoUpdate = ctx.field("autoUpdate").value
  #ctx.field("autoUpdate").setBoolValue(False)
  #valueChanged()
  #MLAB.processEvents()
  
  ctx.field("x1").setValue(minX)
  ctx.field("x2").setValue(maxX)
  ctx.field("y1").setValue(minY)
  ctx.field("y2").setValue(maxY)
  ctx.field("z1").setValue(minZ)
  ctx.field("z2").setValue(maxZ)

  # SubImage0
  ctx.field("SubImage0.x" ).setValue(minX)
  ctx.field("SubImage0.sx").setValue(maxX)
  ctx.field("SubImage0.y" ).setValue(minY)
  ctx.field("SubImage0.sy").setValue(maxY)
  ctx.field("SubImage0.z" ).setValue(minZ)
  ctx.field("SubImage0.sz").setValue(maxZ)

  # SubImage1
  ctx.field("SubImage1.x" ).setValue(minX)
  ctx.field("SubImage1.sx").setValue(maxX)
  ctx.field("SubImage1.y" ).setValue(minY)
  ctx.field("SubImage1.sy").setValue(maxY)
  ctx.field("SubImage1.z" ).setValue(minZ)
  ctx.field("SubImage1.sz").setValue(maxZ)

  # SubImage2
  ctx.field("SubImage2.x" ).setValue(minX)
  ctx.field("SubImage2.sx").setValue(maxX)
  ctx.field("SubImage2.y" ).setValue(minY)
  ctx.field("SubImage2.sy").setValue(maxY)
  ctx.field("SubImage2.z" ).setValue(minZ)
  ctx.field("SubImage2.sz").setValue(maxZ)

  # SubImage3
  ctx.field("SubImage3.x" ).setValue(minX)
  ctx.field("SubImage3.sx").setValue(maxX)
  ctx.field("SubImage3.y" ).setValue(minY)
  ctx.field("SubImage3.sy").setValue(maxY)
  ctx.field("SubImage3.z" ).setValue(minZ)
  ctx.field("SubImage3.sz").setValue(maxZ)

  # SubImage4
  ctx.field("SubImage4.x" ).setValue(minX)
  ctx.field("SubImage4.sx").setValue(maxX)
  ctx.field("SubImage4.y" ).setValue(minY)
  ctx.field("SubImage4.sy").setValue(maxY)
  ctx.field("SubImage4.z" ).setValue(minZ)
  ctx.field("SubImage4.sz").setValue(maxZ)

  # SubImage5
  ctx.field("SubImage5.x" ).setValue(minX)
  ctx.field("SubImage5.sx").setValue(maxX)
  ctx.field("SubImage5.y" ).setValue(minY)
  ctx.field("SubImage5.sy").setValue(maxY)
  ctx.field("SubImage5.z" ).setValue(minZ)
  ctx.field("SubImage5.sz").setValue(maxZ)

  # SubImage6
  ctx.field("SubImage6.x" ).setValue(minX)
  ctx.field("SubImage6.sx").setValue(maxX)
  ctx.field("SubImage6.y" ).setValue(minY)
  ctx.field("SubImage6.sy").setValue(maxY)
  ctx.field("SubImage6.z" ).setValue(minZ)
  ctx.field("SubImage6.sz").setValue(maxZ)

  # SubImage7
  ctx.field("SubImage7.x" ).setValue(minX)
  ctx.field("SubImage7.sx").setValue(maxX)
  ctx.field("SubImage7.y" ).setValue(minY)
  ctx.field("SubImage7.sy").setValue(maxY)
  ctx.field("SubImage7.z" ).setValue(minZ)
  ctx.field("SubImage7.sz").setValue(maxZ)

  # SubImage8
  ctx.field("SubImage8.x" ).setValue(minX)
  ctx.field("SubImage8.sx").setValue(maxX)
  ctx.field("SubImage8.y" ).setValue(minY)
  ctx.field("SubImage8.sy").setValue(maxY)
  ctx.field("SubImage8.z" ).setValue(minZ)
  ctx.field("SubImage8.sz").setValue(maxZ)

  # SubImage9
  ctx.field("SubImage9.x" ).setValue(minX)
  ctx.field("SubImage9.sx").setValue(maxX)
  ctx.field("SubImage9.y" ).setValue(minY)
  ctx.field("SubImage9.sy").setValue(maxY)
  ctx.field("SubImage9.z" ).setValue(minZ)
  ctx.field("SubImage9.sz").setValue(maxZ)

  # updates
  ctx.field("SubImage0.apply").touch()
  ctx.field("SubImage1.apply").touch()
  ctx.field("SubImage2.apply").touch()
  ctx.field("SubImage3.apply").touch()
  ctx.field("SubImage4.apply").touch()
  ctx.field("SubImage5.apply").touch()
  ctx.field("SubImage6.apply").touch()
  ctx.field("SubImage7.apply").touch()
  ctx.field("SubImage8.apply").touch()
  ctx.field("SubImage9.apply").touch()
  
  
  ## set original autoUpdate value
  #ctx.field("autoUpdate").setBoolValue(autoUpdate)

    