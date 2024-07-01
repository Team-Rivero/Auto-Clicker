from tkinter import *
import time
import threading
from pynput import mouse, keyboard

#Global Variables
class ClickerSettings:
    def __init__(self):
        #Trigger Variables
        self.trigger_key = None
        self.setting_trigger = False
        self.bPress_Once = True

        #Clicker Variables
        self.clicker_labels = []
        self.clicker_buttons = []
        self.clicker_keys = []
        self.setting_clicker = False
        self.current_clicker = None
        self.bIs_Mouse = None
        self.total_clicks = 0

        #Tooltip variables
        self.tooltip_window = None
        self.after_id = None

settings = ClickerSettings()

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

#region Tooltips
def show_tooltip(event, Tooltip_Text):
    if settings.tooltip_window or not main_window.winfo_viewable():
        return
    x, y = event.x_root + 20, event.y_root - 20
    settings.tooltip_window = Toplevel(main_window)
    settings.tooltip_window.wm_overrideredirect(True)
    settings.tooltip_window.wm_geometry(f"+{x}+{y}")
    label = Label(settings.tooltip_window, text=Tooltip_Text, relief="solid", borderwidth=1)
    settings.tooltip_window.attributes('-topmost', True)  # Set tooltip to be topmost
    label.pack()

def start_tooltip(event, Tooltip_Text):
    settings.after_id = main_window.after(200, show_tooltip, event, Tooltip_Text)

def stop_tooltip(event):    
    if settings.after_id:
        main_window.after_cancel(settings.after_id)
        settings.after_id = None
    if settings.tooltip_window:
        settings.tooltip_window.destroy()
        settings.tooltip_window = None
#endregion

def bind_tooltip(widget, tooltip_text):
    widget.bind("<Enter>", lambda event: start_tooltip(event, tooltip_text))
    widget.bind("<Leave>", stop_tooltip)

#Create new clicker button
def create_clicker_input(add_click_input, remove_click_input):
    row_offset = 2
    clicker_row = len(settings.clicker_buttons) + row_offset

    #Create Click Input
    clicker_label = Label(frame, text="Clicker(s): ")
    clicker_label.grid(row=clicker_row, column=0, padx=(5, 0), pady=(5, 0))
    settings.clicker_labels.append(clicker_label)
    
    input_clicker = Button(frame, text="Set Clicker Key", command=lambda: (set_input_clicker(clicker_row - 1 - row_offset)))
    input_clicker.grid(row=clicker_row, column=1, padx=(0, 15), pady=(5, 0))
    settings.clicker_buttons.append(input_clicker)
    bind_tooltip(input_clicker, "Clicker Input:\nThe button that is pressed when auto clicking.\nAccepts any key or mouse button.")

    clicker_row += 1

    #Reposition Add/Remove Inputs
    add_click_input.grid(row=clicker_row, column=1, padx=(0, 45), pady=(5, 5))
    remove_click_input.grid(row=clicker_row, column=1, padx=(5, 0), pady=(5, 5))

#Delete new clicker button
def delete_clicker_input(add_click_input, remove_click_input):
    if settings.clicker_buttons:
        print(settings.clicker_buttons)
        row_offset = 2
        clicker_row = len(settings.clicker_buttons) + row_offset

        #Destroy last one in list
        settings.clicker_buttons[-1].destroy()
        settings.clicker_buttons.pop()
        settings.clicker_labels[-1].destroy()
        settings.clicker_labels.pop()

        #Reposition Add/Remove Inputs
        add_click_input.grid(row=clicker_row - 1, column=1, padx=(0, 45), pady=(5, 5))
        remove_click_input.grid(row=clicker_row - 1, column=1, padx=(5, 0), pady=(5, 5))

        clicker_row -= 1

