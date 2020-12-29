import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    class ScrollableArea(ttk.Frame):
        def __init__(self, canvas, parent):
            super().__init__(canvas)
            self.parent = parent

    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.parent = container
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = self.ScrollableArea(canvas, self.parent)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
