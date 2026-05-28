from vpython import *

scene = canvas()
scene.background = color.white

scene.camera.pos = vector(0,0,5)
scene.camera.axis = vector(0,0,-5)

s = sphere(pos=vector(0,0,0), raidus=.2, color = color.blue, shininess=0.9)

while True:
    rate(30)


