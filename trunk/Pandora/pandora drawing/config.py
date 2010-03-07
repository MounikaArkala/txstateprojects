
# scale values from [0->1023] to a more sensible brush size.
pressure_multiplier = 1/1023.
default_pressure = 1023

default_brush_size = 30
default_transparency = 20

#resolution
width  = 800
height = 480
fullscreen = False

### images
images = {'eyedropper': 'imgs/eyedropper.bmp'}

#shit to enable
gamepad = False
pressure = True
pressure_size = True
pressure_trans = True

from pygame.locals import *
#keys for pupnik ;)

buttondown = KEYDOWN
buttonup = KEYUP
keys = {'size+':  K_g, 'size-': K_b,
        'trans+': K_h, 'trans-': K_n,
        'cls': K_c, 'eyedropper': K_e,
        'colorpicker': K_p,
        'replay': K_r,
        'exit': K_q}
        
        
#keys for RPB
"""
gamepad = True
buttondown = JOYBUTTONDOWN
buttonup = JOYBUTTONUP
keys = {'size+':  K_g, 'size-': K_b,
        'trans+': K_h, 'trans-': K_n,
        'cls': K_c, 'eyedropper': 1,
        'colorpicker': 2,
        'replay': 3,
        'exit': K_q}
        

"""