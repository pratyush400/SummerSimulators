Web VPython 3.2
#line above required for glowscript to run

from vpython import *
from random import choice

#----------------------------Declare Globals----------------------------#

pointer_list = []
button_list = []

x_grad = 0
y_grad = 0

Animation_playing = False

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

    def __init__(self, position: vector):
        self.position = position

        self.theta = pi/2

        #set up the circle and arrow for the spinner/position
        self.body = sphere(
                canvas = animation_scene,
                pos = self.position,
                radius = .1,
                color = color.red,
                visible = True
        )
        self.pointer = arrow(
                canvas = animation_scene,
                pos = self.position,
                axis = vector(0, .2, 0),
                shaftwidth =.04, #magnitude/5
                headwidth= .08, #magnitude*2/5
                headlength = .04, #=shaftwidth
                color = color.blue,
                round = True,
                visible = True
        )

        self.magnitude = self.pointer.axis.mag  

        self.magnetic_field = 0

        pointer_list.append(self)


    def calculate_magnetic_field(self):

        #B = background_field + (x_pos * x_gradient) + (y_pos * x_gradient)
        self.magnetic_field = 1 + (x_grad * self.position.x) + (y_grad * self.position.y)
        return self.magnetic_field

    #rotate for 1 ms
    def rotate_self(self):

        B = self.calculate_magnetic_field()
        angular_velocity = pi/180 * B

        self.theta = self.theta + angular_velocity
        self.pointer.axis = vector(
            cos(self.theta) * self.magnitude,
            sin(self.theta) * self.magnitude,
            0
        )


#----------------------------Create 3d Objects for control pannel----------------------------#


class button:

    def __init__(self, chosen_canvas, position, text, icon, action):

        self.canvas = chosen_canvas

        self.position = position

        self.title_text = text

        self.icon_text = icon

        #self.action keeps track of the purpose of the button so it can have behavior when clicked
        self.action = action

        #create the button background
        self.box = box(
            canvas = chosen_canvas,
            pos = position,
            length = .3,
            height = .3,
            width = .001,
            color = vec(0.5,0.5,0.5),

            shininess = 0,
            opacity = 0.3,
        )

        #create the button icon/image
        self.icon = label(
            canvas = chosen_canvas,
            pos = position,
            text = self.icon_text,
            height = 20,
            color = color.black,

            box = False,
            opacity = 0
        )

        #create button text
        self.title = label(
            canvas = chosen_canvas,
            pos = position + vector(0, -.25, 0),
            text = self.title_text,
            height = 12,
            color = color.black,

            box = False,
            opacity = 0
        )

        self.on = False

        button_list.append(self)

    def is_clicked(self, click_pos):

        #check x and y distance from button center
        dx = abs(click_pos.x - self.position.x)
        dy = abs(click_pos.y - self.position.y)

        #both must be within half of the buttons raidus to be True
        return dx <= 0.2 and dy <= 0.2

    def clicked(self):
        self.on = not self.on

        if self.on:
            self.box.color = color.green
        else: self.box.color = vector(.5, .5, .5)

        if self.action:
            self.action(self)



#----------------------------Create functions for animation pannel----------------------------#

def rotate_all():

    #for all pointers (p) in the list, rotate
    for p in pointer_list:

        p.rotate_self()

def adjust_x_gradient(slider):
    x_grad = slider.value

def adjust_y_gradient(slider):
    y_grad = slider.value





#----------------------------Create functions for control pannel----------------------------#


#check to see if any button is triggered on the click
def click_event(event):

    click_pos = event.pos

    #check to see if the click activates any buttons
    for b in button_list:

        if b.is_clicked(click_pos):

            b.clicked()

            break

#Detect when a click happens and call click_event
control_panel.bind('mousedown', click_event)

#assign different function to the different buttons:
def start_button_clicked(button):

    global Animation_playing

    Animation_playing = not Animation_playing

def reset_button_clicked(button):

    for m in pointer_list:
        m.theta = pi/2
        m.pointer.axis = vector(0, m.magnitude, 0)

    button.box.color = vector(.5, .5, .5)

    




#----------------------------Basic Running loop behavior----------------------------#


def Run():

    #-------------------Set up animation canvas---------------#

    # test_pointer = magnetic_pointer(vector(0,0,0))

    for i in range(2):

        for j in range(2):

            magnetic_pointer(vector(i,j,0))
            magnetic_pointer(vector(-i,-j,0))
            magnetic_pointer(vector(-i,j,0))
            magnetic_pointer(vector(i,-j,0))

    #--------------------Set up control panel------------------#

    #create play/pause
    button(control_panel, vector(-3,0,0), 'Play/Pause', '⏯', start_button_clicked)

    #create reset
    button(control_panel, vector(3,0,0), 'Reset', '⟳', reset_button_clicked)

    #tracks the mouse's position in the control pannel -jc
    mouse_location = scene.mouse.pos

#create slider for user control
x_grad_slider = slider(
    bind = adjust_x_gradient,
    min = -10, 
    max = 10, 
    step = .01, 
    value = 0, 
    length = 200,
    width = 10
) 

y_grad_slider = slider(
    bind = adjust_y_gradient,
    min = -10, 
    max = 10, 
    step = .01, 
    value = 0, 
    length = 200,
    width = 10,
    vertical = True
) 


    while True:

        rate(60)

        if Animation_playing == True:
            rotate_all()


#----------------------------Start the sim----------------------------#

Run()