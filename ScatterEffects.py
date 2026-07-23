
None selected 

Skip to content
Using Lewis & Clark College Mail with screen readers
3 of 2,745
Scattering code that needs work is attached
Inbox
Bethe Scalettar
	
Attachments8:36 AM (5 hours ago)
	
	
to James, Pratyush, Bethe

 One attachment
  •  Scanned by Gmail

from vpython import *

#Set up first canvas (scene). Everything will go here by default unit next canvas set up.
scene=canvas(width =1024, height=480, center = vector(0,0,0), background=color.white, userspin=False, userzoom=False, resizable=True)
scene.lights=[]
distant_light(direction=vector( 0.22, 0.44, 0.88), color=color.white)
distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.white)

# Variables
animation_speed = 100
text_size = 15
is_scanning = False
propagating = False
running = False
drag=False
scatter_ratio = 0.2
scatter_positions=[]
for i in range(9):
    scatter_positions.append(vector(scene.width*((84+42*i)/1024),scene.height*(-140/480),0))
scatter_positions.append(vector(scene.width*(390/1024),scene.height*(85/480),0))
scatter_positions.append(vector(scene.width*(80/1024),scene.height*(90/480),0))
scatter_positions.append(vector(scene.width*(175/1024),scene.height*(100/480),0))
scatter_positions.append(vector(scene.width*(250/1024),scene.height*(-140/480),0))
scatter_positions.append(vector(scene.width*(427/1024),scene.height*(-140/480),0))


# <83.7006, -139.623, 0>
# <126.652, -142.927, 0>
# <168.502, -142.927, 0>
# <215.859, -142.927, 0>
# <258.811, -140.725, 0>
# <303.965, -144.029, 0>
# <345.815, -139.623, 0>
# <389.868, -139.623, 0>
# <390.97, 85.0466, 0>
# <79.2953, 89.4519, 0>
# <172.908, 99.3638, 0>
# <250, -142.927, 0>
# <427.313, -141.826, 0>
# Objects
background_media_box = box(pos=vector(0,0,0), height=scene.height, length=scene.width, width=1, opacity=1, shininess=0, texture='https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/2D_X-Ray_Projection_(NO_grid_NO_image).jpg')
xray_source_pos=vector(scene.width*(235.683/1024), scene.height*(166.545/480), 0) #<235.683, 166.545, 0><-2.20265, -189.183, 0><476.873, -189.183, 0>
detector_pos=vector(xray_source_pos.x,scene.height*(-190/480),0)

#Create Title
title = label(pos=vector(0,scene.height/2,0), text='Scattering Effects', font='helvetica', height=1.5*text_size, box=False, visible=True, color=color.black, opacity=0)
lbl_start=label(pos=vector(0,-scene.height/2+text_size/2,0), text="Start with Activities (link at top)!", font="helvetica", box=True, canvas=scene, color=color.black, height=text_size, visible=True, opacity=0)



ray_list=[]
ray_direction=[]
ray_destination=[]
w=-8
for i in range(0,2*abs(w)+1,1):
    ray_list.append(arrow(pos = xray_source_pos, axis = vector(0,0,0), shaftwidth=1, headwidth=3, headlength=10, make_trail=True, color=color.red, visible = False, has_scattered=False))
    ray_direction.append(hat(detector_pos + w*vector(scene.width*(25/1024),0,0) - xray_source_pos))
    ray_destination.append(detector_pos + w*vector(scene.width*(25/1024),0,0))
    w += 1

# Functions

# def click():
#     loc_b=scene.mouse.pos
#     control_panel.append_to_caption(str(loc_b)+'\n')

# scene.bind('mousedown', click)

