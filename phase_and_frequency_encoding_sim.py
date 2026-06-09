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
    
#----------------------------Create Objects for animation pannel----------------------------#

#create an empty list to track all the arrow assets

#create a class that contains all infromation needed for rotating the "magnetic pointers" at different speeds
class magnetic_pointer:

    def __init__(self, posistion):
        self.posistion = posistion

        #set up the circle and arrow for the spinner/posistion
        self.body = sphere(
                canvas = animation_scene,
                pos = self.posistion,
                radius = .5,
                color = color.red,
                visible = True
            )
        self.pointer = arrow(
                canvas = animation_scene,
                pos = self.posistion,
                axis = vector(0, 1, 0),
                shaftwidth =.2,
                headwidth= .4,
                headlength = .15,
                color = color.blue,
                round = True,
                visible = True
            )

        self.magnetic_field = 0


    def calculate_magnetic_field(self):

        B = background_field + (x_pos * x_gradient) + (y_pos * x_gradient)
        self.magnetic_field = B

    #rotate for 1 ms
    def rotate_self(self):

        #calculate theta initial
        unit_vector = target.x_pos / target.raidus
        theta = invcos(unit_vector)

        #calculate b_field
        B = calculate_magnetic_field(self)
        angular_velocity = B * rotation_coefficent

        #find new theta and apply changes
        theta = theta + angular_velocity
        self.pointer.axis = vector(
            cos(theta * raidus),
            sin(theta * raidus),
            0
        )

# test_object_animation_space = sphere(
#     canvas = animation_scene,
#     pos = vector(0,0,0),
#     radius = 1,
#     color = color.red,
#     visible = False
#     )

# test_arrow = arrow(
#     canvas = animation_scene,
#     pos = vector(0, 0, 0),
#     axis = vector(0, 1, 0),
#     shaftwidth =.2,
#     headwidth= .4,
#     headlength = .15,
#     color = color.blue,
#     round = True,
#     visible = True
#)

#----------------------------Create Objects for control pannel----------------------------#

    
# test_object_ctrl_panel = sphere(
#     canvas = control_panel,
#     pos = vector(0,0,0),
#     radius = 1,
#     color = color.red,
#     visible = False
#     )


#----------------------------Create functions for animation pannel----------------------------#






#----------------------------Create functions for control pannel----------------------------#





#----------------------------Basic Running loop behavior----------------------------#


def Run():
    
    
    #tracks the mouse's posistion in the control pannel -jc
    loc_b = control_panel.mouse.pos

    test_pointer = magnetic_pointer(vector(0,0,0))


#----------------------------Start the sim----------------------------#

Run()