#Center Window on screen
def center_window(main_window):
    #Get screen width and height
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    #Calculate position coordinates
    x = (screen_width // 2) - (main_window.winfo_reqwidth() // 2)
    y = (screen_height // 2) - (main_window.winfo_reqheight() // 2)

    #Set the position of the window
    main_window.geometry(f'+{x}+{y}')

#region Created Widgets
#Main Window
main_window = Tk()
main_window.title("Auto Clicker")
main_window.wm_attributes("-topmost", 1)
center_window(main_window)

frame = Frame(main_window, width=250)
frame.pack()

#Create Trigger Input
Label(frame, text="Trigger: ").grid(row=0, column=0, padx=(5, 0), pady=(5, 0))

input_trigger = Button(frame, text="Set Trigger Key", command=lambda: (set_input_trigger()))
input_trigger.grid(row=0, column=1, padx=(0, 15), pady=(5, 0))
bind_tooltip(input_trigger, "Trigger Input:\nControls starting and stopping the auto clicker.\nAccepts any key or mouse button.")

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
click_rate.config(validate="key", validatecommand=(main_window.register(validate_number), '%P'))
bind_tooltip(click_rate, "Clicks per Second:\nPresses the clicker input at the rate provided.\nAccepts float values.")

#Create Duration Time
Label(frame, text="Duration in Seconds: ").grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

duration_time = Entry(frame, width=5)
duration_time.grid(row=1, column=3, padx=(0, 15), pady=(5, 0))
duration_time.insert(0, "0")
duration_time.config(validate="key", validatecommand=(main_window.register(validate_number), '%P'))
bind_tooltip(duration_time, "Duration in Seconds:\nStops clicker after reaching duration.\nAccepts float values.\nStops if duration in clicks occurs first.\nCan still be stopped with trigger.")

#Create Duration Clicks
Label(frame, text="Duration in Clicks: ").grid(row=2, column=2, padx=(5, 0), pady=(5, 0))

duration_clicks = Entry(frame, width=5)
duration_clicks.grid(row=2, column=3, padx=(0, 15), pady=(5, 0))
duration_clicks.insert(0, "0")
duration_clicks.config(validate="key", validatecommand=(main_window.register(validate_number), '%P'))
bind_tooltip(duration_clicks, "Duration in Clicks:\nStops clicker after reaching click count.\nAccepts float values.\nStops if duration in seconds occurs first.\nCan still be stopped with trigger.")

#Create Toggle/Hold Checkbox
Label(frame, text="Toggle/Hold: ").grid(row=0, column=4, padx=(5, 0), pady=(5, 0))

toggle_checkbox = BooleanVar(value=True)
toggle_box = Checkbutton(frame, variable=toggle_checkbox)
toggle_box.grid(row=0, column=5, padx=(0, 15), pady=(5, 0))
bind_tooltip(toggle_box, "Toggle/Hold:\nToggle = Pressing trigger starts clicker until pressed again.\nHold = Pressing trigger runs clicker till released.")
#endregion

#Waiting for trigger key...
def set_input_trigger():
    settings.setting_trigger = True
    input_trigger.config(text="Press Key...")

#Set Trigger
def set_trigger(key):
    if settings.setting_trigger:
        try:
            settings.trigger_key = key
            input_trigger.config(text=str(key))
            settings.setting_trigger = False
        except AttributeError:
            pass

#Waiting for clicker key...
def set_input_clicker(clicker_index):
    settings.setting_clicker = True
    settings.clicker_buttons[clicker_index].config(text="Press Key...")
    settings.current_clicker = settings.clicker_buttons[clicker_index]

#Set Clicker
def set_clicker(key, bMouse_Keyboard):
    if settings.setting_clicker:
        try:
            settings.clicker_keys = key
            settings.bIs_Mouse = bMouse_Keyboard
            settings.current_clicker.config(text=str(key))
            settings.setting_clicker = False
        except AttributeError:
            pass

#Keyboard press
def on_press(key):

    if key == settings.trigger_key:
        if settings.bPress_Once == True:
            settings.bPress_Once = False
            #Start/Stop auto clicker thread
            start_stop_thread(key)
  
    #Set Trigger
    set_trigger(key)

    #Set Clicker
    set_clicker(key, False)

#Keyboard Release
def on_release(key):
    if key == settings.trigger_key:
        settings.bPress_Once = True
        #Start/Stop auto clicker thread
        if not toggle_checkbox.get():
            stop_thread()

#Mouse press
def on_click(x, y, key, pressed):
    if pressed:
        #Removes focus from text fields
        widget = main_window.winfo_containing(x, y)
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
    if pressed == False:
        if key == settings.trigger_key:
            settings.bPress_Once = True
            #Start/Stop auto clicker thread
            if not toggle_checkbox.get():
                stop_thread()

#Start/Stop Auto Clicker Thread
def start_stop_thread(key):
    if not settings.setting_trigger and settings.clicker_keys and settings.trigger_key is not None:
        #Stop after clicks
        stop_after_clicks(key)
        
        #Start/Stop Thread
        if key == settings.trigger_key:
            if not click_thread.running:
                start_thread()
            else:
                stop_thread()

#Start Thread Function
def start_thread():
    #Apply settings before starting
    click_thread.clicker_keys = settings.clicker_keys
    click_thread.click_rate = float(click_rate.get().strip())
    click_thread.bIs_Mouse = settings.bIs_Mouse
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
    settings.total_clicks = 0
    click_thread.running = False

#Duration Clicks
def stop_after_clicks(key):    
    #Make sure clicks is valid
    try:
        clicks = float(duration_clicks.get().strip())
        if clicks > 0:
            if key == settings.clicker_keys:
                settings.total_clicks += 1
                if settings.total_clicks >= clicks:
                    stop_thread()
    except:
        return

#Thread to control clicks
class ClickButton(threading.Thread):
    def __init__(self):
        super(ClickButton, self).__init__()
        self.settings = settings
        self.mouse_controller = mouse_controller
        self.keyboard_controller = keyboard_controller
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
click_thread = ClickButton()
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
    main_window.destroy()

main_window.protocol("WM_DELETE_WINDOW", on_close)
main_window.mainloop()