def scale_rays(rays, in_directions, in_destinations, in_scatters):
    global running, propagating
    control_panel.unbind("mousedown", no_scatter)
    control_panel.unbind("mousedown", with_scatter)
    control_panel.unbind("mousedown", scatter_grid)
    control_panel.unbind("mousedown", Run)
    directions = in_directions[:]
    destinations = in_destinations[:]
    scatters = in_scatters[:]
    scatter_indexes = []
    index_choices = list(range(len(rays)))
    if button_box_dict['With Scatter'].color == color.green:
        for k in range(round(scatter_ratio*len(rays))):
            random_index_choice=floor(min(random()*len(index_choices), abs(len(scatters)-0.0000001)))
            # while random_index_choice in scatter_indexes and:
            #     random_index_choice=floor(min(random()*len(index_choices), abs(len(scatters)-0.0000001)))
            scatter_indexes.append(index_choices[random_index_choice])
            index_choices.pop(random_index_choice)
        # print(str(scatter_indexes))
    for i in rays:
        i.has_scattered = False
    for i in range(len(rays)):
        rays[i].pos = xray_source_pos
        rays[i].axis = directions[i]
        rays[i].visible = True
    while any([sqrt((rays[k].pos.x-destinations[k].x)**2+(rays[k].pos.y-destinations[k].y)**2) >= 2 for k in range(len(rays))]):
        rate(animation_speed)
        for i in range(len(rays)):
            if sqrt((rays[i].pos.x-destinations[i].x)**2+(rays[i].pos.y-destinations[i].y)**2) >= 2:
                rays[i].pos += 2*directions[i]
            # print('With Scatter On: ' + str(button_box_dict['With Scatter'].color == color.green))
            # print('Ray at Height: ' + str(rays[i].pos.y))
            # print('Has Scattered: ' + str(rays[i].has_scattered))
            # print('In Index: ' + str(i in scatter_indexes))
            number_scattered = 0
            if button_box_dict['With Scatter'].color == color.green and rays[i].pos.y <= scene.height*(-50/480) and not rays[i].has_scattered and i in scatter_indexes:
                while in_directions[i] == directions[i]:
                    random_destination_choice=floor(min(random()*len(scatters), abs(len(scatters)-0.0000001)))
                    destinations[i]=scatters[random_destination_choice]
                    directions[i]=hat(destinations[i]-rays[i].pos)
                rays[i].axis = directions[i]
                if button_box_dict['Scatter Grid'].color == vector(0.7,0.7,0.7) and destinations[i].y < 0:
                    destinations[i] = rays[i].pos + abs((rays[i].pos.y-detector_pos.y)/directions[i].y)*directions[i]
                if len(scatters) > 1:
                    scatters.pop(random_destination_choice)
                rays[i].has_scattered = True
    if button_box_dict['No Scatter'].color == color.green:
        background_media_box.texture = 'https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/2D_X-Ray_Projection_(NO_grid_SHARP_image).jpg'
    elif button_box_dict['With Scatter'].color == color.green and button_box_dict['Scatter Grid'].color == color.green:
        background_media_box.texture = 'https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/2D_X-Ray_Projection_(YES_grid_YES_image).jpg'
    else:
        #the correct extension for 20% is: 2D_X-Ray_Projection_(NO_grid_YES_image)_20.jpg
        #print(str(round((scatter_ratio * 100))))
        shouldBePercentLink = 'https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/2D_X-Ray_Projection_(NO_grid_YES_image)_' + str(round((scatter_ratio * 100))) + '.jpg'
        #print(shouldBePercentLink)
        background_media_box.texture = shouldBePercentLink
    sleep(2*(100/animation_speed))
    for i in rays:
        i.clear_trail()
        i.visible=False
    running = False
    propagating = False
    button_box_dict['Send X-Rays'].color=vector(0.7,0.7,0.7)
    control_panel.bind("mousedown", no_scatter)
    control_panel.bind("mousedown", with_scatter)
    control_panel.bind("mousedown", scatter_grid)
    control_panel.bind("mousedown", Run)

