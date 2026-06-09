Web VPython 3.2 
#line above required for glowscript to run

from vpython import *
from random import choice


#----------------------------Create Scenes----------------------------#
animation_scene = canvas(
    width = 1024, 
    height = 480, 
    center = vector(0,0,0), 
    background = vector(1,1,1), 
    resizable = False, 
    userzoom = False, 
    userspin = False
    )

scene.lights = []
distant_light(direction = vector( 0.22, 0.44, 0.88), color = color.white)
distant_light(direction = vector(-0.88, -0.22, -0.44), color = color.white)

control_panel = canvas(
    width =1024, 
    height=100, 
    center = vector(0, 0, 0), 
    background = vec(0.622, 0.779, 0.847), 
    userspin = False, 
    userzoom = False, 
    resizable = False
    )
    
#----------------------------Create Objects----------------------------#

test_object_animation_space = sphere(
    canvas = animation_scene,
    pos = vector(0,0,0),
    radius = 1,
    color = color.red
    )
    
test_object_ctrl_panel = sphere(
    canvas = control_panel,
    pos = vector(0,0,0),
    radius = 1,
    color = color.red
    )