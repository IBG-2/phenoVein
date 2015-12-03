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
import least_sqr
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math



def clearAll():
  ctx.module("PythonImage").call("getInterface").unsetImage()
  ctx.field("fittedVeinThickness").setValue(-1)



amplitudeGlobal = 0.0


def calcThickness(verbose=False):
 
  tic = time.time()
 
  # set default error values for thickness and chiSqr
  ctx.field("fittedVeinThickness").setValue(-1)
  ctx.field("fittedVeinWidthChiSqr").setValue(-1)

 
  plotting   = ctx.field("showFittingPlot").value
  renderVein = ctx.field("renderVein").value
 
  # get input images
  mask_ml = ctx.field("input0").image()
  mask = mask_ml.getTile((0,0,0,0,0,0), mask_ml.imageExtent())

  dis_ml = ctx.field("input1").image()
  dis = dis_ml.getTile((0,0,0,0,0,0), dis_ml.imageExtent())

  image_ml = ctx.field("input2").image()
  image = image_ml.getTile((0,0,0,0,0,0), image_ml.imageExtent())

  # get index for vein edge profile
  ind = np.flatnonzero(mask)

  # check for valid mask
  if ind.size == 0:
    print("Object probably too small, no valid mask found, stop!")
    return

  x   = dis.flat[ind]
  y   = image.flat[ind]
  
  normFactor = np.mean(y)
  #normFactor = np.max(y)
  y=y/normFactor
  
  # ignore norm factor
  normFactor = 1

  xu     = np.unique(x)
  yu     = np.zeros(np.shape(xu))
  weight = np.zeros(np.shape(xu))
  for i in range(len(xu)):
    yi    = y[x==xu[i]]
    yu[i] = np.mean(yi)
    weight[i] = len(yi)

  # check for valid distance 
  if np.min(xu) != 0:
    print("Invalid region of skeleton and surrounding, stop")
    return



  dat      = np.zeros( (len(xu),3), float)
  dat[:,0] = xu
  dat[:,1] = yu
  #dat[:,2] = 1.0/weight      # variante 1 - normal linear weight
  dat[:,2] = 1.0/(weight/(xu+1))  # variante 2 - distance depend weight ~ number of elements in y divided by distance x ("the more far away the less important is this value")
  
  
  ## starting values
  offset      = yu[-1]
  squareWidth = ctx.field("startSquare").value # recommended values ~ [1-3 pixel sizes]
  sigma       = ctx.field("startSigma").value  # recommendes values ~ [ca 1 pixel size]
  amplitude   = yu[0] - offset

  global amplitudeGlobal
  amplitudeGlobal = yu[0]

  ## VARIANTE 1: using a global constant amplitude
  p0 = (offset, squareWidth, sigma)
  costFunction=gauss_edge_3p

  ## VARIANTE 2: amplitude is fitting parameter as well
  #p0 = (offset, squareWidth, sigma, amplitude)
  #costFunction=gauss_edge_4p

  print("pStart: " + str(p0))

  if plotting:
    plt.figure(1)
    plt.cla()
    #plt.plot(x,y*normFactor, '+r')
    #plt.plot(xu,yu*normFactor, '.')
    plt.plot(x,y, '+r')
    plt.plot(xu,yu, '.')
    plt.xlabel("Distance from Skeleton [mm]")
    plt.ylabel("Image Intensity [a.u.]")
    plt.title("Fit of Vein Model")
    plt.legend(['Pixel values', 'Weighted mean values'])
    plt.show()
    plt.draw()
    

  ####################################################################################
  # Fitting
  ticFit    = time.time()
  fitResult = least_sqr.LeastSquares.leastSquaresFit(costFunction,p0,dat,max_iterations=100)
  tocFit    = time.time() - ticFit
  pFit      = fitResult[0]
  pFit[2]   = math.fabs(pFit[2]) # in case sigma is negative (can happen, but we ignore it...)
  fitChiSqr = fitResult[1] / len(xu) 
  ####################################################################################


  if plotting:
    plt.figure(1)
    #print('Time to fit: '+str(np.round(tocFit,2)))
    print("pFit: " + str(pFit))
    xFit = np.linspace(xu[0], xu[-1], 200) 
    yFit = costFunction(pFit, xFit)
    plt.plot(xFit, yFit * normFactor)
    plt.legend(['Pixel values', 'Weighted mean values', 'Fit (chiSqr: '+str(fitChiSqr)+')'])
    plt.draw()
    #plt.figure(2)
    #plt.cla()
    #plt.imshow(np.squeeze(image), cmap = cm.Greys_r)
    ##plt.axes('equal')
    #plt.draw()



  #squareWidth = max(0, pFit[1])
  squareWidth = pFit[1]
  sigma       = pFit[2]
  
  calibrationFactor = math.sqrt(2*math.log(2)) # == FWHM/2    FWHM=2*sqrt(2*ln(2))

  thickness = 2 * (squareWidth + calibrationFactor * sigma )
  
  maxVeinThickness = ctx.field("maxVeinThickness").value  
  
  if thickness > 0:
    ctx.field("fittedVeinThickness").setValue(thickness)
    ctx.field("fittedVeinWidthChiSqr").setValue(fitChiSqr)
    print("Fitted vein width: " + str(thickness))
  else:
    print("Estimated vein thickness negativ, returning -1! Please, check starting values...")


  ## output for visualization
  if (ctx.field("renderVein").value):
    nx = mask_ml.imageExtent()[0]
    ny = mask_ml.imageExtent()[1]
    interface = ctx.module("PythonImage").call("getInterface")
    outMask = interface._image
    #print(np.size(outMask))
    if (outMask == None) or (outMask.size != ny*nx):
      print("Initialize vein boundary mask image")
      outMask = np.ndarray((1,1,1,1,ny,nx), np.uint8())
      outMask = outMask * 0
    if (thickness <= maxVeinThickness) and (thickness > 0):
      outMask[ (dis < thickness/2.0) & (mask==1)] = 1
    else:
      outMask[dis == 0] = 2
    interface.setImage(outMask, minMaxValues = (0,1), voxelToWorldMatrix = mask_ml.voxelToWorldMatrix())
    
  
  #if plotting:
  toc = time.time() - tic
  print("Fitting time: " + str(np.round(toc,2)))

  return


  
def gauss_edge_3p(p,x):
  global amplitudeGlobal
  (offset, squareWidth, sigma) = p
  amplitude = amplitudeGlobal - offset
  y=[amplitude + offset if xi<squareWidth else amplitude*np.exp(-(xi-squareWidth)**2/(2.0*sigma**2))+offset for xi in x]
  return (y)

def gauss_edge_4p(p,x):
  #print(p)
  (offset, squareWidth, sigma, amplitude) = p
  #amplitude = amplitude - offset
  y=[amplitude + offset if xi<squareWidth else amplitude*np.exp(-(xi-squareWidth)**2/(2.0*sigma**2))+offset for xi in x]
  return (y)

