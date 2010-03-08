#!/usr/local/bin/python
# by Daniel Rosengren

import sys, time
stdout = sys.stdout

BAILOUT = 16
MAX_ITERATIONS = 1000

class Iterator:
  def __init__(self):
    print 'Rendering...'
    self.MAX_ITERATIONS = 1000
    temp = []
    for y in range(-39, 39):
      #stdout.write('\n')
      temp.append('\n')
      for x in range(-39, 39):
        i = self.mandelbrot(x/40.0, y/40.0)
        
        if i == 0:
          temp.append('*')
          #stdout.write('*')
        else:
          temp.append(' ')
          #stdout.write(' ')
    print "".join(temp)
    
  def mandelbrot(self, x, y):
    cr = y - 0.5
    ci = x
    zi = 0.0
    zr = 0.0
    i = 0

    while True:
      i += 1
      temp = zr * zi
      zr2 = zr * zr
      zi2 = zi * zi
      zr = zr2 - zi2 + cr
      zi = temp + temp + ci
 		  
      if zi2 + zr2 > BAILOUT:
        return i
      if i > MAX_ITERATIONS:
        return 0

t = time.time()
Iterator()
print '\nPython Elapsed %.02f' % (time.time() - t)
