Web VPython 3.2
#line above required for glowscript to run

from vpython import *
from random import choice

#----------------------------Declare Globals----------------------------#

pointer_list = [] #list to store magentic pointers
button_list = []
slider_list = []
arrow_list = [] #list to store the memory arrows for the picture function
label_list = [] #list of all the average value calculation objects

x_grad = 0
y_grad = 0

Animation_playing = False

gradient_active = False


#----------------------------Add Hyperlinks-------------------------------#

#create an invisable canvas, if you dont glowscript doesnt like it

# scene = canvas(width=0, height=0)

link = document.createElement("a")
link.href = "https://medicalimaging.watzekdi.net/images/mri_images/Slice%20Selection/Background-Phase%26FreqEncoding_new.png"
link.target = "_blank"
link.innerHTML = "Background"

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

#----------------------------Create Objects for animation pannel----------------------------#

#create an empty list to track all the arrow assets

#create a class that contains all infromation needed for rotating the "magnetic pointers" at different speeds
class magnetic_pointer:

    def __init__(self, position):
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

        self.frequency = 0


        #this is horrable, and unreadable but glowscript requires it to be one line
        #i have included a readable version below
        #note: readable version needs updating, but the basic structure is there

        self.text_representation = [box(canvas=animation_scene, pos=self.position + vector(0, 0, .1), length=.5, height=.5, width=.001, color=vector(0.5,0.5,0.5), shininess=0, opacity=1, visible=False), label(canvas=animation_scene, text='frequency =', pos=self.position + vector(0,0.15,.11), height=12, depth=0.02, color=color.black, box = False, opacity=0, visible=False), label(canvas=animation_scene, text='angle = ', pos=self.position+vector(0,-0.1,.11), height = 12, depth=0.02, color=color.black, box=False, opacity=0, visible=False)]

        # self.text_representation = [
        #     box(
        #         canvas=animation_scene,
        #         pos=self.position + vector(0, 0, .1),
        #         length=.5,
        #         height=.5,
        #         width=.001,
        #         color=vector(0.5, 0.5, 0.5),
        #         shininess=0,
        #         opacity=1,
        #         visible=False
        #     ),
        #     label(
        #         canvas=animation_scene,
        #         text='frequency =',
        #         pos=self.position + vector(0, 0.15, .11),
        #         height=12,
        #         depth=0.02,
        #         color=color.black,
        #         box=False,
        #         opacity=0,
        #         visible=False
        #     ),
        #     label(
        #         canvas=animation_scene,
        #         text='angle = ',
        #         pos=self.position + vector(0, -0.1, .11),
        #         height=12,
        #         depth=0.02,
        #         color=color.black,
        #         box=False,
        #         opacity=0,
        #         visible=False
        #     )
        # ]

        pointer_list.append(self)


    def calculate_magnetic_field(self):

        #B = background_field + (x_pos * x_gradient) + (y_pos * x_gradient)

        B = 3

        if gradient_active:
            B += (slider_list[0].current_value * self.position.x) + (slider_list[1].current_value * self.position.y)

        self.magnetic_field = B
        return self.magnetic_field

    #rotate for 1 timeframe
    def rotate_self(self):

        B = self.calculate_magnetic_field()
        #use factor to adjust rotation speed to be accurate to real MRI, note 1 second real time = .01ms simulation time
        angular_velocity = ( ( ( ( 2 * pi ) * .42 ) / 3) * B)/60

        self.theta = self.theta + angular_velocity
        self.pointer.axis = vector(
            cos(self.theta) * self.magnitude,
            sin(self.theta) * self.magnitude,
            0
        )

        if self.theta >= 2*pi:
            self.theta = self.theta - (2*pi)

    def calculate_frequency(self):

        B = self.calculate_magnetic_field()

        angular_velocity = ( ( ( ( 2 * pi ) * .42 ) / 3) * B)

        self.frequency = angular_velocity / (2*pi)

        return self.frequency


#create a class so we can include sliders in the animation pannel

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

