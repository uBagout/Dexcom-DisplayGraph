import datetime
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys
import threading
from pydexcom import Dexcom

import numpy as np
import os
import dotenv



dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

API_USER = os.environ["API_USER"]
API_PASSWORD = os.environ['API_PASSWORD']
TIMEFRAME= int(os.environ['TIMEFRAME'])
XPOS = int(os.environ['XPOS'])
YPOS = int(os.environ['YPOS'])
lHYPO = float(os.environ['HYPOLIMIT'])
lHYPER = float(os.environ['HYPERLIMIT'])


#non-diabetic / non-dexcom user clarification:
#bg = blood glucose - measure of blood sugars that diabetics use to manage their condition
#transmitter - the transmitter attached to the dexcom sensor which we stick on our skin
#receiver - bluetooth receiver, referring to whichever device the user is using to receive transmitter data (either their phone or the official dexcom device)
#lHYPO, lHYPER. Blood Glucose Values (in mmol/L) for Hypoglycaemia, Hyperglycaemia Limits

dexcom = Dexcom(API_USER, API_PASSWORD, True)

f = plt.figure(figsize=(5,2), facecolor="white", alpha=0)
a = f.add_subplot()


def animate(i):
    res = dexcom.get_glucose_readings(TIMEFRAME) 
    
    a.clear()

    a.set_xlim(TIMEFRAME//12, 0.0)
    a.axis('off')
    a.hlines([lHYPO , lHYPER], 0, TIMEFRAME//12, colors= ['r', 'y'])
    if res != None and len(res) != 0: #no data check
             
        x = []
        y = []
        timelimit = datetime.datetime.now()
            

        if timelimit.hour-TIMEFRAME//60 < 0:
            timelimit = timelimit.replace(day = timelimit.day-1)
            timelimit = timelimit.replace(hour = timelimit.hour-TIMEFRAME//60+24)
        else:
            timelimit = timelimit.replace(hour = timelimit.hour-TIMEFRAME//60)

        for r in res:
            if r.time > timelimit:
                delta = (r.time - timelimit) // datetime.timedelta(0, 300) #300s = 5 minute intervals
                x.append(delta) 
                y.append(r.mmol_l)
        x.reverse()
    
        a.plot(x, y, color='gray', alpha=1.0)
    

class App(tk.Tk):
    def __init__(self, *args, **kwargs): #use to initialise settings
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.configure(background='white')
        self.wm_attributes("-transparentcolor", "white")

        self.wm_attributes("-topmost", True) #draw window ontop of all others to create an overlay - this does not affect fullscreen applications

        self.f_canvas = FigureCanvasTkAgg(f, self)
        self.f_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        animate(1) #force animation
    

        self.grip = tk.Label(self, bitmap="gray25")
        self.grip.place(x= 63, y=45)

        self.grip.bind('<Triple-Button-1>', self.closeapp)
        self.grip.bind("<ButtonPress-1>", self.startpos)
        self.grip.bind("<ButtonRelease-1>", self.stoppos)
        self.grip.bind("<B1-Motion>", self.move)

        self.geometry(f"+{XPOS}+{YPOS}")
    
    def closeapp(self, event):
        sys.exit()

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

        dotenv.set_key(dotenv_file, "XPOS", str(x))
        dotenv.set_key(dotenv_file, "YPOS", str(y))

app = App()
ani = animation.FuncAnimation(f, animate, interval=300000)
app.mainloop()
