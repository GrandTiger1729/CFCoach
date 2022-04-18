from __future__ import annotations
from typing import *

import random
import json
import time, threading
import tkinter
from tkinter import ttk, tix
import webbrowser

import requests

import codeforces

class ProblemList:

    problemlist: List[codeforces.Problem] = []
    finished: List[bool]
    left: int = 0

    def __len__(self):
        return len(self.problemlist)

    def __getitem__(self, index):
        return self.problemlist[index]


    def fetch_problems(self, amount, **options):
        (problemlist, problem_statisticses) = codeforces.Problemset.problems(
            tags = options.get('tags'),
            problemsetName = options.get('problemsetName')
        )

        def _filter(problem: codeforces.Problem):
            return problem.rating is not None and options['lowerbound'] <= problem.rating <= options['upperbound']
        
        self.problemlist = random.choices(problemlist, k=amount)
        self.finished = [False] * amount
        self.left = amount

    def change_problem_state(self, index: int):
        if self.finished[index]:
            self.finished[index] = False
            self.left += 1
        else:
            self.finished[index] = True
            self.left -= 1

    def clear(self):
        self.problemlist.clear()
        self.finished.clear()

    def delete(self, index):
        self.finished[index] = True

    def add(self, index):
        self.finished[index] = False

class Training:

    handle: Optional[str] = None
    problem_options: dict
    problemlist: ProblemList = ProblemList()
    start_time: int = None
    finished = True
    check_var: List[tkinter.IntVar]
    duration: int
    showtags: bool
    autotrack: bool
    hold: List[str] = []

    def __init__(self, problem_frame):
        self.problem_frame: ttk.LabelFrame = problem_frame

        with open('settings.json', 'r') as f:
            data = json.load(f)
            self.duration = data['duration']
            self.problem_options = data['problem_options']
            self.showtags = data['showtags']
            self.autotrack = data['autotrack']

    @property
    def finished(self):
        return self.start_time is None or time.time() - self.start_time > self.duration or self.problemlist.left == 0

    def fetch_problems(self, **options):
        with open('settings.json', 'r') as f:
            data: dict = json.load(f)['problem_options']
            data.update(options)
            options = data
            amount = options['amount']
            options.pop('amount')
        
        self.problemlist.fetch_problems(amount, **options)
        self.check_var = [tkinter.IntVar(self.problem_frame) for _ in range(amount)]
    
    def start(self, **options):
        thread = threading.Thread(target=lambda: self._start(**options))
        thread.start()
       
    def _start(self, **options):
        with open('settings.json', 'r') as f:
            data = json.load(f)
            self.problem_options = options.get('problem_options') or data['problem_options']
            self.showtags = options.get('showtags') or data['showtags']
            self.autotrack = options.get('autotrack') or data['autotrack']

        self.fetch_problems(**self.problem_options)
        self.problem_frame.pack_forget()
        for item in reversed(self.problem_frame.winfo_children()):
            item.destroy()
        
        for i in range(len(self.problemlist)):
            problem = self.problemlist[i]

            ttk.Checkbutton(self.problem_frame,
                text=f'{i+1}.', variable=self.check_var[i],
                command=lambda i=i: self.change_problem_state(i)
            ).grid(row=3*i, column=0, rowspan=3)

            ttk.Label(self.problem_frame, text='Name: ').grid(row=3*i, column=1, padx=10)
            ttk.Label(self.problem_frame, text=problem.name).grid(row=3*i, column=2, padx=100)

            ttk.Label(self.problem_frame, text='Url: ').grid(row=3*i+1, column=1)
            link = ttk.Label(self.problem_frame, text=problem.url, foreground='blue', font='arail 9 underline')
            link.bind('<Button-1>', lambda e, url=problem.url: webbrowser.open_new_tab(url))
            link.grid(row=3*i+1, column=2)
            
            ttk.Label(self.problem_frame, text='tags: ').grid(row=3*i+2, column=1)
            if self.showtags:
                ttk.Label(self.problem_frame, text=str(problem.rating) + ', ' + ', '.join(problem.tags)).grid(row=3*i+2, column=2)
        
        self.problem_frame.pack()
        
        self.start_time = time.time()
        if not self.autotrack:
            return
        
        with open('settings.json', 'r') as f:
            data = json.load(f)
            self.duration = options.get('duration') or data['duration']
            self.handle = options.get('handle') or data['handle']
        
        thread = threading.Thread(target=self.track)
        thread.start()
        thread.join()
    
    def change_problem_state(self, index: int):
        self.problemlist.change_problem_state(index)
        self.check_var[index].set(self.problemlist.finished[index])

    def track(self):
        if self.finished:
            return
        
        def _track():
            (submission,) = codeforces.User.status(self.handle, 1, 1)
            if submission.creationTimeSeconds - self.start_time >= PERIOD:
                return
            self.check(submission)
        
        PERIOD = 30
        while not self.finished:
            start_period = time.perf_counter()
            _track()
            time.sleep(PERIOD - (time.perf_counter() - start_period))
            self.resolve()
        else:
            _track()
        
        while self.hold:
            start_period = time.perf_counter()
            self.resolve()
            time.sleep(PERIOD - (time.perf_counter() - start_period))

    def check(self, submission: codeforces.Submission):
        if submission.verdict == codeforces.SubmissionType('TESTING'):
            self.hold.append(submission.author.members[0].handle)
            return
    
    def resolve(self):
        hold = self.hold
        self.hold.clear()
        for handle in hold:
            self.check(self, handle)

