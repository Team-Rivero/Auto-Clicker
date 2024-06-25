from tkinter import *
import time
import threading
from pynput import mouse, keyboard

# button = mouse.Button.right
#Default Input
#button_to_click = 'e'
#Default Trigger Input Key
start_stop_key = keyboard.KeyCode(char='a')

#Create Window
window = Tk()
frame = Frame(window)
frame.pack()

#Define Start/Stop Key  DOESN'T WORK FOR MOUSE BUTTONS
def on_single_key(e):
    global start_stop_key

    window.unbind("<KeyPress>")
    start_stop_key = keyboard.KeyCode(char=chr(e.keycode).lower())
    trigger_button.config(text=str(e.keycode) + " | " + chr(e.keycode).lower())
    #print(start_stop_key)

#Input Trigger Button
trigger_button = Button(window, text=start_stop_key.char)
trigger_button.config(command=lambda: (window.bind("<KeyPress>" , on_single_key), trigger_button.config(text=" ")))
trigger_button.pack()

#Clicks per second input
click_rate = Text(window, height = 1, width = 3)
click_rate.insert("1.0", "1")
click_rate.pack()

#Button To Press
button_to_click = Text(window, height = 1, width = 3)
button_to_click.insert("1.0", "e")
button_to_click.pack()

# threading.Thread is used
# to control clicks
class ClickMouse(threading.Thread):
    def __init__(self):
        super(ClickMouse, self).__init__()
        self.running = False
        self.program_running = True
  
    def start_clicking(self):
        self.running = True
  
    def stop_clicking(self):
        self.running = False

    # method to check and run loop until
    # it is true another loop will check
    # if it is set to true or not,
    # for mouse click it set to button
    # and click rate.
    def run(self):
        while self.program_running:
            print("Running?")
            while self.running:
                #mouse.click(self.button)
                controller.press(self.button_to_click)
                time.sleep(self.click_rate)
            time.sleep(0.1)

# instance of mouse controller is created
mouse = mouse.Controller()
click_thread = ClickMouse()
click_thread.start()

#Instance of keyboard controller created
controller = keyboard.Controller()

#Checks if pressed key is input trigger key to start/stop
def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            #apply settings before starting
            click_thread.button_to_click = (button_to_click.get("1.0", END).strip())
            click_thread.click_rate = float(click_rate.get("1.0", END).strip())
            click_thread.start_clicking()

# Create a listener instance
listener = keyboard.Listener(on_press=on_press)

# Start the listener in a separate thread
listener_thread = threading.Thread(target=listener.start)
listener_thread.start()

window.mainloop()
