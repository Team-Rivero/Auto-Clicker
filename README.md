#Auto Clicker made using Python

#Create build
pyinstaller Script/clicker.py --name "Auto Clicker" --icon=Images/icon.ico --onefile --noconsole

#Bugs/Future Features:
Feature that holds clicker key instead of spams:
	Can be used to hold shift for you while you do other inputs basically.
	Currently modules don't seem to allow this capability.
	Using emulated usb keyboard to get working. Might not work on windows?

Multiple Clicker Keys:
	'KeyCode' object is not iterable. Caused from trying to run for loop of list of clicker keys. I think everything else is already set up properly aside from pressing 	the keys in the list instead of just one.

Only runs at 64 inputs a second with current thread.

Lower download size of 9mb.