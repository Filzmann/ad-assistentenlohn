import tkinter as tk
from tkinter import ttk

from scollable_frame import ScrollableFrame

root = tk.Tk()

frame = ScrollableFrame(root)

for i in range(50):
    ttk.Label(frame.scrollable_frame, text="Sample scrolling label").pack()

frame.pack()
root.mainloop()