# Hyperlinks - figure this out better from Bruce Sherwood email on 1/12/2024
s = '''<font size=4> <font>'''
l= '''<font size=4> <font>'''
q = '''<font size=4> <font>'''
v = '''<font size=4> <font>'''
def link1(url, d):
    global s
    s += "<a href='https://webdev2.watzek.cloud/~nddill/scanningSims/images/Activities/Activities_A-mode-Level2.png" + "' target='_blank'>" + url + "</a>"
    s += d
def link2(url, d):
    global l
    l += "<a href='https://webdev2.watzek.cloud/~nddill/scanningSims/images/Activities/Activities_A-mode-Level1.png" + "' target='_blank'>" + url + "</a>"
    l += d
def link3(url, d):
    global q
    q += "<a href='https://webdev2.watzek.cloud/~nddill/scanningSims/images/Background/Background_US_onepage.png" + "' target='_blank'>" + url + "</a>"
    q += d
def link4(url, d):
    global v
    v += "<a href='https://webdev2.watzek.cloud/~nddill/scanningSims/images/Information/Information-A-mode.png" + "' target='_blank'>" + url + "</a>"
    v += d
 
link1("Activities: Level 2", "&nbsp &nbsp &nbsp")
scene.append_to_title(s)
link2("Activities: Level 1", "&nbsp &nbsp &nbsp")
scene.append_to_title(l)
link3("Background", "&nbsp &nbsp &nbsp")
scene.append_to_title(q)
link4("Information", "&nbsp &nbsp &nbsp")
scene.append_to_title(v)

# Set up Control Panel
control_panel=canvas(width=1024, height=100, center = vector(0,0,0), background=vec(0.622, 0.779, 0.847), userspin=False, userzoom=False, resizable=False)
title_cp=label(pos=vector(0,(control_panel.height/2)-text_size,0), text='Control Panel', font='helvetica', height=control_panel.height*(20/100), box=False, visible=True, color=color.black, opacity=0)

# Create Buttons
button_box_dict = {}
button_icon_list = []
button_text_list = []
button_size = 50

def create_buttons(chosen_canvas, text_list, icon_list):
    side_buffer = chosen_canvas.width/100
    step = (chosen_canvas.width-2*side_buffer)/(len(text_list)-1)
    for i in range(len(text_list)):
        button_box_dict.setdefault(text_list[i], box(pos=vector((-chosen_canvas.width/2)+side_buffer+(i*step), -text_size/2, 0), length=control_panel.width*(button_size/1024), height=control_panel.height*(button_size/100), width=0.01, color=vec(0.7,0.7,0.7), shininess=0, opacity=0.3))
        button_icon_list.append(label(pos=button_box_dict[text_list[i]].pos, text=icon_list[i], height=button_box_dict[text_list[i]].height/1.7, color=color.black, box=False, opacity=0))
        button_text_list.append(label(pos=button_box_dict[text_list[i]].pos-vector(0,button_box_dict[text_list[i]].height/2+text_size,0), text=text_list[i], height=text_size, color=color.black, box=False, opacity=0))

create_buttons(control_panel, ['Send X-Rays', 'No Scatter', 'With Scatter', 'Scatter Grid'], ['⏯','🚫','⬇️','☷'])

# Button Functionality
def Run():
    global propagating, running
    loc_b=control_panel.mouse.pos
    if abs(loc_b.x-button_box_dict['Send X-Rays'].pos.x)<=button_box_dict['Send X-Rays'].length/2 and abs(loc_b.y-button_box_dict['Send X-Rays'].pos.y)<=button_box_dict['Send X-Rays'].height/2: 
        scene.autoscale=False
        running = not running
        if running:
            propagating = True
            button_box_dict['Send X-Rays'].color = color.green
            scale_rays(ray_list, ray_direction, ray_destination, scatter_positions)
        else: 
            propagating = False
            button_box_dict['Send X-Rays'].color = vector(0.7,0.7,0.7)
