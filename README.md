#Auto Clicker made using Python

#Create build
pyinstaller Script/clicker.py --name "Auto Clicker" --icon=Images/icon.ico --onefile --noconsole

#Bugs/Future Features:
Feature that holds clicker key instead of spams:
	Can be used to hold shift for you while you do other inputs basically.
	Running on separate thread might be cause. Was able to get it working fine for macro

Multiple Clicker Keys:
	'KeyCode' object is not iterable. Caused from trying to run for loop of list of clicker keys. I think everything else is already set up properly aside from pressing the keys in the list instead of just one.
	Remove thread? Might solve holding key problem. Forgot why it was needed in the first place.

Only runs at 64 inputs a second with current thread.

Lower download size of 9mb.
