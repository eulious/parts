#!/usr/bin/env python3

from time import sleep

open("log", "wt").write("")
while True:
    a = input()
    open("log", "at").write(a + "\n")
    # sleep(0.1)
    print(a)
