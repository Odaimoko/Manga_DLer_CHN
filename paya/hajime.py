#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk


def calculate(*args):
	try:
		print(cb.get(), cb.current(2))
		s.configure('TButton', font='helvetica 24')

		value = float(feet.get())
		meters.set((0.3048 * value * 10000.0 + 0.5) / 10000.0)
	except ValueError:
		pass


root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12", borderwidth=10, relief="sunken")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=2)
mainframe.rowconfigure(1, weight=5)
mainframe.rowconfigure(2, weight=3)
mainframe.rowconfigure(3, weight=7)
feet = StringVar()
meters = StringVar()
cbbox = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))
# feet_entry.state(["disabled"])
# feet_entry.columnconfigure(0,weight=1)
# feet_entry.rowconfigure(0,weight=4)
mitoru = ttk.Label(mainframe, textvariable=meters, width=10)
mitoru.grid(column=2, row=2, sticky=(W, E))
# mitoru.columnconfigure(1,weight=3)
# mitoru.rowconfigure(1,weight=2)

btn = ttk.Button(mainframe, text="Calculate", command=calculate, default="active")
btn.grid(column=3, row=3, sticky=E)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)

p = ttk.Progressbar(mainframe,length=200)
p.grid(column=1,row=2)
ttk.Label(mainframe, text="is equivalent to", foreground="red", background="yellow", relief="sunken"). \
	grid(column=1, row=2, sticky=(E, W))
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

cb = ttk.Combobox(mainframe)
cb['values'] = ('USA', 'Canada', 'Australia')
cb.bind("<<ComboboxSelected>>", calculate)
for child in mainframe.winfo_children(): child.grid_configure(padx=0, pady=0)

feet_entry.focus()


menubar = Menu()
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='可是ile', underline="2")
menubar.add_cascade(menu=menu_edit, label='Edit', underline="3")
menu_file.add_cascade(menu=menu_edit, label="jiliguala")
check = StringVar()
menu_file.add_checkbutton(label='Check', variable=check, onvalue=1, offvalue=0)
radio = StringVar()
menu_file.add_radiobutton(label='One', variable=radio, value=1)
menu_file.add_radiobutton(label='Two', variable=radio, value=2)

root['menu'] = menubar
l = Listbox(mainframe, height=5)
l.bind("<Enter>",calculate)
l.grid(column=0, row=0, sticky=(N,W,E,S))
s = ttk.Scrollbar(mainframe, orient=VERTICAL, command=l.yview)
s.grid(column=1, row=0, sticky=(W,N,S))
l['yscrollcommand'] = s.set
ttk.Sizegrip().grid(column=1, row=1, sticky=(S,E))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
for i in range(1,101):
    l.insert('end', 'Line %d of 100' % i)
root.mainloop()

