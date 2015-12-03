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
import math



def clearAll():
  ctx.module("PythonImage").call("getInterface").unsetImage()
  ctx.field("fittedVeinThickness").setValue(-1)



amplitudeGlobal = 0.0


def calcThickness(verbose=False):
 
  plotting = ctx.field("showFittingPlot").value
 
  mask_ml = ctx.field("input0").image()
  mask = mask_ml.getTile((0,0,0,0,0,0), mask_ml.imageExtent())

  dis_ml = ctx.field("input1").image()
  dis = dis_ml.getTile((0,0,0,0,0,0), dis_ml.imageExtent())

  image_ml = ctx.field("input2").image()
  image = image_ml.getTile((0,0,0,0,0,0), image_ml.imageExtent())

  ind = np.flatnonzero(mask)
  x   = dis.flat[ind]
  y   = image.flat[ind]
  
  y=y/np.mean(y)


  xu     = np.unique(x)
  yu     = np.zeros(np.shape(xu))
  weight = np.zeros(np.shape(xu))
  for i in range(len(xu)):
    yi    = y[x==xu[i]]
    yu[i] = np.mean(yi)
    weight[i] = len(yi)
  

  dat      = np.zeros( (len(xu),3) ,float)
  dat[:,0] = xu
  dat[:,1] = yu
  dat[:,2] = 1.0/weight
  
  
  ## starting values - NEED TO BE FETCHED FROM MAIN APPLICATION, no constant values here
  offset      = yu[-1]
  #squareWidth = 0.03
  #sigma       = 0.01
  squareWidth = ctx.field("startSquare").value # recommended values ~ 0.03 [1-3 pixel sizes]
  sigma       = ctx.field("startSigma").value  # recommendes values ~ 0.01 [ca 1 pixel size]
#  amplitude   = max(yu) - min(yu)
  global amplitudeGlobal
  amplitudeGlobal = yu[0]


  p0 = (offset, squareWidth, sigma)#, amplitude)
  fitInLogSpace = False  
  costFunction=gauss_edge
  if (fitInLogSpace):
#    p0 = [np.sqrt(pp) for pp in p0]
#    p0 = [np.log(pp) for pp in p0]
#    print(p0)
    p0=list(p0)
 #   p0[1]=np.log(p0[1])
    p0[1]=np.sqrt(p0[1])
    p0=tuple(p0)
#    costFunction=gauss_edge_log_1
#    costFunction=gauss_edge_x2
    costFunction=gauss_edge_x2_1
    
  #global fitInLogSpace
  #if (fitInLogSpace):
  #  p0 = (math.log(offset), math.log(squareWidth), math.log(sigma), math.log(amplitude))
  #else:
  #  p0 = (offset, squareWidth, sigma, amplitude)    
  #print("p0 in logspace: " + str(p0))


  #p0 = (0.1,1,1,1)
  #p0[0] = 0.1
  #p0[1] = 1
  #p0[2] = 1
  #p0[3] = 1

  #x = np.linspace(0,10, 40, )
  #x = range(0,10)
  #y = gauss_edge(p0, x)  + np.random.uniform(0,1000, len(x))

  if plotting:
    plt.figure(1)
    plt.cla()
    plt.plot(x,y, '+r')
    plt.plot(xu,yu, '.')
    plt.xlabel("Distance from Skeleton [mm]")
    plt.ylabel("Normalized Image Intensity [a.u.]")
    plt.title("Fit of Vein Model")
    plt.legend(['Pixel values', 'Mean values'])
    plt.show()
    plt.draw()


  tic = time.time()
  pFit=least_sqr.LeastSquares.leastSquaresFit(costFunction,p0,dat,max_iterations=25)
  pFit = pFit[0]
  if (fitInLogSpace):
#    pFit = [pp**2 for pp in pFit]
#    pFit = [np.exp(pp) for pp in pFit]
#    pFit[1]=np.exp(pFit[1])
    pFit[1]=pFit[1]**2

  toc = time.time() - tic

  if plotting:
    print('Time to fit: '+str(np.round(toc,2)))
    print("pFit: " + str(pFit))
    xFit = np.linspace(xu[0], xu[-1], 200) 
    yFit = gauss_edge(pFit, xFit)
    plt.plot(xFit, yFit)
    plt.legend(['Pixel values', 'Mean values', 'Fit'])
    plt.draw()

  #squareWidth = max(0, pFit[1])
  squareWidth = pFit[1]
  sigma       = pFit[2]

  calibrationFactor = 1

  thickness = 2 * (squareWidth + calibrationFactor*sigma)
  ctx.field("fittedVeinThickness").setValue(thickness)


  ## output for visualization
  nx = mask_ml.imageExtent()[0]
  ny = mask_ml.imageExtent()[1]
  
  interface = ctx.module("PythonImage").call("getInterface")
  outMask = interface._image
  
  if (outMask == None):
    outMask = np.ndarray((1,1,1,1,ny,nx), np.uint8())
     
  maxVeinThickness = ctx.field("maxVeinThickness").value  
  if (thickness <= maxVeinThickness):
    outMask[dis < thickness/2.0] = 1
  else:
    outMask[dis == 0] = 2
     
  interface.setImage(outMask, minMaxValues = (0,1), voxelToWorldMatrix = mask_ml.voxelToWorldMatrix())
  

  return


def gauss_edge_x2(p,x):
  p=[pp**2 for pp in p]
  (offset, squareWidth, sigma, amplitude) = p
  y=[amplitude + offset if xi<squareWidth else amplitude*np.exp(-(xi-squareWidth)**2/(2.0*sigma**2))+offset for xi in x]
  return (y)
def gauss_edge_x2_1(p,x):
#  p=[pp**2 for pp in p]
  (offset, squareWidth, sigma, amplitude) = p
  squareWidth=squareWidth**2
  y=[amplitude + offset if xi<squareWidth else amplitude*np.exp(-(xi-squareWidth)**2/(2.0*sigma**2))+offset for xi in x]
  return (y)

def gauss_edge_log(p,x):
  p=[np.exp(pp) for pp in p]
  (offset, squareWidth, sigma, amplitude) = p
  y=[amplitude + offset if xi<squareWidth else amplitude*np.exp(-(xi-squareWidth)**2/(2.0*sigma**2))+offset for xi in x]
  return (y)
  
def gauss_edge_log_1(p,x):
#  p=[np.exp(pp) for pp in p]
  (offset, squareWidth, sigma, amplitude) = p
  squareWidth=np.exp(squareWidth)
  y=[amplitude + offset +1/squareWidth if xi<squareWidth else amplitude*np.exp(-(xi-squareWidth)**2/(2.0*sigma**2))+offset for xi in x]
  return (y)
  
def gauss_edge(p,x):
  global amplitudeGlobal
  (offset, squareWidth, sigma) = p
  amplitude = amplitudeGlobal - offset
#  (offset, squareWidth, sigma, amplitude) = p
  y=[amplitude + offset if xi<squareWidth else amplitude*np.exp(-(xi-squareWidth)**2/(2.0*sigma**2))+offset for xi in x]
  return (y)

