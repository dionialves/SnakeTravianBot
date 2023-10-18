import tkinter as tk

"""
root = tk.Tk()
S = tk.Scrollbar(root)
T = tk.Text(root, bg = 'black', fg='white', height=20, width=80)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.LEFT, fill=tk.Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = "teste"
T.insert(tk.END, quote)
tk.mainloop()"""


class OutputMenssage(tk.Text):
    def __init__(self, **kwargs):
        kwargs['fg'] = 'white'
        kwargs['bg'] = 'black'
        super().__init__(**kwargs)

message = OutputMenssage()
message.insert(tk.END, "texte")
message.mainloop()