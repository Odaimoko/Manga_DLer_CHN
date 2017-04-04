from tkinter import *
from tkinter import ttk

root = Tk()
root.title ("doda")
l  = Listbox(root, height=5,selectmode="extended")
l2 = Listbox(root, height=5,borderwidth="0")
l.grid(column=0, row=0, sticky=(N, W, E, S))
l2.grid(column=1, row=0, sticky=(N, W, E, S))
# l2.bindtags((l2,root,"all"))
def bv(*args):
	l.yview(*args)
	l2.yview(*args)


s = ttk.Scrollbar(root, orient=VERTICAL, command=bv)
s.grid(column=2, row=0, sticky=(N, S))
l['yscrollcommand'] = s.set
l2['yscrollcommand'] = s.set


def setall(*args):
	s.set(*args)
	l2.yview_moveto(args[0])
	l.yview_moveto(args[0])


l['yscrollcommand'] = setall
l2['yscrollcommand'] = setall
ttk.Sizegrip().grid(column=99, row=91, sticky=(W, E))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
for i in range(1, 101):
	l.insert('end', 'Line %d of 100' % i)
	l2.insert('end', 'Line %d of 100' % i)

tree = ttk.Treeview(root)
# Inserted at the root, program chooses id:
tree.insert('', 'end', 'widgets', text='Widget Tour')

# Same thing, but inserted as first child:
tree.insert('', 0, 'app', text='Applications')

# Treeview chooses the id:
id = tree.insert('', 'end', text='Tutorial')
tree.insert(id, 'end', text='Tree')
# Inserted underneath an existing node:
tree.insert('widgets', 'end', text='Canvas')
tree.grid(column=3)
tree.move('widgets', id, 'end')  # move widgets under gallery
print(tree.item("app"))

tree['columns'] = ('size', 'modified', 'owner')
tree.column('size', anchor='center')
tree.heading('size', text='Size')
tree.set('widgets', 'size', '12KB')
size = tree.set('widgets', 'size')
tree.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))

def setsize():
	import  time
	while True:
		time.sleep(.5)
		tree.set('app','size',str(time.clock()))
import threading
threading.Thread(target=setsize).start()
root.mainloop()
