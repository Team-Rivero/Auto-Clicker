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

class ClickerApp:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = ClickerSettings()

        #Instance of mouse and keyboard controller created
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

        #Create Thread
        self.click_thread = ClickButton(self.settings, self.mouse_controller, self.keyboard_controller)
        self.click_thread.start()

        self.setup_listeners()
        self.create_widgets()
        self.center_window()

    #Center Window on screen
    def center_window(self):
        #Get screen width and height
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()

        #Calculate position coordinates
        x = (screen_width // 2) - (self.main_window.winfo_reqwidth() // 2)
        y = (screen_height // 2) - (self.main_window.winfo_reqheight() // 2)

        #Set the position of the window
        self.main_window.geometry(f'+{x}+{y}')

    #Create Widgets
    def create_widgets(self):
        #Main Window
        self.main_window.title("Auto Clicker")
        self.main_window.wm_attributes("-topmost", 1)

        self.frame = Frame(self.main_window, width=250)
        self.frame.pack()

        #Create Trigger Input
        Label(self.frame, text="Trigger: ").grid(row=0, column=0, padx=(5, 0), pady=(5, 0))

        self.input_trigger = Button(self.frame, text="Set Trigger Key", command=lambda: (self.set_input_trigger()))
        self.input_trigger.grid(row=0, column=1, padx=(0, 15), pady=(5, 0))
        self.bind_tooltip(self.input_trigger, "Trigger Input:\nControls starting and stopping the auto clicker.\nAccepts any key or mouse button.")

        #Add Click Input
        self.add_click_input = Button(self.frame, text="+", command=lambda: (self.create_clicker_input(self.add_click_input, self.remove_click_input)))
        self.add_click_input.grid(row=3, column=1, padx=(0, 45), pady=(5, 5))

        #Remove Click Input
        self.remove_click_input = Button(self.frame, text="-", command=lambda: (self.delete_clicker_input(self.add_click_input, self.remove_click_input)))
        self.remove_click_input.grid(row=3, column=1, padx=(5, 0), pady=(5, 5))

        #First Clicker Input
        self.create_clicker_input(self.add_click_input, self.remove_click_input)

        #Create Click-Rate Input
        Label(self.frame, text="Clicks/s: ").grid(row=0, column=2, padx=(5, 0), pady=(5, 0))

        self.click_rate = Entry(self.frame, width=5)
        self.click_rate.grid(row=0, column=3, padx=(0, 15), pady=(5, 0))
        self.click_rate.insert(0, "100")
        self.click_rate.config(validate="key", validatecommand=(self.main_window.register(self.validate_number), '%P'))
        self.bind_tooltip(self.click_rate, "Clicks per Second:\nPresses the clicker input at the rate provided.\nAccepts float values.")

        #Create Duration Time
        Label(self.frame, text="Duration in Seconds: ").grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

        self.duration_time = Entry(self.frame, width=5)
        self.duration_time.grid(row=1, column=3, padx=(0, 15), pady=(5, 0))
        self.duration_time.insert(0, "0")
        self.duration_time.config(validate="key", validatecommand=(self.main_window.register(self.validate_number), '%P'))
        self.bind_tooltip(self.duration_time, "Duration in Seconds:\nStops clicker after reaching duration.\nAccepts float values.\nStops if duration in clicks occurs first.\nCan still be stopped with trigger.")

        #Create Duration Clicks
        Label(self.frame, text="Duration in Clicks: ").grid(row=2, column=2, padx=(5, 0), pady=(5, 0))

        self.duration_clicks = Entry(self.frame, width=5)
        self.duration_clicks.grid(row=2, column=3, padx=(0, 15), pady=(5, 0))
        self.duration_clicks.insert(0, "0")
        self.duration_clicks.config(validate="key", validatecommand=(self.main_window.register(self.validate_number), '%P'))
        self.bind_tooltip(self.duration_clicks, "Duration in Clicks:\nStops clicker after reaching click count.\nAccepts float values.\nStops if duration in seconds occurs first.\nCan still be stopped with trigger.")

        #Create Toggle/Hold Checkbox
        Label(self.frame, text="Toggle/Hold: ").grid(row=0, column=4, padx=(5, 0), pady=(5, 0))

        self.toggle_checkbox = BooleanVar(value=True)
        self.toggle_box = Checkbutton(self.frame, variable=self.toggle_checkbox)
        self.toggle_box.grid(row=0, column=5, padx=(0, 15), pady=(5, 0))
        self.bind_tooltip(self.toggle_box, "Toggle/Hold:\nToggle = Pressing trigger starts clicker until pressed again.\nHold = Pressing trigger runs clicker till released.")

    #Create new clicker widget
    def create_clicker_input(self, add_click_input, remove_click_input):
        row_offset = 2
        clicker_row = len(self.settings.clicker_buttons) + row_offset

        #Create Click Input
        self.clicker_label = Label(self.frame, text="Clicker(s): ")
        self.clicker_label.grid(row=clicker_row, column=0, padx=(5, 0), pady=(5, 0))
        self.settings.clicker_labels.append(self.clicker_label)

        self.input_clicker = Button(self.frame, text="Set Clicker Key", command=lambda: (self.set_input_clicker(clicker_row - 1 - row_offset)))
        self.input_clicker.grid(row=clicker_row, column=1, padx=(0, 15), pady=(5, 0))
        self.settings.clicker_buttons.append(self.input_clicker)
        self.bind_tooltip(self.input_clicker, "Clicker Input:\nThe button that is pressed when auto clicking.\nAccepts any key or mouse button.")

        clicker_row += 1

        #Reposition Add/Remove Inputs
        add_click_input.grid(row=clicker_row, column=1, padx=(0, 45), pady=(5, 5))
        remove_click_input.grid(row=clicker_row, column=1, padx=(5, 0), pady=(5, 5))

    #Delete new clicker widget
    def delete_clicker_input(self, add_click_input, remove_click_input):
        if self.settings.clicker_buttons:
            row_offset = 2
            clicker_row = len(self.settings.clicker_buttons) + row_offset

            #Destroy last one in list
            self.settings.clicker_buttons[-1].destroy()
            self.settings.clicker_buttons.pop()
            self.settings.clicker_labels[-1].destroy()
            self.settings.clicker_labels.pop()

            #Reposition Add/Remove Inputs
            add_click_input.grid(row=clicker_row - 1, column=1, padx=(0, 45), pady=(5, 5))
            remove_click_input.grid(row=clicker_row - 1, column=1, padx=(5, 0), pady=(5, 5))

            clicker_row -= 1

    #Validate entry inputs
    def validate_number(self, input):
        # Allow '.' backspace or int
        if input == "." or input == '':
            return True
        try:
            float(input)
            return True
        except ValueError:
            return False

    #region Tooltips
    def show_tooltip(self, event, Tooltip_Text):
        if self.settings.tooltip_window or not self.main_window.winfo_viewable():
            return
        x, y = event.x_root + 20, event.y_root - 20
        self.settings.tooltip_window = Toplevel(self.main_window)
        self.settings.tooltip_window.wm_overrideredirect(True)
        self.settings.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = Label(self.settings.tooltip_window, text=Tooltip_Text, relief="solid", borderwidth=1)
        self.settings.tooltip_window.attributes('-topmost', True)  # Set tooltip to be topmost
        label.pack()

    def start_tooltip(self, event, Tooltip_Text):
        self.settings.after_id = self.main_window.after(200, self.show_tooltip, event, Tooltip_Text)

    def stop_tooltip(self, event):    
        if self.settings.after_id:
            self.main_window.after_cancel(self.settings.after_id)
            self.settings.after_id = None
        if self.settings.tooltip_window:
            self.settings.tooltip_window.destroy()
            self.settings.tooltip_window = None
    #endregion

    def bind_tooltip(self, widget, tooltip_text):
        widget.bind("<Enter>", lambda event: self.start_tooltip(event, tooltip_text))
        widget.bind("<Leave>", self.stop_tooltip)

    #Waiting for trigger key...
    def set_input_trigger(self):
        self.settings.setting_trigger = True
        self.input_trigger.config(text="Press Key...")

    #Set Trigger
    def set_trigger(self, key):
        if self.settings.setting_trigger:
            try:
                self.settings.trigger_key = key
                self.input_trigger.config(text=str(key))
                self.settings.setting_trigger = False
            except AttributeError:
                pass

    #Waiting for clicker key...
    def set_input_clicker(self, clicker_index):
        self.settings.setting_clicker = True
        self.settings.clicker_buttons[clicker_index].config(text="Press Key...")
        self.settings.current_clicker = self.settings.clicker_buttons[clicker_index]

    #Set Clicker
    def set_clicker(self, key, bMouse_Keyboard):
        if self.settings.setting_clicker:
            try:
                self.settings.clicker_keys = key
                self.settings.bIs_Mouse = bMouse_Keyboard
                self.settings.current_clicker.config(text=str(key))
                self.settings.setting_clicker = False
            except AttributeError:
                pass

    #Keyboard press
    def on_press(self, key):
        if key == self.settings.trigger_key:
            if self.settings.bPress_Once == True:
                self.settings.bPress_Once = False
                #Start/Stop auto clicker thread
                self.start_stop_thread(key)
    
        #Set Trigger
        self.set_trigger(key)

        #Set Clicker
        self.set_clicker(key, False)

    #Keyboard Release
    def on_release(self, key):
        if key == self.settings.trigger_key:
            self.settings.bPress_Once = True
            #Start/Stop auto clicker thread
            if not self.toggle_checkbox.get():
                self.stop_thread()

    #Mouse press
    def on_click(self, x, y, key, pressed):
        if pressed:
            #Removes focus from text fields
            widget = self.main_window.winfo_containing(x, y)
            if widget in (self.click_rate, self.duration_clicks, self.duration_time):
                return  # Do nothing if clicked inside the Entry widget
            else:
                self.frame.focus()

            #Start/Stop auto clicker thread
            self.start_stop_thread(key)

            #Set Trigger
            self.set_trigger(key)

            #Set Clicker
            self.set_clicker(key, True)
        if pressed == False:
            if key == self.settings.trigger_key:
                self.settings.bPress_Once = True
                #Start/Stop auto clicker thread
                if not self.toggle_checkbox.get():
                    self.stop_thread()

    #Start/Stop Auto Clicker Thread
    def start_stop_thread(self, key):
        if not self.settings.setting_trigger and self.settings.clicker_keys and self.settings.trigger_key is not None:
            #Stop after clicks
            self.stop_after_clicks(key)

            #Start/Stop Thread
            if key == self.settings.trigger_key:
                if not self.click_thread.running:
                    self.start_thread()
                else:
                    self.stop_thread()

    #Start Thread Function
    def start_thread(self):
        #Apply settings before starting
        self.click_thread.clicker_keys = self.settings.clicker_keys
        self.click_thread.click_rate = float(self.click_rate.get().strip())
        self.click_thread.bIs_Mouse = self.settings.bIs_Mouse
        self.click_thread.running = True
        #Duration handling
        try:
            seconds = float(self.duration_time.get().strip())
            if seconds > 0:
                #Schedule a stop after seconds
                threading.Timer(seconds, self.stop_thread).start()
        except:
            return

    #Stop Thread Function
    def stop_thread(self):
        self.settings.total_clicks = 0
        self.click_thread.running = False

    #Duration Clicks
    def stop_after_clicks(self, key):    
        #Make sure clicks is valid
        try:
            clicks = float(self.duration_clicks.get().strip())
            if clicks > 0:
                if key == self.settings.clicker_keys:
                    self.settings.total_clicks += 1
                    if self.settings.total_clicks >= clicks:
                        self.stop_thread()
        except:
            return
    
    #Setup Listeners
    def setup_listeners(self):
        #Listener for keyboard presses
        listener_keyboard_press = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        threading.Thread(target=listener_keyboard_press.start).start()

        #Listener for Mouse presses
        listener_mouse = mouse.Listener(on_click=self.on_click)
        threading.Thread(target=listener_mouse.start).start()

    #Stop separate thread on window close
    def on_close(self):
        self.click_thread.program_running = False
        self.main_window.destroy()

#Thread to control clicks
class ClickButton(threading.Thread):
    def __init__(self, settings, mouse_controller, keyboard_controller):
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
                    self.mouse_controller.click(self.clicker_keys)
                else:
                    self.keyboard_controller.press(self.clicker_keys)
                time.sleep(1/self.click_rate)
            time.sleep(0.1)

if __name__ == "__main__":
    main_window = Tk()
    app = ClickerApp(main_window)
    main_window.protocol("WM_DELETE_WINDOW", app.on_close)
    main_window.mainloop()
