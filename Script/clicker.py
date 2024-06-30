from tkinter import *
import time
import threading
from pynput import mouse, keyboard

#Global Variables
trigger_key = None
bIs_Mouse = None
setting_trigger = False
setting_clicker = False
total_clicks = 0
bPress_Once = True

clicker_buttons = []
clicker_keys = []
clicker_labels = []
clicker_next_row = 2
current_clicker = None

#Instance of mouse and keyboard controller created
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

#Validate entry inputs
def validate_number(input):
    # Allow '.' backspace or int
    if input == "." or input == '':
        return True
    try:
        float(input)
        return True
    except ValueError:
        return False

#Create new clicker button
def create_clicker_input(add_click_input, remove_click_input):
    row_offset = 2
    clicker_row = len(clicker_buttons) + row_offset

    #Create Click Input
    clicker_label = Label(frame, text="Clicker(s): ")
    clicker_label.grid(row=clicker_row, column=0, padx=(5, 0), pady=(5, 0))
    clicker_labels.append(clicker_label)
    
    input_clicker = Button(frame, text="Set Clicker Key", command=lambda: (set_input_clicker(clicker_row - 1 - row_offset)))
    input_clicker.grid(row=clicker_row, column=1, padx=(0, 15), pady=(5, 0))
    clicker_buttons.append(input_clicker)

    clicker_row += 1

    #Reposition Add/Remove Inputs
    add_click_input.grid(row=clicker_row, column=1, padx=(0, 45), pady=(5, 5))
    remove_click_input.grid(row=clicker_row, column=1, padx=(5, 0), pady=(5, 5))

#Delete new clicker button
def delete_clicker_input(add_click_input, remove_click_input):
    if clicker_buttons:
        print(clicker_buttons)
        row_offset = 2
        clicker_row = len(clicker_buttons) + row_offset

        #Destroy last one in list
        clicker_buttons[-1].destroy()
        clicker_buttons.pop()
        clicker_labels[-1].destroy()
        clicker_labels.pop()

        #Reposition Add/Remove Inputs
        add_click_input.grid(row=clicker_row - 1, column=1, padx=(0, 45), pady=(5, 5))
        remove_click_input.grid(row=clicker_row - 1, column=1, padx=(5, 0), pady=(5, 5))

        clicker_row -= 1

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

#region Created Widgets
#Main Window
window = Tk()
window.title("Auto Clicker")
window.wm_attributes("-topmost", 1)
center_window(window)

frame = Frame(window, width=250)
frame.pack()

#Create Trigger Input
Label(frame, text="Trigger: ").grid(row=0, column=0, padx=(5, 0), pady=(5, 0))

input_trigger = Button(frame, text="Set Trigger Key", command=lambda: (set_input_trigger()))
input_trigger.grid(row=0, column=1, padx=(0, 15), pady=(5, 0))

#Add Click Input
add_click_input = Button(frame, text="+", command=lambda: (create_clicker_input(add_click_input, remove_click_input)))
add_click_input.grid(row=3, column=1, padx=(0, 45), pady=(5, 5))

#Remove Click Input
remove_click_input = Button(frame, text="-", command=lambda: (delete_clicker_input(add_click_input, remove_click_input)))
remove_click_input.grid(row=3, column=1, padx=(5, 0), pady=(5, 5))

#First Clicker Input
create_clicker_input(add_click_input, remove_click_input)

#Create Click-Rate Input
Label(frame, text="Clicks/s: ").grid(row=0, column=2, padx=(5, 0), pady=(5, 0))

click_rate = Entry(frame, width=5)
click_rate.grid(row=0, column=3, padx=(0, 15), pady=(5, 0))
click_rate.insert(0, "100")
click_rate.config(validate="key", validatecommand=(window.register(validate_number), '%P'))

#Create Duration Time
Label(frame, text="Duration in Seconds: ").grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

duration_time = Entry(frame, width=5)
duration_time.grid(row=1, column=3, padx=(0, 15), pady=(5, 0))
duration_time.insert(0, "0")
duration_time.config(validate="key", validatecommand=(window.register(validate_number), '%P'))

#Create Duration Clicks
Label(frame, text="Duration in Clicks: ").grid(row=2, column=2, padx=(5, 0), pady=(5, 0))

duration_clicks = Entry(frame, width=5)
duration_clicks.grid(row=2, column=3, padx=(0, 15), pady=(5, 0))
duration_clicks.insert(0, "0")
duration_clicks.config(validate="key", validatecommand=(window.register(validate_number), '%P'))

#Create Toggle/Hold Checkbox
Label(frame, text="Toggle/Hold: ").grid(row=0, column=4, padx=(5, 0), pady=(5, 0))

