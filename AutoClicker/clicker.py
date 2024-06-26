from tkinter import *
import time
import threading
from pynput import mouse, keyboard

# button = mouse.Button.right
#Default Input
#button_to_click = 'e'
#Default Trigger Input Key
start_stop_key = keyboard.KeyCode(char='a')

#Center Window on screen
def center_window(window):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position coordinates
    x = (screen_width // 2) - (window.winfo_reqwidth() // 2)
    y = (screen_height // 2) - (window.winfo_reqheight() // 2)

    # Set the position of the window
    window.geometry(f'+{x}+{y}')

#Create Window
window = Tk()
window.title("Clicker")
center_window(window)
frame = Frame(window, width = 250)
frame.pack()

#Create Input Trigger Input
label = Label(window, text="Trigger: ")
label.pack(side=LEFT, padx=(5, 0), pady=0)
label.pack()

input_trigger = Button(window, text=str(ord(start_stop_key.char)) + " | " + start_stop_key.char)
input_trigger.pack(side=LEFT, padx=(0, 15), pady=0)
input_trigger.config(command=lambda: (window.bind("<KeyPress>" , on_single_key), input_trigger.config(text=" ")))
input_trigger.pack()

#Create Click-Rate Input
label = Label(window, text="Clicks/s: ")
label.pack(side=LEFT, padx=0, pady=0)
label.pack()

click_rate = Text(window, height = 1, width = 3)
click_rate.pack(side=LEFT, padx=(0, 15), pady=0)
click_rate.insert("1.0", "1")
click_rate.pack()

#Button To Click Input
label = Label(window, text="Key to Click: ")
label.pack(side=LEFT, padx=0, pady=0)
label.pack()

button_to_click = Text(window, height = 1, width = 3)
button_to_click.pack(side=LEFT, padx=(0, 15), pady=0)
button_to_click.insert("1.0", "e")
button_to_click.pack()

#Define Trigger Button DOESN'T WORK FOR MOUSE BUTTONS YET
def on_single_key(e):
    global start_stop_key

    window.unbind("<KeyPress>")
    start_stop_key = keyboard.KeyCode(char=chr(e.keycode).lower())
    input_trigger.config(text=str(ord(start_stop_key.char)) + " | " + start_stop_key.char)

#Create Duration Time
label = Label(window, text="Duration in Seconds: ")
label.pack(side=LEFT, padx=0, pady=0)
label.pack()

duration_time = Text(window, height = 1, width = 3)
duration_time.pack(side=LEFT, padx=(0, 15), pady=0)
duration_time.insert("1.0", "0")
duration_time.pack()

#Create Duration Clicks
label = Label(window, text="Duraction in Clicks: ")
label.pack(side=LEFT, padx=0, pady=0)
label.pack()

duration_clicks = Text(window, height = 1, width = 3)
duration_clicks.pack(side=LEFT, padx=(0, 15), pady=0)
duration_clicks.insert("1.0", "0")
duration_clicks.pack()

#Create Toggle/Hold Checkbox
label = Label(window, text="Toggle/Hold: ")
label.pack(side=LEFT, padx=0, pady=0)
label.pack()

toggle_checkbox = BooleanVar(value=True)
toggle_box = Checkbutton(window, variable=toggle_checkbox)
toggle_box.pack(side=LEFT, padx=0, pady=0)
toggle_box.pack()

#Thread to control clicks
class ClickButton(threading.Thread):
    def __init__(self):
        super(ClickButton, self).__init__()
        self.running = False
        self.program_running = True
    
    def duration(self):
        time.sleep(float(duration_time.get("1.0", END).strip()))
        click_thread.running = False

    #Loops every .1 second to check whether to run. Better option?
    def run(self):
        while self.program_running:
            while self.running:
                #mouse.click(self.button.left)
                controller.press(self.button_to_click)
                time.sleep(1/self.click_rate)
            time.sleep(0.1)

    #Stop when window closed
    def stop(self):
        self.program_running = False

# instance of mouse and keyboard controller created
mouse = mouse.Controller()
controller = keyboard.Controller()

#Create Thread
click_thread = ClickButton()
click_thread.start()

#Checks if pressed key is input trigger key to start/stop
def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.running = False
        else:
            #apply settings before starting
            click_thread.button_to_click = (button_to_click.get("1.0", END).strip())
            click_thread.click_rate = float(click_rate.get("1.0", END).strip())
            click_thread.running = True
            #Duration if greater than 0
            if float(duration_time.get("1.0", END).strip()) > 0:
                click_thread.duration()

# Create a listener instance
listener = keyboard.Listener(on_press=on_press)

# Start the listener in a separate thread
listener_thread = threading.Thread(target=listener.start)
listener_thread.start()

#Stop separate thread on window close
def on_close():
    click_thread.stop()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()
