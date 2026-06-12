Web VPython 3.2
from vpython import *
#Web VPython 3.2

from vpython import *
from random import choice


scene=canvas(width =1024, height=480, center=vector(0,0,0), background=color.white, resizable=False, userzoom=False, userspin=False)
scene.lights=[]
distant_light(direction=vector( 0.22, 0.44, 0.88), color=color.white)
distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.white)
#Moved down 100 affects below
browser_window = window
my_bookImage = box(pos=vector(0,-100,0), length=scene.width, height=scene.height, texture="https://i.imgur.com/ipbI9jA.jpeg", shininess=0, visible = False, color=color.white)

#Text to speech

YOUR_DOCUMENT_TEXT = """
Paste your text here. 
It can span multiple lines and paragraphs.
For example: Hello! This text is stored directly inside the code.
The browser will read it perfectly without needing any external file.
"""

#Variables
atoms_loc = scene.width/2
animation_speed=1000
remember_speed = animation_speed
E = 20 #Energy in keVT
Z = 7.4 #Starting atomic number
theta = pi/15
text_size=15 
started = False #Set to true when simulation first starts (see Run())
started_atomic = False #Used if user hits switch to target view before simulation done and prints warning (see SwitchView() if and else lines)
propagating = False
running = False
is_atomic = False #Set to true when you switch to mechanistic view (see switchView)
has_run = False #Set to true after a full atomic/mechanistic run. Calls reset_atomic to reset visible stuff if don't change atomic mechanism. Check has_run.
remember_has_run=has_run
PE_dropElectronLoc = vector((-104/1025)*scene.width,(10/513)*scene.height,0)
PE_scatterElectronLoc = vector((-70/1025)*scene.width,(-31/513)*scene.height,0)
PE_MElectronLoc = vector(-130, 40, 0)   # M shell
PE_LElectronLoc = vector(-115, 25, 0)   # L shell
PE_MElectron = sphere(
    pos=PE_MElectronLoc,
    radius=8,
    color=color.orange,
    visible=False
)
# SETTING UP COMPTON ELECTRON RANDOMNESS 
# seeting comptom election positions
bottom_left = vector((-63/1025)*scene.width,(-153/513)*scene.height,0)
top_left = vector((-63/1470)*scene.width,(145/590)*scene.height,0)
bottom_right = vector((40/1000)*scene.width,(-160/500)*scene.height,0)
top_right = vector((45/1000)*scene.width,(140/590)*scene.height,0)

bl_url = "https://medicalimaging.watzekdi.net/images/Xray_images/Activity2-Interactions/electron_BL.png"
tl_url = "https://medicalimaging.watzekdi.net/images/Xray_images/Activity2-Interactions/electron_TL.png"
br_url = "https://medicalimaging.watzekdi.net/images/Xray_images/Activity2-Interactions/electron_BR.png"
tr_url = "https://medicalimaging.watzekdi.net/images/Xray_images/Activity2-Interactions/electron_TR.png"

COMPTON_ANIMATION = {1: [bottom_left, bl_url,-20, -0.2], 2: [top_left, tl_url, 40, 0.2], 3: [bottom_right, br_url,-20, -0.2], 4: [top_right, tr_url, 40, 0.2]}

animation_choice = choice(list(COMPTON_ANIMATION.keys()))
compton_electronLoc, url, x_corr, electron_y = COMPTON_ANIMATION[animation_choice]


