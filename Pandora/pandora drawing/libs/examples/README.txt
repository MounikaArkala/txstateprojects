--Heading---:
PAdLib: Pygame [2D] Advance Graphics Library
Ian Mallett
MArch 2008 - May 2008

Have fun!


--Instructions--:
Run the included example files.
Then look at their code to see how they work.
Most of the Examples' code fit onto one page!  (The comments make them longer).
DO NOT BOTHER TRYING TO RUN padlib.py!  It is a library, and by itself, does nothing.  Look at the tutorials.  


---Usage---:
To use PAdLib in your games, take padlib.py or padlib.pyc and place it in your project folder.  
Import it from your main and do what you want to do, as per the examples.  


---To Do---:
Planned Features:
-Maybe smooth dashed lines?
-Make arbitrary polygonal occluders for shadows and particles?

Email me at ian@geometrian.com to suggest new ideas!  (And really, go ahead, don't be afraid, I need new ideas for this, just no spam allowed).


---License---:
Obviously, this is a library, and I am providing it for free.  
You may use it in any of your projects.
Just keep your integrity, and don't write something like: "I made this program." at the top of my library, (which would be a big fat lie).


---Credits---:
John Eriksson (wmjoers) provided the underlying Shadow code, which I modified here.


---Changes---:
Changes:
v.5.0.0:
 Made Beizer curves with n control points, updated relevant demo
 Made the Rounded Rectangles method more efficient and customizable.  Added transparency
v.4.0.0:
 Added DashedLine() and Demo
 Added BezierCurve()/aaBeizerCurve() and Demo
 Added Particles/Shadows Demo
 Made fewer occluders in Particles Demo
v.3.0.0:
 Added optional Gravity, Collision Detection, and Bouncing to particle_system()
 Added support for Psyco
v.2.0.0:
 Added pygame.init() which fixes bug in PyGame 1.7
 Added RoundedRect() and Demo 
v.1.0.0 - original release:
 Had:
  particle_system()
  Shadow()
  antialias()
  aacircle()