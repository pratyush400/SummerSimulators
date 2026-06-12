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