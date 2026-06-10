Web VPython 3.2
#line above required for glowscript to run

from vpython import *
from random import choice


#----------------------------Declare Globals----------------------------#

pointer_list = []

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

animation_scene.lights = []
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

        pointer_list.append(self)


    def calculate_magnetic_field(self):

        B = background_field + (x_pos * x_gradient) + (y_pos * x_gradient)
        self.magnetic_field = B

    #rotate for 1 ms
    def rotate_self(self):
        print("working")

        # #calculate theta initial
        # unit_vector = target.x_pos / target.raidus
        # theta = acos(unit_vector)

        # #calculate b_field
        # B = self.calculate_magnetic_field(self)
        # angular_velocity = B * rotation_coefficent

        # #find new theta and rotate to it
        # theta = theta + angular_velocity
        # self.pointer.axis = vector(
        #     cos(theta * raidus),
        #     sin(theta * raidus),
        #     0
        # )

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

def rotate_all():

    for i in len(pointer_list):

        pointer_list[i].rotate_self()





#----------------------------Create functions for control pannel----------------------------#

def create_button(chosen_canvas, text, icon):

    #create the button background
    box(
        canvas = chosen_canvas,
        pos=vector(0,0,1),
        length = chosen_canvas.width * .2,
        height = chosen_canvas.height * .2,
        width = 1,
        color = vec(0.5,0.5,0.5),

        shininess = 0,
        opacity = 0.3,
    )

    #create the button icon/image
    label(
        canvas = chosen_canvas,
        pos = vector(0,0,1),
        text = icon,
        height = chosen_canvas.height * .1,
        color = color.black,
        box = False,
        opacity = 0

    )

    #create button text
    label(
        canvas = chosen_canvas,
        pos = vector(0,0,1),
        text = text,
        height = chosen_canvas.height *.1,
        color = color.black,
        box = False,
        opacity = 0
    )

def start_button_clicked(evt):

    rotate_all()

control_panel.bind('click', start_button_clicked)






#----------------------------Basic Running loop behavior----------------------------#


def Run():

    #-------------------Set up animation canvas---------------#

    test_pointer = magnetic_pointer(vector(0,0,0))

    #--------------------Set up control panel------------------#

    #sets up images for the control pannel -jc
    create_button(control_panel, 'Play/Pause', '⏯')

    #tracks the mouse's posistion in the control pannel -jc
    mouse_location = control_panel.mouse.pos



    while True:
        rate(60)


#----------------------------Start the sim----------------------------#

Run()