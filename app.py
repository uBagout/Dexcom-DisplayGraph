import datetime
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
import time
import threading
from pydexcom import Dexcom

import numpy as np
import os

#non-diabetic / non-dexcom user clarification:
#bg = blood glucose - measure of blood sugars that diabetics use to manage their condition
#transmitter - the transmitter attached to the dexcom sensor which we stick on our skin
#receiver - bluetooth receiver, referring to whichever device the user is using to receive transmitter data (either their phone or the official dexcom device)

dexcom = Dexcom("", "", True) #insert username and password here

class App(tk.Tk):
    def __init__(self, *args, **kwargs): #use to initialise settings
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "white")
        self.wm_attributes("-topmost", True) #draw window ontop of everything else as we want a permanent overlay
        #self.wm_attributes("-alpha", 1.0)

        
        f = plt.figure(figsize=(5,2), facecolor="none")
        f_canvas = FigureCanvasTkAgg(f, self)
        f_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        a = f.add_subplot()
   
        timeframe = 1440 #timeframe in minutes
        res = dexcom.get_glucose_readings(timeframe)  
        self.display_graph(a, res)

        timer_thread = threading.Thread(target = self.update, args = (a, res))
        timer_thread.start()


        self.grip = tk.Label(self, bitmap="gray25")
        self.grip.place(x= 63, y=45)

        self.grip.bind("<ButtonPress-1>", self.startpos)
        self.grip.bind("<ButtonRelease-1>", self.stoppos)
        self.grip.bind("<B1-Motion>", self.move)


    def update(self, a, res): #this should run every 5 minutes
        last = time.time()
        while True:
            if time.time() - last >= 300: 
                last = time.time()
                newread = dexcom.get_current_glucose_reading()
                #check invalid reading - signal loss - sensor not available
                if newread != None:
                    res.insert(0, newread)
                
                if res != None and len(res) > 288: #288 max number of readings in a day, no need to keep more in storage for plot
                        res.pop()

                self.display_graph(a, res)
        
    def display_graph(self, a, res, hours = 6): #make hours a setting to be changed
        a.clear()
        a.set_xlim(hours*12, 0.0)
        a.axis('off')

        if res != None and len(res) != 0: #no data check
            #we remake our x (time) and y (bg value) lists to plot each time we display the graph.
            #could optimise this by: changing each x value by 5 minutes, in update(), and if exceeds timeframe, pop x and y rather than recalculate full list each time

                   
            x = []
            y = []
            timelimit = datetime.datetime.now()
            
            #evaluate our timelimit to n hours before current time (there is a better way to do this before structuring the timelimit as a datetime)
            if timelimit.hour-hours < 0:
                timelimit = timelimit.replace(day = timelimit.day-1)
                timelimit = timelimit.replace(hour = timelimit.hour-hours+24)
            else:
                timelimit = timelimit.replace(hour = timelimit.hour-hours)

            #take all times in res that convene to the selected timeframe   
            #could find earliest corresponding indice that fits within the timeframe, but we still need to iterate over to assign x so is a minimal improvement
            for r in res:
                if r.time > timelimit:
                    delta = (r.time - timelimit) // datetime.timedelta(0, 300) #300s = 5 minute intervals
                    x.append(delta) 
                    y.append(r.mmol_l)
            x.reverse()
            
            a.plot(x, y, color='gray', alpha=1.0)

        a.hlines([4.0 , 12.0], 0, hours*12, ['r', 'y']) #12 sets of 5 minute intervals in an hour

        # finish tkinter gui stuff, save graph location for next run, use env variables / text config for program settings
        #figure out better graph transparency, currently there is a non transparent outline around the plot, but it works fine on white backgrounds (most browser webpages)

    def startpos(self, event):
        self.x = event.x
        self.y = event.y

    def stoppos(self, event):
        self.x = None
        self.y = None

    def move(self, event):
        x = (event.x_root - self.x + self.winfo_x() - self.grip.winfo_rootx())
        y = (event.y_root - self.y + self.winfo_y() - self.grip.winfo_rooty())
        self.geometry(f"+{x}+{y}")

app = App()
app.mainloop()
