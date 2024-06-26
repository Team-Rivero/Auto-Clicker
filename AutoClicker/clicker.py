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

#Define Trigger Button DOESN'T WORK FOR MOUSE BUTTONS YET
def on_single_key(e):
    global start_stop_key

    window.unbind("<KeyPress>")
    start_stop_key = keyboard.KeyCode(char=chr(e.keycode).lower())
    input_trigger.config(text=str(ord(start_stop_key.char)) + " | " + start_stop_key.char)

#Create Window
window = Tk()
window.title("Clicker")
window.wm_attributes("-topmost", 1)
center_window(window)

frame = Frame(window, width=250)
frame.pack()

#Create Input Trigger Input
label_trigger = Label(frame, text="Trigger: ")
label_trigger.pack(side=LEFT, padx=0, pady=0)

input_trigger = Button(frame, text=str(ord(start_stop_key.char)) + " | " + start_stop_key.char)
input_trigger.pack(side=LEFT, padx=(0, 15), pady=0)
input_trigger.config(command=lambda: (window.bind("<KeyPress>", on_single_key), input_trigger.config(text=" ")))

#Button To Click Input
label_click = Label(frame, text="Key to Click: ")
label_click.pack(side=LEFT, padx=0, pady=0)

button_to_click = Text(frame, height = 1, width = 3)
button_to_click.pack(side=LEFT, padx=(0, 15), pady=0)
button_to_click.insert("1.0", "e")

#Create Click-Rate Input
label_rate = Label(frame, text="Clicks/s: ")
label_rate.pack(side=LEFT, padx=0, pady=0)

click_rate = Text(frame, height = 1, width = 3)
click_rate.pack(side=LEFT, padx=(0, 15), pady=0)
click_rate.insert("1.0", "1")

#Create Duration Time
label_duration = Label(frame, text="Duration in Seconds: ")
label_duration.pack(side=LEFT, padx=0, pady=0)

duration_time = Text(frame, height = 1, width = 3)
duration_time.pack(side=LEFT, padx=(0, 15), pady=0)
duration_time.insert("1.0", "0")

#Create Duration Clicks
label_duration_clicks = Label(frame, text="Duraction in Clicks: ")
label_duration_clicks.pack(side=LEFT, padx=0, pady=0)

duration_clicks = Text(frame, height = 1, width = 3)
duration_clicks.pack(side=LEFT, padx=(0, 15), pady=0)
duration_clicks.insert("1.0", "0")

#Create Toggle/Hold Checkbox
label_toggle = Label(frame, text="Toggle/Hold: ")
label_toggle.pack(side=LEFT, padx=0, pady=0)

toggle_checkbox = BooleanVar(value=True)
toggle_box = Checkbutton(frame, variable=toggle_checkbox)
toggle_box.pack(side=LEFT, padx=0, pady=0)

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
            # Duration handling
            duration_sec = float(duration_time.get("1.0", END).strip())
            if duration_sec > 0:
                # Schedule a stop after duration_sec seconds
                threading.Timer(duration_sec, lambda: setattr(click_thread, 'running', False)).start()

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
