Web VPython 3.2

from vpython import *
from random import *

#---------------Declare Globals----------------#

button_list = []
X_Ray_list = []

#----------------------------Add Hyperlinks-------------------------------#

link1 = document.createElement("a")
link1.href = "https://placeholder.com"
link1.target = "_blank"
link1.innerHTML = "Background"

document.body.prepend(link1)

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

#animation_scene.range = 1.5
animation_scene.lights = []
distant_light(direction = vector( 0.22, 0.44, 0.88), color = color.white)
distant_light(direction = vector(-0.88, -0.22, -0.44), color = color.white)


control_panel = canvas(
    width =1024,
    height=100,
    center = vector(0, 0, 0),
    background = vector(0.622, 0.779, 0.847),
    userspin = False,
    userzoom = False,
    resizable = False
)   

#----------------------------Create Title / Links-----------------------------#

title = label(
    canvas=animation_scene,
    pos=vector(0, 2, 0),
    text = "Effects of Scattering on X-Ray Imaging",
    height=25,
    color=color.black,
    box=False,
    opacity=0
)


#---------------Create Classes-----------------#

class slider3d:

    def __init__(self, chosen_canvas, start_pos, end_pos, min_value, max_value, labeltext):
        self.canvas = chosen_canvas
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        #create an axis that moves from the start point to the end point
        self.axis = end_pos - start_pos

        self.min_value = min_value
        self.max_value = max_value
        self.current_value = (self.min_value + self.max_value) / 2

        self.body = cylinder(

            canvas = self.canvas,
            pos = self.start_pos,
            axis = self.axis,
            radius = .03,
            color = color.black,
            visible = True

        )

        self.slide = box(
            canvas = self.canvas,

            pos = self.start_pos + .5 * self.axis + vector(0,0,.04),
            length = .16,                
            height = .16,                
            width = .01,                 
            color = vector(.4, .4, .4)
        )

        self.label = text(
            text = labeltext,
            pos = self.start_pos + .45 * self.axis + .2 * norm(cross(self.axis, vector(0,0,1))),
            axis = self.axis,
            height = 0.08,
            depth = 0.004,
            color = color.black
        )

        self.dragging = False

        slider_list.append(self)

    def update_value(self):
        percent_full = dot(self.slide.pos - self.start_pos, norm(self.axis)) / mag(self.axis)

        self.current_value = self.min_value + (self.max_value - self.min_value) * percent_full

    def is_clicked(self, click_pos):

        return mag(click_pos - self.slide.pos) <= .1
        
        
    def move(self):

        #establish new relitive location

        loc_rel = animation_scene.mouse.pos - self.start_pos

        #calculate % of slider active
        loc_percentage = dot(loc_rel, self.axis) / mag2(self.axis)

        #set bounds for slider range

        if loc_percentage < 0:
            loc_percentage = 0
        elif loc_percentage > 1:
            loc_percentage = 1

        #move
        self.slide.pos = self.start_pos + (self.axis * loc_percentage) + vector(0,0,.04)

class button:

    def __init__(self, chosen_canvas, position, text, icon, action):

        self.canvas = chosen_canvas

        self.position = position

        #self.action keeps track of the purpose of the button so it can have behavior when clicked
        self.action = action

        #create the button background
        self.box = box(
            canvas = chosen_canvas,
            pos = position,
            length = .3,
            height = .3,
            width = .001,
            color = vector(0.5,0.5,0.5),

            shininess = 0,
            opacity = 0.3,
        )

        #create the button icon/image
        self.icon = label(
            canvas = chosen_canvas,
            pos = position,
            text = icon,
            height = 20,
            color = color.black,

            box = False,
            opacity = 0
        )

        #create button text
        self.title = label(
            canvas = chosen_canvas,
            pos = position + vector(0, -.25, 0),
            text = text,
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
        #swap on/off state
        self.on = not self.on

        #set color correctly if on/off
        if self.on:
            self.box.color = color.green
        else: self.box.color = vector(.5, .5, .5)

        #call the function associated with the button
        if self.action:
            self.action(self)

class X_Ray:


    def __init__(self, interaction_pos):

        #set up path from emitter to paitent

        self.body_emmited = cylinder(

            canvas = animation_scene,
            pos = vector(0, 1.5, 0),
            axis = interaction_pos - emission_box.pos,
            radius = .03,
            color = color.blue,
            visible = False

        )

        #set up object/attribute to store ray fron paitent to photo.
        self.body_interacted = cylinder(
            
            canvas = animation_scene,
            pos = interaction_pos,
            axis = vector(0,0,0),
            radius = .03,
            color = color.blue,
            visible = False

        )

        X_Ray_list.append(self)

    
    def interaction(self):
        pass

        scatter_roll = random.randint(1,10)
        #create a die roll to determine if ray should diflect.

        #If the particle is not difelcted keep the path straight

        if scatter_roll <= 3:
            self.body_interacted.axis = self.body_emmited.axis

        #If the particles is diflected diflect in one of two directions
        if scatter_roll > 3:

            #direction coinflip
            direction_coinflip = random.randint(0,1)

            if direction_coinflip == 0:
                self.body_interacted.axis = self.body_emmited.axis + vector(self.body_interacted.axis.mag,0,0)
            if direction_coinflip == 1:
            self.body_interacted.axis = self.body_emmited.axis - vector(self.body_interacted.axis.mag,0,0)




#---------------Create Functions---------------#

def clear_rays():
    global X_Ray_list

    X_Ray_list = []


#---------------Click Functionality------------#

def click_event_anim(event):

    pass

animation_scene.bindreturn('mousedown', click_event_anim)

def click_event_ctrl(event):

    click_pos = event.pos

    #check to see if the click activates any buttons
    for b in button_list:

        if b.is_clicked(click_pos):

            b.clicked()

            return

control_panel.bind('mousedown', click_event_ctrl)

def unclick(event):
    pass

control_panel.bind('mouseup', unclick)
animation_scene.bind('mouseup', unclick)


#---------------Setup Objects------------------#

emission_box = box(
            canvas = animation_scene,

            pos = vector(0, 1.5, 0),
            length = .1,                
            height = .1,                
            width = .1,                 
            color = vector(.4, .4, .4)
            texture = ""
        )
    
paitent_placeholder_line = cylinder(

            canvas = animation_scene,

            pos = vector(-1.5, .5, 0),
            axis = vector(3,0,0),
            radius = .03,
            color = color.black,
            visible = True

        )

screen_placeholder_line = cylinder(

            canvas = animation_scene,

            pos = vector(-1.5, -.5, 0),
            axis = vector(3,0,0),
            radius = .03,
            color = color.black,
            visible = True

        )

paitent_picture_placeholder = box(
            canvas = animation_scene,

            pos = vector(0,0,0),
            length = .1,                
            height = .1,                
            width = .1,                 
            color = vector(.4, .4, .4)
        )


ctrlbox = box(
            canvas = control_panel,

            pos = vector(0,0,0),
            length = 1,                
            height = 1,                
            width = 1,                 
            color = vector(.4, .4, .4)
        )

#---------------Setup main loop----------------#

def run():

    while True:

        rate(60)

run()