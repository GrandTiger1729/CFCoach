from __future__ import annotations
from typing import *

from tkinter import ttk
from tkinter import tix
import tkinter

from training import ProblemList, Training

class App:
    def __init__(self):
        self.mainframe = tix.Tk()
        self.mainframe.config(height=800, width=1000)
        self.mainframe.title('CFCoach')

        ttk.Label(self.mainframe, text='This is a Codeforces training program').pack(side='top')
        ttk.Label(self.mainframe, text='Support by GrandTiger').pack(side='bottom')
        problem_frame = ttk.LabelFrame(self.mainframe, borderwidth=5, text='Problemset', width=500, height=400)
        problem_frame.pack()

        self.training = Training(problem_frame)

        menu = tkinter.Menu(self.mainframe)
        self.mainframe.config(menu=menu)

        filemenu = tkinter.Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New', command=self.create)
        filemenu.add_command(label='Save')
        
    def create(self):
        options: dict = {}
        self.training.start(**options)

    def run(self):
        self.mainframe.mainloop()
        exit(0)

root = App()
root.run()