toggle_checkbox = BooleanVar(value=True)
toggle_box = Checkbutton(frame, variable=toggle_checkbox)
toggle_box.grid(row=0, column=5, padx=(0, 15), pady=(5, 0))
#endregion

#Waiting for trigger key...
def set_input_trigger():
    global setting_trigger
    setting_trigger = True
    input_trigger.config(text="Press Key...")

#Set Trigger
def set_trigger(key):
    global trigger_key, setting_trigger
    if setting_trigger:
        try:
            trigger_key = key
            input_trigger.config(text=str(key))
            setting_trigger = False
        except AttributeError:
            pass

#Waiting for clicker key...
def set_input_clicker(clicker_index):
    global setting_clicker, current_clicker
    setting_clicker = True
    clicker_buttons[clicker_index].config(text="Press Key...")
    current_clicker = clicker_buttons[clicker_index]

#Set Clicker
def set_clicker(key, bMouse_Keyboard):
    global trigger_key, setting_clicker, clicker_keys, bIs_Mouse
    if setting_clicker:
        try:
            clicker_keys = key
            bIs_Mouse = bMouse_Keyboard
            current_clicker.config(text=str(key))
            setting_clicker = False
        except AttributeError:
            pass

#Keyboard press
def on_press(key):
    global bPress_Once, trigger_key

    if key == trigger_key:
        if bPress_Once == True:
            bPress_Once = False
            #Start/Stop auto clicker thread
            start_stop_thread(key)
  
    #Set Trigger
    set_trigger(key)

    #Set Clicker
    set_clicker(key, False)

#Keyboard Release
def on_release(key):
    global bPress_Once, trigger_key

    if key == trigger_key:
        bPress_Once = True
        #Start/Stop auto clicker thread
        if not toggle_checkbox.get():
            stop_thread()

#Mouse press
def on_click(x, y, key, pressed):
    if pressed:
        #Removes focus from text fields
        widget = window.winfo_containing(x, y)
        if widget in (click_rate, duration_clicks, duration_time):
            return  # Do nothing if clicked inside the Entry widget
        else:
            frame.focus()

        #Start/Stop auto clicker thread
        start_stop_thread(key)

        #Set Trigger
        set_trigger(key)

        #Set Clicker
        set_clicker(key, True)

#Start/Stop Auto Clicker Thread
def start_stop_thread(key):
    global total_clicks
    if not setting_trigger and clicker_keys and trigger_key is not None:
        #Stop after clicks
        stop_after_clicks(key)
        
        #Start/Stop Thread
        if key == trigger_key:
            if not click_thread.running:
                start_thread()
            else:
                stop_thread()

#Start Thread Function
def start_thread():
    global bIs_Mouse
    #Apply settings before starting
    click_thread.clicker_keys = clicker_keys
    click_thread.click_rate = float(click_rate.get().strip())
    click_thread.bIs_Mouse = bIs_Mouse
    click_thread.running = True
    #Duration handling
    try:
        seconds = float(duration_time.get().strip())
        if seconds > 0:
            #Schedule a stop after seconds
            threading.Timer(seconds, stop_thread).start()
    except:
        return

#Stop Thread Function
def stop_thread():
    global total_clicks
    total_clicks = 0
    click_thread.running = False

#Duration Clicks
def stop_after_clicks(key):
    global total_clicks
    
    #Make sure clicks is valid
    try:
        clicks = float(duration_clicks.get().strip())
        if clicks > 0:
            if key == clicker_keys:
                total_clicks += 1
                if total_clicks >= clicks:
                    stop_thread()
    except:
        return

#Thread to control clicks
class ClickThread(threading.Thread):
    def __init__(self):
        super(ClickThread, self).__init__()
        self.running = False
        self.program_running = True

    #Loops every .1 second to check whether to run. Better option?
    def run(self):
        while self.program_running:
            while self.running and self.click_rate > 0:
                if self.bIs_Mouse:
                    mouse_controller.click(self.clicker_keys)
                else:
                    keyboard_controller.press(self.clicker_keys)
                    keyboard_controller.release(self.clicker_keys)
                time.sleep(1/self.click_rate)
            time.sleep(0.1)

#Create Thread
click_thread = ClickThread()
click_thread.start()

#Listener for keyboard presses
listener_keyboard_press = keyboard.Listener(on_press=on_press, on_release=on_release)
threading.Thread(target=listener_keyboard_press.start).start()

#Listener for Mouse presses
listener_mouse = mouse.Listener(on_click=on_click)
threading.Thread(target=listener_mouse.start).start()

#Stop separate thread on window close
def on_close():
    click_thread.program_running = False
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
