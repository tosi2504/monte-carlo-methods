import tkinter as tk
import re


# layout:
# input N, seed, pf. button set. When set pressed -> grayed out and windows spawn
# input temperature, beta
# buttons start, pause, thermalize


def check_pos_int(str):
    return re.fullmatch(r"[0-9]+", str) is not None

def check_pos_float(str):
    if len(str) == 0:
        return True
    else:
        return re.fullmatch(r"([0-9]+([.][0-9]*)?|[.][0-9]+)", str) is not None

class FloatEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        self.var = tk.StringVar()
        super().__init__(master = parent, textvariable = self.var, **kwargs)
        self.parent = parent
        self.old_value = ""
        self.var.trace("w", self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        if check_pos_float(self.get()):
            self.old_value = self.get()
        else:
            self.set(self.old_value)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_grid_properties_interface()
        self.create_temperature_interface()
        self.create_play_interface()

    def run(self):
        self.mainloop()

    def create_grid_properties_interface(self):
        self.lbl_N = tk.Label(self, text="N: ")
        self.entry_N = tk.Entry(self)
        self.lbl_seed = tk.Label(self, text = "Seed: ")
        self.entry_seed = tk.Entry(self)
        self.lbl_pf = tk.Label(self, text = "Pf:")
        self.entry_pf = tk.Entry(self)
        self.btn_set = tk.Button(self, text = "SET", command=self.press_btn_set)
        self.btn_dscrd = tk.Button(self, text = "DISCARD", state=tk.DISABLED, command=self.press_btn_discard)

        self.lbl_N.grid(row=0,column=0)
        self.entry_N.grid(row=0,column=1)
        self.lbl_seed.grid(row=0,column=2)
        self.entry_seed.grid(row=0,column=3)
        self.lbl_pf.grid(row=0,column=4)
        self.entry_pf.grid(row=0,column=5)
        self.btn_set.grid(row=0,column=6)
        self.btn_dscrd.grid(row=0,column=7)

    def press_btn_set(self):
        #check if entries are ok
        entries_ok = True
        entries_ok = entries_ok and check_pos_int(self.entry_N.get())
        entries_ok = entries_ok and check_pos_int(self.entry_seed.get())
        entries_ok = entries_ok and check_pos_int(self.entry_pf.get())
        if not entries_ok:
            print("Invalid entry")
            return

        #disable entries
        self.entry_N.config(state=tk.DISABLED)
        self.entry_seed.config(state=tk.DISABLED)
        self.entry_pf.config(state=tk.DISABLED)
        self.btn_set.config(state=tk.DISABLED)
        self.btn_dscrd.config(state=tk.NORMAL)

        #spawn windows for grid and plot

    def press_btn_discard(self):
        #enable entries
        self.entry_N.config(state=tk.NORMAL)
        self.entry_seed.config(state=tk.NORMAL)
        self.entry_pf.config(state=tk.NORMAL)
        self.btn_set.config(state=tk.NORMAL)
        self.btn_dscrd.config(state=tk.DISABLED)

    def create_temperature_interface(self):
        self.label_T = tk.Label(self, text = "T: ")
        self.entry_T = FloatEntry(self, state=tk.DISABLED)
        self.label_beta = tk.Label(self, text = "beta: ")
        self.entry_beta = FloatEntry(self)

        self.label_T.grid(row = 1, column = 0)
        self.entry_T.grid(row = 1, column = 1)
        self.label_beta.grid(row = 1, column = 2)
        self.entry_beta.grid(row = 1, column = 3)

    def create_play_interface(self):
        self.btn_start = tk.Button(self, text = "START")
        self.btn_pause = tk.Button(self, text = "PAUSE")
        self.btn_therm = tk.Button(self, text = "THERM")

        self.btn_start.grid(row = 2, column = 0, columnspan = 2)
        self.btn_pause.grid(row = 2, column = 2, columnspan = 2)
        self.btn_therm.grid(row = 2, column = 4, columnspan = 2)



my_app = App()
my_app.run()
