#Create GUI and run the scripts
import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk

from GUI import appGUI
if __name__ == "__main__":
    csv_file = "CS2_ProPlayers_2025.csv"
    #root = tk.Tk()
    root = ttk.Window(themename = 'darkly')
    app = appGUI(root, csv_file)
    root.mainloop() #start the Tkinter event loop
