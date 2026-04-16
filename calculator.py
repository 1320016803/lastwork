import tkinter as tk

def calc(op):
    a = int(e1.get())
    b = int(e2.get())
    if op == "+":
        res.set(a+b)
    else:
        res.set(a-b)    

root = tk.Tk()
root.title("简单计算器")
e1 = tk.Entry(root, width=5)
e2 = tk.Entry(root, width=5)
e1.pack()
e2.pack()
tk.Button(root, text="+", command=lambda: calc("+")).pack()
tk.Button(root, text="-", command=lambda: calc("-")).pack()
res = tk.StringVar()
tk.Label(root, textvariable=res).pack()
root.mainloop()
