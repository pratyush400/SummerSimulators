Web VPython 3.2

from vpython import *

#---------------Declare Globals----------------#

#----------------------------Add Hyperlinks-------------------------------#

link1 = document.createElement("a")
link1.href = "https://placeholder.com"
link1.target = "_blank"
link1.innerHTML = "Background"

document.body.prepend(link)

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

animation_scene.range = 1.5
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
    pos=vector(0, 1.3, 0),
    text="Investigating Phase and Frequency Encoding",
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

#---------------Create Functions---------------#

#---------------Setup Objects------------------#

#---------------Setup main loop----------------#

def run():

    while True:

        rate(60)

run()