import tkinter as tk


class TimePicker(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.reg = self.register(self.hour_valid)
        self.hourstr = tk.StringVar(self, '10')
        self.hour = tk.Spinbox(self, from_=0, to=23, wrap=True, validate='focusout', validatecommand=(self.reg, '%P'),
                               invalidcommand=self.hour_invalid, textvariable=self.hourstr, width=2)
        self.reg2 = self.register(self.min_valid)
        self.minstr = tk.StringVar(self, '30')
        self.min = tk.Spinbox(self, from_=0, to=59, wrap=True, validate='focusout', validatecommand=(self.reg2, '%P'),
                              invalidcommand=self.min_invalid, textvariable=self.minstr, width=2)
        self.hour.grid()
        self.min.grid(row=0, column=1)

    def hour_invalid(self):
        self.hourstr.set('10')

    def hour_valid(self, eingabe):
        if eingabe.isdigit() and int(eingabe) in range(24) and len(eingabe) in range(1, 3):
            valid = True
        else:
            valid = False
        if not valid:
            self.hour.after_idle(lambda: self.hour.config(validate='focusout'))
        return valid

    def min_invalid(self):
        self.minstr.set('30')

    def min_valid(self, eingabe):
        if eingabe.isdigit() and int(eingabe) in range(60) and len(eingabe) in range(1, 3):
            valid = True
        else:
            valid = False
        if not valid:
            self.min.after_idle(lambda: self.min.config(validate='focusout'))
        return valid