class average_label:
    
    def __init__(self, pos, targets):

        self.targets = targets

        self.value = 0

        #caculate value based on the average value of the targets
        for target in targets:
            target.calculate_frequency()
            self.value += target.frequency
        
        self.value = self.value / len(targets)

        self.position = pos

        #create main structure of the average
        self.body = box(
            canvas = animation_scene,
            pos = self.position,
            length = .5,
            height = .2,
            width = .001,
            color = vector(0.5,0.5,0.5),

            shininess = 0,
            opacity = 0.3,
        )

        #create text
        self.text = label(
            canvas = animation_scene,
            pos = self.position + vector(0, .04, 0.02),
            text = f'ν \n{self.value}',
            height = 10,
            color = color.black,

            box = False,
            opacity = 0
        )

        label_list.append(self)

    def update(self):
        
        self.value = 0

        for target in self.targets:
            target.calculate_frequency()
            self.value += target.frequency
        
        self.value = self.value / len(self.targets)

        self.text.text = f'ν \n {self.value:.4f}'



#----------------------------Create 3d Objects for control pannel----------------------------#


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



#----------------------------Create functions for animation pannel----------------------------#

def rotate_all():

    #for all pointers (p) in the list, rotate
    for p in pointer_list:

        p.rotate_self()






#----------------------------Create functions for control pannel----------------------------#


#check to see if any button is triggered on the click
def click_event_ctrl(event):

    click_pos = event.pos

    #check to see if the click activates any buttons
    for b in button_list:

        if b.is_clicked(click_pos):

            b.clicked()

            return

def click_event_anim(event):

    global gradient_active

    click_pos = event.pos

    for s in slider_list:

        if s.is_clicked(click_pos):
            s.dragging = True

            #automattically turn the gradient on when the slider is moved
            if not gradient_active:
                gradient_active = True


            #allow x_slide to appear after the y_slider used
            for obj in slider_list:
                obj.body.visible = True
                obj.slide.visible = True
                obj.label.visible = True

            return

def unclick(event):
    for s in slider_list:
        s.dragging = False

#Detect when a click happens and call click_event
control_panel.bind('mousedown', click_event_ctrl)
animation_scene.bind('mousedown', click_event_anim)

#Detect when the mouse is lifed so we dont do unintentional functions
control_panel.bind('mouseup', unclick)
animation_scene.bind('mouseup', unclick)

#assign different function to the different buttons:
def start_button_clicked(button):

    global Animation_playing

    Animation_playing = not Animation_playing

    if button.on == True:
        button_list[0].title.text = 'Pause'

    if button.on == False:
        button_list[0].title.text = 'Play'

# def gradient_button(button):

#     global gradient_active

#     gradient_active = not gradient_active

def take_picture(button):

    global arrow_list

    for i, m in enumerate(pointer_list):

        m.text_representation[1].text =f"Frequency = \n {m.calculate_frequency():.4f} Hz"
        m.text_representation[2].text =f"Theta = \n {m.theta:.4f} rad"

        #blueshift
        if m.calculate_magnetic_field() > 3:

            m.text_representation[0].color = vector(0, .1, 0) + vector(0, 0, m.calculate_frequency()/.42)

        #redshift
        else if m.calculate_magnetic_field() < 3: 

            m.text_representation[0].color = vector(0, .1, .1) + vector(m.calculate_frequency()/.42, 0, 0)

        else if m.calculate_magnetic_field() == 3:

            m.text_representation[0].color = vector(.1, 0, .1) + vector(0, m.calculate_frequency()/.42, 0)


        for j in m.text_representation:

            if button.on == True:
                j.visible = True

            if button.on == False:
                j.visible = False


    #create the arrows for visual representation
    if button.on == True:

        reset_arrow_memoryow_memory()

        for m in pointer_list:
            arrow_list.append(
                arrow(
                    canvas = animation_scene,
                    pos = m.position*.6 + vector(1.5,0,0),
                    axis = m.pointer.axis,
                    shaftwidth =.04, #magnitude/5
                    headwidth= .08, #magnitude*2/5
                    headlength = .04, #=shaftwidth
                    color = color.blue,
                    round = True,
                    visible = True
                )
            )
    




def reset_button_clicked_pointers(button):

    for m in pointer_list:
        m.theta = pi/2
        m.pointer.axis = vector(0, m.magnitude, 0)

    button.box.color = vector(.5, .5, .5)