pulse_list=[vector(0,34.625,0),vector(0.125,34.625,0),vector(0.25,34.5,0),vector(0.375,34.375,0),vector(0.5,34.25,0),vector(0.625,34.125,0),vector(0.75,34,0),vector(0.875,33.75,0),vector(1,33.625,0),vector(1.125,33.25,0),vector(1.25,33.125,0),vector(1.375,32.875,0),vector(1.5,32.75,0),vector(1.625,32.625,0),vector(1.75,32.5,0),vector(1.875,32.375,0),vector(2,32.375,0),vector(2.125,32.25,0),vector(2.25,32.375,0),vector(2.375,32.375,0),vector(2.5,32.5,0),vector(2.625,32.625,0),vector(2.75,32.75,0),vector(2.875,32.875,0),vector(3,33,0),vector(3.125,33.25,0),vector(3.25,33.625,0),vector(3.375,34,0),vector(3.5,34.375,0),vector(3.625,35,0),vector(3.75,35.5,0),vector(3.875,35.875,0),vector(4,36.375,0),vector(4.125,36.875,0),vector(4.25,37.125,0),vector(4.375,37.5,0),vector(4.5,37.875,0),vector(4.625,38.25,0),vector(4.75,38.5,0),vector(4.875,38.75,0),vector(5,38.875,0),vector(5.125,39,0),vector(5.25,39.125,0),vector(5.375,39.25,0),vector(5.5,39.375,0),vector(5.625,39.375,0),vector(5.75,39.5,0),vector(5.875,39.5,0),vector(6,39.5,0),vector(6.125,39.5,0),vector(6.25,39.375,0),vector(6.375,39.375,0),vector(6.5,39.25,0),vector(6.625,39.125,0),vector(6.75,39,0),vector(6.875,38.875,0),vector(7,38.75,0),vector(7.125,38.5,0),vector(7.25,38.125,0),vector(7.375,37.875,0),vector(7.5,37.625,0),vector(7.625,37.125,0),vector(7.75,36.625,0),vector(7.875,36.125,0),vector(8,35.625,0),vector(8.125,34.75,0),vector(8.25,34,0),vector(8.375,32.875,0),vector(8.5,31.75,0),vector(8.625,30.5,0),vector(8.75,29.25,0),vector(8.875,28.25,0),vector(9,27.375,0),vector(9.125,26.25,0),vector(9.25,25.375,0),vector(9.375,24.625,0),vector(9.5,23.875,0),vector(9.625,23.25,0),vector(9.75,22.625,0),vector(9.875,22.25,0),vector(10,21.875,0),vector(10.125,21.5,0),vector(10.25,21.375,0),vector(10.375,21.25,0),vector(10.5,21.25,0),vector(10.625,21.25,0),vector(10.75,21.25,0),vector(10.875,21.375,0),vector(11,21.625,0),vector(11.125,21.875,0),vector(11.25,22.5,0),vector(11.375,22.875,0),vector(11.5,23.375,0),vector(11.625,24.125,0),vector(11.75,24.875,0),vector(11.875,25.75,0),vector(12,26.5,0),vector(12.125,27.625,0),vector(12.25,28.75,0),vector(12.375,29.75,0),vector(12.5,30.75,0),vector(12.625,32.25,0),vector(12.75,33.75,0),vector(12.875,35,0),vector(13,36.25,0),vector(13.125,37.75,0),vector(13.25,39,0),vector(13.375,40,0),vector(13.5,41,0),vector(13.625,42.25,0),vector(13.75,43.25,0),vector(13.875,44,0),vector(14,44.75,0),vector(14.125,45.625,0),vector(14.25,46.25,0),vector(14.375,46.75,0),vector(14.5,47.125,0),vector(14.625,47.625,0),vector(14.75,47.875,0),vector(14.875,48,0),vector(15,48.125,0),vector(15.125,48.25,0),vector(15.25,48.125,0),vector(15.375,48,0),vector(15.5,47.875,0),vector(15.625,47.75,0),vector(15.75,47.375,0),vector(15.875,47,0),vector(16,46.625,0),vector(16.125,45.875,0),vector(16.25,45.25,0),vector(16.375,44.5,0),vector(16.5,43.75,0),vector(16.625,42.75,0),vector(16.75,41.75,0),vector(16.875,40.75,0),vector(17,39.625,0),vector(17.125,38,0),vector(17.25,35.875,0),vector(17.375,34.375,0),vector(17.5,32.625,0),vector(17.625,29.5,0),vector(17.75,26.625,0),vector(17.875,24.25,0),vector(18,21.75,0),vector(18.125,18.5,0),vector(18.25,15.875,0),vector(18.375,14,0),vector(18.5,12,0),vector(18.625,9.75,0),vector(18.75,8,0),vector(18.875,6.625,0),vector(19,5.375,0),vector(19.125,4,0),vector(19.25,2.875,0),vector(19.375,2.5,0),vector(19.5,2,0),vector(19.625,1.375,0),vector(19.75,1.25,0),vector(19.875,1.25,0),vector(20,1.625,0),vector(20.125,2.125,0),vector(20.25,2.75,0),vector(20.375,3.5,0),vector(20.5,4.375,0),vector(20.625,5.75,0),vector(20.75,7.375,0),vector(20.875,8.875,0),vector(21,10.375,0),vector(21.125,12.625,0),vector(21.25,15,0),vector(21.375,17.125,0),vector(21.5,19.5,0),vector(21.625,22.625,0),vector(21.75,25.875,0),vector(21.875,28.75,0),vector(22,32.125,0),vector(22.125,36.5,0),vector(22.25,40.5,0),vector(22.375,44.125,0),vector(22.5,48,0),vector(22.625,52.25,0),vector(22.75,56,0),vector(22.875,58.875,0),vector(23,61.75,0),vector(23.125,64.875,0),vector(23.25,67.5,0),vector(23.375,69.375,0),vector(23.5,71.375,0),vector(23.625,73.375,0),vector(23.75,75,0),vector(23.875,76.125,0),vector(24,76.875,0),vector(24.125,77.75,0),vector(24.25,78.125,0),vector(24.375,78.25,0),vector(24.5,78.125,0),vector(24.625,77.75,0),vector(24.75,76.875,0),vector(24.875,76.125,0),vector(25,75,0),vector(25.125,73.375,0),vector(25.25,71.375,0),vector(25.375,69.375,0),vector(25.5,67.5,0),vector(25.625,64.875,0),vector(25.75,61.75,0),vector(25.875,58.875,0),vector(26,56,0),vector(26.125,52.25,0),vector(26.25,48,0),vector(26.375,44.125,0),vector(26.5,40.5,0),vector(26.625,36.5,0),vector(26.75,32.125,0),vector(26.875,28.75,0),vector(27,25.875,0),vector(27.125,22.625,0),vector(27.25,19.5,0),vector(27.375,17.125,0),vector(27.5,15,0),vector(27.625,12.625,0),vector(27.75,10.375,0),vector(27.875,8.875,0),vector(28,7.375,0),vector(28.125,5.75,0),vector(28.25,4.375,0),vector(28.375,3.5,0),vector(28.5,2.75,0),vector(28.625,2.125,0),vector(28.75,1.625,0),vector(28.875,1.25,0),vector(29,1.25,0),vector(29.125,1.375,0),vector(29.25,2,0),vector(29.375,2.5,0),vector(29.5,2.875,0),vector(29.625,4,0),vector(29.75,5.375,0),vector(29.875,6.625,0),vector(30,8,0),vector(30.125,9.75,0),vector(30.25,12,0),vector(30.375,14,0),vector(30.5,15.875,0),vector(30.625,18.5,0),vector(30.75,21.75,0),vector(30.875,24.25,0),vector(31,26.625,0),vector(31.125,29.5,0),vector(31.25,32.625,0),vector(31.375,34.375,0),vector(31.5,35.875,0),vector(31.625,38,0),vector(31.75,39.625,0),vector(31.875,40.75,0),vector(32,41.75,0),vector(32.125,42.75,0),vector(32.25,43.75,0),vector(32.375,44.5,0),vector(32.5,45.25,0),vector(32.625,45.875,0),vector(32.75,46.625,0),vector(32.875,47,0),vector(33,47.375,0),vector(33.125,47.75,0),vector(33.25,47.875,0),vector(33.375,48,0),vector(33.5,48.125,0),vector(33.625,48.25,0),vector(33.75,48.125,0),vector(33.875,48,0),vector(34,47.875,0),vector(34.125,47.625,0),vector(34.25,47.125,0),vector(34.375,46.75,0),vector(34.5,46.25,0),vector(34.625,45.625,0),vector(34.75,44.75,0),vector(34.875,44,0),vector(35,43.25,0),vector(35.125,42.25,0),vector(35.25,41,0),vector(35.375,40,0),vector(35.5,39,0),vector(35.625,37.75,0),vector(35.75,36.25,0),vector(35.875,35,0),vector(36,33.75,0),vector(36.125,32.25,0),vector(36.25,30.75,0),vector(36.375,29.75,0),vector(36.5,28.75,0),vector(36.625,27.625,0),vector(36.75,26.5,0),vector(36.875,25.75,0),vector(37,24.875,0),vector(37.125,24.125,0),vector(37.25,23.375,0),vector(37.375,22.875,0),vector(37.5,22.5,0),vector(37.625,21.875,0),vector(37.75,21.625,0),vector(37.875,21.375,0),vector(38,21.25,0),vector(38.125,21.25,0),vector(38.25,21.25,0),vector(38.375,21.25,0),vector(38.5,21.375,0),vector(38.625,21.5,0),vector(38.75,21.875,0),vector(38.875,22.25,0),vector(39,22.625,0),vector(39.125,23.25,0),vector(39.25,23.875,0),vector(39.375,24.625,0),vector(39.5,25.375,0),vector(39.625,26.25,0),vector(39.75,27.375,0),vector(39.875,28.25,0),vector(40,29.25,0),vector(40.125,30.5,0),vector(40.25,31.75,0),vector(40.375,32.875,0),vector(40.5,34,0),vector(40.625,34.75,0),vector(40.75,35.625,0),vector(40.875,36.125,0),vector(41,36.625,0),vector(41.125,37.125,0),vector(41.25,37.625,0),vector(41.375,37.875,0),vector(41.5,38.125,0),vector(41.625,38.5,0),vector(41.75,38.75,0),vector(41.875,38.875,0),vector(42,39,0),vector(42.125,39.125,0),vector(42.25,39.25,0),vector(42.375,39.375,0),vector(42.5,39.375,0),vector(42.625,39.5,0),vector(42.75,39.5,0),vector(42.875,39.5,0),vector(43,39.5,0),vector(43.125,39.375,0),vector(43.25,39.375,0),vector(43.375,39.25,0),vector(43.5,39.125,0),vector(43.625,39,0),vector(43.75,38.875,0),vector(43.875,38.75,0),vector(44,38.5,0),vector(44.125,38.25,0),vector(44.25,37.875,0),vector(44.375,37.5,0),vector(44.5,37.125,0),vector(44.625,36.875,0),vector(44.75,36.375,0),vector(44.875,35.875,0),vector(45,35.5,0),vector(45.125,35,0),vector(45.25,34.375,0),vector(45.375,34,0),vector(45.5,33.625,0),vector(45.625,33.25,0),vector(45.75,33,0),vector(45.875,32.875,0),vector(46,32.75,0),vector(46.125,32.625,0),vector(46.25,32.5,0),vector(46.375,32.375,0),vector(46.5,32.375,0),vector(46.625,32.25,0),vector(46.75,32.375,0),vector(46.875,32.375,0),vector(47,32.5,0),vector(47.125,32.625,0),vector(47.25,32.75,0),vector(47.375,32.875,0),vector(47.5,33.125,0),vector(47.625,33.25,0),vector(47.75,33.625,0),vector(47.875,33.75,0),vector(48,34,0),vector(48.125,34.125,0),vector(48.25,34.25,0),vector(48.375,34.375,0),vector(48.5,34.5,0),vector(48.625,34.625,0),vector(48.75,34.625,0)]
#test_photon=curve(pos=pulse_list, color=vec(0,0.5,0), radius=1, canvas=scene, origin=vector(-110,-40,0))
message_list = []
num_PE=0
num_CS=0
N=0
num_trans=0
my_element_changed=False
remember_m_index=0

