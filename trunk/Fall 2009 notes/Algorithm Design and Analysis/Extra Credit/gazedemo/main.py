#!C:\Panda3D-1.6.2\
#Copyright Luke Paireepinart 2009
__license__ = """
Copyright (c) 2009 Luke Paireepinart

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""

from pandac.PandaModules import loadPrcFile
loadPrcFile("config/Config.prc")

import direct.directbase.DirectStart
from pandac.PandaModules import *

from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
import math

#Load up our room
environ = loader.loadModel('models/abstractroom')
environ.reparentTo(render)


#Enable automatic shader generation by Panda
render.setShaderAuto()

#set up our global mouse position variable
mousepos = Vec4(0,0,0,1)

#task to move camera, called every frame!
def SpinCameraTask(task):
    #just rotates the camera around the origin.
    angledegrees = task.time * 6.0
    angleradians = angledegrees * (math.pi / 180.)
    base.camera.setPos(20*math.sin(angleradians), -20.*math.cos(angleradians), 3)
    base.camera.setHpr(angledegrees, 0, 0)
    return Task.cont
    


#detect the current mouse position.
def mousePos(task):
    
    global mousepos
    # check if the mouse is available
    if not base.mouseWatcherNode.hasMouse():
        return Task.cont
   
    # get the relative mouse position,
    # its always between 1 and -1 for both coords.
    mpos = base.mouseWatcherNode.getMouse()
    temp = tuple(mpos)
    mpos = Vec4(temp[0], temp[1], mousepos[2], mousepos[3])
    #mpos = Vec4(temp[0], temp[1], 0, 1)
    if mpos != mousepos:
        #mouse position changed since last time.
        mousepos = Vec4(mpos[0], mpos[1], mousepos[2], mousepos[3])
        
        #update the shader if mouse position changed.
        environ.setShaderInput("mousepos", mousepos)
        
    return Task.cont 

#these are later bound to keyboard events.
def enableGaze():
    global mousepos
    print "Gaze enabled!"
    #mousepos[2] is used as a hack for whether the effect is enabled, allows us to only pass a single
    # float4 and save time.  it really should be in its own variable.  this is an optimization.
    mousepos = (mousepos[0], mousepos[1], 1, mousepos[3])
    environ.setShaderInput("mousepos", mousepos)
def disableGaze():
    global mousepos
    print "Gaze disabled!"
    mousepos = (mousepos[0], mousepos[1], 0, mousepos[3])
    environ.setShaderInput("mousepos", mousepos)

#spin the camera around and call mousePos every frame.
taskMgr.add(SpinCameraTask, "SpinCameraTask")
taskMgr.add(mousePos, "MousePosition")

#bind arrow_up and arrow_down to call these functions.
base.accept("arrow_up", enableGaze)
base.accept("arrow_down", disableGaze)


#Load a cute panda and make him walk around!
pandaActor = Actor.Actor("models/panda-model", {"walk": "models/panda-walk4"})
pandaActor.setScale(0.005, 0.005, 0.005)
pandaActor.reparentTo(render)
pandaActor.loop("walk")

#create four lerp intervals needed to walk back and forth.
#the panda will move smoothly between each point.
#he will change positions, rotate 180, change positions, rotate 180, and repeat.
pandaPosInterval1 = pandaActor.posInterval(13, Point3(0, -10, 0), startPos=Point3(0,10,0))
pandaPosInterval2 = pandaActor.posInterval(13, Point3(0,10,0), startPos=Point3(0,-10,0))
pandaHprInterval1 = pandaActor.hprInterval(3, Point3(180, 0,0), startHpr=Point3(0,0,0))
pandaHprInterval2 = pandaActor.hprInterval(3, Point3(0,0,0), startHpr = Point3(180,0,0))

#create and play the sequence that coordinates the intervals
pandaPace = Sequence(pandaPosInterval1, pandaHprInterval1, pandaPosInterval2, pandaHprInterval2, name="pandaPace")
pandaPace.loop()


#This is just the lighting code.  not very interesting.
lightpivot = render.attachNewNode("lightpivot")
lightpivot.setPos(0,0,25)
lightpivot.hprInterval(10,Point3(360,0,0)).loop()
plight = PointLight('plight')
plight.setColor(Vec4(1, 1, 1, 1))
plight.setAttenuation(Vec3(0.7,0.05,0))
plnp = lightpivot.attachNewNode(plight)
plnp.setPos(45, 0, 0)
environ.setLight(plnp)
environ.setShaderInput("light", plnp)
# create a sphere to denote the light
sphere = loader.loadModel("models/sphere")
sphere.reparentTo(plnp)


#mousepos is the variable we are going to pass into our shader.  
#it is accessible in CG by k_mousepos.
environ.setShaderInput("mousepos", mousepos)


#load the bumpmapping shader (it's automatically compiled and uploaded to the GPU) and set it as the shader for the environment.
environ.setShader(Shader.load("shaders/bumpMapper.sha"))

#run it!
run()