control_panel.bind("mousedown", Run)

def no_scatter():
    global running, propagating, ray_list
    loc_b=control_panel.mouse.pos
    if abs(loc_b.x-button_box_dict['No Scatter'].pos.x)<=button_box_dict['Send X-Rays'].length/2 and abs(loc_b.y-button_box_dict['No Scatter'].pos.y)<=button_box_dict['Send X-Rays'].height/2 and button_box_dict['No Scatter'].color != color.green:
        button_box_dict['No Scatter'].color = color.green
        button_box_dict['With Scatter'].color = vector(0.7,0.7,0.7)
        button_box_dict['Scatter Grid'].color = vector(0.7,0.7,0.7)
        background_media_box.texture = 'https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/2D_X-Ray_Projection_(NO_grid_NO_image).jpg'
        for i in ray_list:
            i.clear_trail()
            i.visible=False
        running = False
        propagating = False
        button_box_dict['Send X-Rays'].color=vector(0.7,0.7,0.7)

control_panel.bind("mousedown", no_scatter)

def with_scatter():
    global running, propagating, ray_list
    loc_b=control_panel.mouse.pos
    if abs(loc_b.x-button_box_dict['With Scatter'].pos.x)<=button_box_dict['Send X-Rays'].length/2 and abs(loc_b.y-button_box_dict['With Scatter'].pos.y)<=button_box_dict['Send X-Rays'].height/2 and button_box_dict['With Scatter'].color != color.green:
        button_box_dict['No Scatter'].color = vector(0.7,0.7,0.7)
        button_box_dict['With Scatter'].color = color.green
        background_media_box.texture = 'https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/2D_X-Ray_Projection_(NO_grid_NO_image).jpg'
        for i in ray_list:
            i.clear_trail()
            i.visible=False
        running = False
        propagating = False
        button_box_dict['Send X-Rays'].color=vector(0.7,0.7,0.7)

control_panel.bind("mousedown", with_scatter)

def scatter_grid():
    global running, propagating, ray_list
    loc_b=control_panel.mouse.pos
    if abs(loc_b.x-button_box_dict['Scatter Grid'].pos.x)<=button_box_dict['Send X-Rays'].length/2 and abs(loc_b.y-button_box_dict['Scatter Grid'].pos.y)<=button_box_dict['Send X-Rays'].height/2:
        if button_box_dict['Scatter Grid'].color == vector(0.7,0.7,0.7) and button_box_dict['With Scatter'].color == color.green:
            button_box_dict['Scatter Grid'].color = color.green
            background_media_box.texture = 'https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/2D_X-Ray_Projection_(YES_grid_NO_image).jpg'
        else:
            button_box_dict['Scatter Grid'].color = vector(0.7,0.7,0.7)
            background_media_box.texture = 'https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/2D_X-Ray_Projection_(NO_grid_NO_image).jpg'
        for i in ray_list:
            i.clear_trail()
            i.visible=False
        running = False
        propagating = False
        button_box_dict['Send X-Rays'].color=vector(0.7,0.7,0.7)
        
control_panel.bind("mousedown", scatter_grid)



def adjust_scatter_ratio(s):
    global scatter_ratio
    if isinstance(s, float):
        scatter_ratio = s
        scatter_ratio_slider.value = scatter_ratio
    else:
        scatter_ratio = s.value
    scatter_ratio_caption.text ='<font size=4>' +  str(round(scatter_ratio*100)) + "% Scattering\n"
scatter_ratio_slider = slider(bind=adjust_scatter_ratio, min=0, max=1, step=0.2, value=scatter_ratio, length=250, width=15)
scatter_ratio_caption = wtext(text='<font size=4>' + str(round(scatter_ratio*100)) + "% Scattering\n")

button_box_dict['No Scatter'].color = color.green

# Running Code
while True:
    x=0

VS_ScatterEffects.py
Displaying VS_ScatterEffects.py.