#Objects

# compton text 
lbl_compton=label(pos=vector(0, scene.height/2 - 70, 0),text="Compton Scattering", font="helvetica", box=False,canvas=scene, color=vec(0, 0, 0), height=text_size,visible=False, opacity=0)


# 2. Text-to-speech execution engine
def speak(text_message):
    js_code = f"""
    var msg = new SpeechSynthesisUtterance("{text_message}");
    window.speechSynthesis.speak(msg);
    """
    # Execute the raw JavaScript code string within the browser
    GS_EXEC(js_code)

# 3. Interactive button callback
def handle_button_click():
    speak(YOUR_DOCUMENT_TEXT)

# Hyperlinks 
s = '''<font size=4> <font>'''
l= '''<font size=4> <font>'''
q = '''<font size=4> <font>'''
v = '''<font size=4> <font>'''
def link1(url, d):
    global s
    s += "<a href='https://webdev2.watzek.cloud/~nddill/scanningSims/images/projection_Radiography/%20Information-Interactions.png" + "' target='_blank'>" + url + "</a>"
    s += d
def link2(url, d):
    global l
    l += "<a href='https://medicalimaging.watzekdi.net/images/Xray_images/Activity2-Interactions/Activities-interactions.png" + "' target='_blank'>" + url + "</a>"
    l += d
def link3(url, d):
    global q
    q += "<a href='https://medicalimaging.watzekdi.net/images/Xray_images/Activity2-Interactions/Background-interactions.png" + "' target='_blank'>" + url + "</a>"
    q += d
def link4(url, d):
    global v
    v += "<a href='https://medicalimaging.watzekdi.net/images/Xray_images/Activity2-Interactions/%20Information-Interactions.png" + "' target='_blank'>" + url + "</a>"
    v += d
    


link4("Information", "&nbsp &nbsp &nbsp")
scene.append_to_title(v)
link3("Background", "&nbsp &nbsp &nbsp")
scene.append_to_title(q)
link2("Activities", "&nbsp &nbsp &nbsp")
scene.append_to_title(l)
scene.append_to_title("<br><br>")

speech_button = button(bind=handle_button_click, text="Click to Speak")