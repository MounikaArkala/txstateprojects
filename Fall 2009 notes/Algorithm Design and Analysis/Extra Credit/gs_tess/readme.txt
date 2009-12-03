Geometry Shader Tessellation demo
by Alex Nankervis

This demo tessellates a heightfield based on distance to the viewer using the geometry shader, with smooth transitions between each tessellation level. The geometry shader isn't really meant for tessellation, but it works well when combined with transform feedback to store the results for later reuse.

The tessellation level is first calculated in the vertex shader based on distance to the viewer. Then, in the geometry shader, per-edge blend factors are calculated to provide a smooth transition between tessellation levels. Triangle strips are output for each row of tessellated triangles generated from the source triangle, with edge triangles pulled towards corner vertices based on the smooth transition adjustment. Finally, in the fragment shader, a color ramp is output to show the tessellation level.

The important code is in the shaders folder - map.shv, map.shg, map.shf.

requires: shader model 4 graphics card

tested on: GeForce 8800 GTX

Controls:
W/S - move camera forward/backward
A/D - move camera side to side
space/control - move camera up/down
mouse - change camera direction
ESC - exit