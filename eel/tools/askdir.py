#!/usr/bin/env python3

from tkinter import Tk
from platform import system
from tkinter.filedialog import askdirectory

root = Tk()
root.withdraw()
IS_MAC = system() == "Darwin"
path = askdirectory()
print(path)
