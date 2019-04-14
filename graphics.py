# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


LARGE_FONT= ("Verdana", 12)

callfunctions={"building": (lambda t: squarecall(t,8,18,10)) , "data_center": (lambda t: randomcall(t,7,3)), "PV_production": (lambda t:gaussiancall(t,12,2,-16)),"VE": (lambda t: randomcall(t,0,5))   }        
names=[ "building", "data_center", "PV_production", "VE"]
manager=Manager(names,callfunctions)        
manager.simulation(24)      

def plotload(player,ax):
    rects=[]
    for t in range(len(player.load)):
        rect= Rectangle( (t,0),1,player.load[t] )
        rects.append(rect)
    # Create patch collection with specified colour/alpha
    pc = PatchCollection(rects, alpha=0.5, facecolor="grey", edgecolor="black")
    # Add collection to axes
    ax.add_collection(pc)
    ax.set_xlim(0,len(player.load))
    ax.set_ylim(1.2*min(0,min(player.load)),1.2*max(player.load))
    ax.grid(True)
    ax.set_title(player.name+": load")
        
        
def plotbills(player,ax):
    rects=[]
    for t in range(len(player.bill)):
        rect= Rectangle( (t,0), 1, player.bill[t] )
        rects.append(rect)
    # Create patch collection with specified colour/alpha
    pc = PatchCollection(rects, alpha=0.5, facecolor="green", edgecolor="black")
    # Add collection to axes
    ax.add_collection(pc)
    ax.set_xlim(0,len(player.bill))
    ax.set_ylim(1.2*min(0,min(player.bill)),1.2*max(0,max(player.bill)))
    ax.grid(True)
    ax.set_title(player.name+": bill")
                
def plotsupplied(player, ax):
    rects=[]
    for t in range(len(player.supplied)):
        rect= Rectangle( (t,0), 1, player.supplied[t] )
        rects.append(rect)
    # Create patch collection with specified colour/alpha
    pc = PatchCollection(rects, alpha=0.5, facecolor="blue", edgecolor="black")
    ax.add_collection(pc)
    ax.set_xlim(0,len(player.supplied))
    ax.set_ylim(1.2*min(0,min(player.supplied)),1.2*max(0,max(player.supplied)))
    ax.grid(True)
    ax.set_title(player.name+": supplied load")
    
def plotbalance(manager,ax):                         
    rects=[]
    for t in range(len(manager.balance)):
        rect= Rectangle( (t,0), 1, manager.balance[t] )
        rects.append(rect)
        # Create patch collection with specified colour/alpha
    pc = PatchCollection(rects, alpha=0.5, facecolor="orange", edgecolor="black")
        # Add collection to axes
    ax.add_collection(pc)
    ax.set_xlim(0,len(manager.balance))
    ax.set_ylim(1.2*min(0,min(manager.balance)),1.2*max(0,max(manager.balance)))
    ax.grid(True)
    ax.set_xlabel("Global balance")    
       
class SummaryWindow(tk.Tk):

    def __init__(self, manager, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

       # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # first page
        frame= StartPage(container, self, manager)        
        self.frames["StartPage"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        
        
        #page for the manager
        frame= PageManager(container, self, manager)        
        self.frames["Manager"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        
        #pages for the players
        for name in manager.players:
            
            frame= PagePlayer(container, self, manager.players[name])   
            print("ajout", name)
            self.frames[name] = frame      
            frame.grid(row=0, column=0, sticky="nsew")
            
        for key in self.frames: print("key",key, self.frames[key])            
        self.show_frame("StartPage")

    def show_frame(self, cont):

        frame = self.frames[cont]
        print("affichage", cont)
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller, manager):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Who are you?", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Manager",
                            command=lambda: controller.show_frame("Manager"))
        button.pack()

        names=[]
        i=-1
        for name in manager.players:
            print("bouton",name)
            names.append(name)
            i+=1
            button=ttk.Button(self, text= name, command = lambda toto= i: controller.show_frame(names[toto])) ######## ici astuce 
            button.pack(fill=None)  
            
            
            
class PageManager(tk.Frame):

    def __init__(self, parent, controller, manager):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Manager", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack()

        f = Figure(figsize=(8,4), dpi=100)
        a = f.add_subplot(111)
        plotbalance(manager, a)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



class PagePlayer(tk.Frame):

    def __init__(self, parent, controller, player):
        tk.Frame.__init__(self, parent)
        print("remplissage_page", player.name)
        label = tk.Label(self, text=player.name, font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack()

        f = Figure(figsize=(20,8), dpi=100)
        a = f.add_subplot(221)
        plotload(player,a)

        a2 = f.add_subplot(222)
        plotsupplied(player,a2)

        a3 = f.add_subplot(223)
        plotbills(player,a3)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        