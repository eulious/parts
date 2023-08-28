#!/usr/bin/env python3

import eel
from tkinter import Tk
from platform import system
from subprocess import call
from tkinter.filedialog import askdirectory

IS_MAC = system() == "Darwin"
IS_WINDOWS = system() == "Windows"
IS_LINUX = system() == "Linux"

root = Tk()
root.withdraw()


def print_ret(ret):
    print("ret", ret)


@eel.expose
def hello(x):
    print("x", x)
    eel.add(x, 2)(print_ret)
    return x


@eel.expose
def askdirpath():
    if IS_MAC:
        call("(sleep 1; open -a python) &", shell=True)
    path = askdirectory()
    print("path", path)
    return path


eel.init("web/dist")
eel.start("index.html", size=(1024, 768), port=5468)
