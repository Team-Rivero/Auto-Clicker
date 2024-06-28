from tkinter import *
import time
import threading
from pynput import mouse, keyboard

#Global Variables
start_stop_key = None
clicker_key = None
setting_trigger = False
setting_clicker = False
total_clicks = 0

#Instance of mouse and keyboard controller created
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

#Center Window on screen
def center_window(window):
    #Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    #Calculate position coordinates
    x = (screen_width // 2) - (window.winfo_reqwidth() // 2)
    y = (screen_height // 2) - (window.winfo_reqheight() // 2)

    #Set the position of the window
    window.geometry(f'+{x}+{y}')

#Set trigger key
def set_trigger_key():
    global setting_trigger
    setting_trigger = True
    input_trigger.config(text="Press Key...")

#Set auto clicker key
def set_input_clicker():
    global setting_clicker
    setting_clicker = True
    input_clicker.config(text="Press Key...")

#region Created Windows
#Main Window
window = Tk()
window.title("Clicker")
window.wm_attributes("-topmost", 1)
center_window(window)

frame = Frame(window, width=250)
frame.pack()

#Create Trigger Input
label_trigger = Label(frame, text="Trigger: ")
label_trigger.grid(row=0, column=0, padx=(5, 0), pady=(5, 0))

input_trigger = Button(frame, text="Set Trigger Key")
input_trigger.grid(row=0, column=1, padx=(0, 15), pady=(5, 0))
input_trigger.config(command=lambda: (set_trigger_key()))

#Create Click Input
label_clicker = Label(frame, text="Clicker: ")
label_clicker.grid(row=2, column=0, padx=(5, 0), pady=(5, 0))

input_clicker = Button(frame, text="Set Clicker Key")
input_clicker.grid(row=2, column=1, padx=(0, 15), pady=(5, 0))
input_clicker.config(command=lambda: (set_input_clicker()))

#Create Click-Rate Input
label_rate = Label(frame, text="Clicks/s: ")
label_rate.grid(row=0, column=2, padx=(5, 0), pady=(5, 0))

click_rate = Text(frame, height=1, width=3)
click_rate.grid(row=0, column=3, padx=(0, 15), pady=(5, 0))
click_rate.insert("1.0", "100")

#Create Duration Time
label_duration_time = Label(frame, text="Duration in Seconds: ")
label_duration_time.grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

duration_time = Text(frame, height=1, width=3)
duration_time.grid(row=1, column=3, padx=(0, 15), pady=(5, 0))
duration_time.insert("1.0", "0")

#Create Duration Clicks
label_duration_clicks = Label(frame, text="Duration in Clicks: ")
label_duration_clicks.grid(row=2, column=2, padx=(5, 0), pady=(5, 0))

duration_clicks = Text(frame, height=1, width=3)
duration_clicks.grid(row=2, column=3, padx=(0, 15), pady=(5, 0))
duration_clicks.insert("1.0", "0")

#Create Toggle/Hold Checkbox
label_toggle = Label(frame, text="Toggle/Hold: ")
label_toggle.grid(row=0, column=4, padx=(5, 0), pady=(5, 0))

toggle_checkbox = BooleanVar(value=True)
toggle_box = Checkbutton(frame, variable=toggle_checkbox)
toggle_box.grid(row=0, column=5, padx=(0, 15), pady=(5, 0))
#endregion

#Thread to control clicks
class ClickButton(threading.Thread):
    def __init__(self):
        super(ClickButton, self).__init__()
        self.running = False
        self.program_running = True

    #Loops every .1 second to check whether to run. Better option?
    def run(self):
        while self.program_running:
            while self.running:
                #mouse_controller.click(self.button.left)
                keyboard_controller.press(self.clicker_key)
                time.sleep(1/self.click_rate)
            time.sleep(0.1)

    #Stop when window closed
    def stop(self):
        self.program_running = False

#Create Thread
click_thread = ClickButton()
click_thread.start()

#Stop Thread Function
def stop_thread():
    global total_clicks
    total_clicks = 0
    click_thread.running = False

#Set Trigger
def set_trigger(button):
    global start_stop_key, setting_trigger
    if setting_trigger:
        try:
            start_stop_key = button
            input_trigger.config(text=str(button))
            setting_trigger = False
        except AttributeError:
            pass

#Set Clicker
def set_clicker(button):
    global start_stop_key, setting_clicker, clicker_key
    if setting_clicker:
        try:
            clicker_key = button
            input_clicker.config(text=str(button))
            setting_clicker = False
        except AttributeError:
            pass

#Checks if pressed key is input trigger key to start/stop
def on_press(key):
    global start_stop_key, clicker_key, setting_trigger, setting_clicker, total_clicks

    #Start/Stop auto clicker thread
    if not setting_trigger and clicker_key and start_stop_key is not None:
        if key == start_stop_key:
            if click_thread.running:
                stop_thread()
            else:
                #Apply settings before starting
                click_thread.clicker_key = clicker_key
                click_thread.click_rate = float(click_rate.get("1.0", END).strip())
                click_thread.running = True
                #Duration handling
                seconds = float(duration_time.get("1.0", END).strip())
                if seconds > 0:
                    #Schedule a stop after seconds
                    threading.Timer(seconds, stop_thread).start()

        #Duration Clicks
        clicks = float(duration_clicks.get("1.0", END).strip())
        
        #Schedule a stop after clicks
        if clicks > 0:
            if key == clicker_key:
                total_clicks += 1
                if total_clicks >= clicks:
                    stop_thread()
                    
    #Set Trigger
    set_trigger(key)

    #Set Clicker
    set_clicker(key)

#Checks if pressed key is input trigger key to start/stop
def on_click(x, y, button, pressed):
    global start_stop_key, clicker_key, setting_trigger, setting_clicker, total_clicks
    
    #Set Trigger
    set_trigger(button)

    #Set Clicker
    set_clicker(button)

#Listener for keyboard presses
start_stop_listener = keyboard.Listener(on_press=on_press)
listener_thread = threading.Thread(target=start_stop_listener.start)
listener_thread.start()

#Listener for Mouse presses
start_stop_listener_mouse = mouse.Listener(on_click=on_click)
listener_thread_mouse = threading.Thread(target=start_stop_listener_mouse.start)
listener_thread_mouse.start()

#Stop separate thread on window close
def on_close():
    click_thread.stop()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()