def reset_button_clicked_sliders(button):

    for s in slider_list:
        s.slide.pos = s.start_pos + s.axis * .5 + vector(0,0,.04)
        s.current_value = (s.max_value + s.min_value) / 2

    button.box.color = vector(.5, .5, .5)

    global gradient_active

    gradient_active = False

def reset_arrow_memoryow_memory():
    
    global arrow_list

    for a in arrow_list:
        a.visible = False
    
    arrow_list = []





#----------------------------Basic Running loop behavior----------------------------#


def Run():

    #-------------------Set up animation canvas---------------#
    animation_scene.select()

    #bottom row
    pointer1 = magnetic_pointer(vector(-0.6, -0.6, 0))
    pointer2 = magnetic_pointer(vector( 0.0, -0.6, 0))
    pointer3 = magnetic_pointer(vector( 0.6, -0.6, 0))

    #middle row
    pointer4 = magnetic_pointer(vector(-0.6,  0.0, 0))
    pointer5 = magnetic_pointer(vector( 0.0,  0.0, 0))
    pointer6 = magnetic_pointer(vector( 0.6,  0.0, 0))

    #top row
    pointer7 = magnetic_pointer(vector(-0.6,  0.6, 0))
    pointer8 = magnetic_pointer(vector( 0.0,  0.6, 0))
    pointer9 = magnetic_pointer(vector( 0.6,  0.6, 0))

    #create averages forcollumns
    average_label(vector(-.6,1,0),[pointer1, pointer4, pointer7])
    average_label(vector(0,1,0),[pointer2, pointer5, pointer8])
    average_label(vector(.6,1,0),[pointer3, pointer6, pointer9])

    #create averages for rows
    average_label(vector(-1.4,-.6,0),[pointer1, pointer2, pointer3])
    average_label(vector(-1.4,0,0),[pointer4, pointer5, pointer6])
    average_label(vector(-1.4,.6,0),[pointer7, pointer8, pointer9])    

    #create sliders
    #do not break sliders (or any class for that matter) into multiple lines, this breaks glowscripts ability to translate into js.
    x_slider = slider3d(animation_scene, vector(-1,-1,0), vector(1,-1,0), -3, 3, 'x gradient')

    #x_slider not suppoed to be visible initally, only after interacting with y_slider

    x_slider.body.visible = False
    x_slider.slide.visible = False
    x_slider.label.visible = False

    y_slider = slider3d(animation_scene, vector(-2,-.7,0), vector(-2,.7,0), -3, 3, 'y gradient')

    #--------------------Set up control panel------------------#

    control_panel.select()

    #create play/pause
    button(control_panel, vector(-3,0,0), 'Play', '⏯', start_button_clicked)

    #create button to control gradient state, now no longer in use, preserve in case of future necesity
    #button(control_panel, vector(-2,0,0), 'Activate gradient', '⏯', gradient_button)

    button(control_panel, vector(-2,0,0), 'Picture', '📷', take_picture)

    #create spinner reset
    button(control_panel, vector(3,0,0), 'Reset Pointers', '⟳', reset_button_clicked_pointers)

    #create slider reset
    button(control_panel, vector(2,0,0), 'Reset Gradient', '⟳', reset_button_clicked_sliders)


    #running program

    while True:

        rate(60)

        #tracks the mouse's position in the control pannel -jc
        mouse_location_anim = animation_scene.mouse.pos
        mouse_location_ctrl = control_panel.mouse.pos

        if Animation_playing:
            rotate_all()

        for s in slider_list:

            if slider_list[0].dragging: #reset y if x moving
                slider_list[1].slide.pos = (slider_list[1].start_pos + .5 * slider_list[1].axis +vector(0, 0, .04))
                slider_list[1].update_value()

            if slider_list[1].dragging: #reset x if y moving
                slider_list[0].slide.pos = (slider_list[0].start_pos + .5 * slider_list[0].axis +vector(0, 0, .04))
                slider_list[0].update_value()


            if s.dragging:

                s.move()
            s.update_value()
        
        for l in label_list:
            l.update()

#----------------------------Start the sim----------------------------#

Run()