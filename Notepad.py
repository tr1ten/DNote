try:
    from tkinter import *
    import tkinter.messagebox as tsg
    import tkinter.filedialog as fg
    import tkinter.simpledialog as sd
    from tkinter import ttk
except Exception:
    raise ImportError('Install tkinter module ')

class Notepad(object):
    def __init__(self, parent):
        self.root = parent
        self.filename = ''

        self.root.geometry('600x500')
        self.root.title("Notepad")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Horizontal.TScrollbar", gripcount=0,
                        background="Green", darkcolor="DarkGreen", lightcolor="LightGreen",
                        troughcolor="gray", bordercolor="blue", arrowcolor="white")

        scroll = ttk.Scrollbar(self.root)
        scroll.pack(fill=Y, side=RIGHT)
        self.text = Text(self.root, bg='gray11', yscrollcommand=scroll.set, width=600, height=500, fg='white', undo=True,
                    autoseparators=True, maxundo=-1)
        self.text.pack(fill=BOTH)
        self.text.config(insertbackground='green')
        scroll.config(command=self.text.yview)
        self.root.protocol('WM_DELETE_WINDOW', self.closing)
        self.text.bind('<Double-Button-1>', lambda event: self.text.tag_remove('find', 1.0, END))
        imag = PhotoImage(file='assets/file.png')
        imag1 = PhotoImage(file='assets/fol1.png')
        mainmenu = Menu(root, bg='white', activebackground='royalblue1', font='opensans 9 underline')

        imag2 = PhotoImage(file='assets/save1.png')
        imag3 = PhotoImage(file='assets/ex.png')

        m1 = Menu(mainmenu, tearoff=0, activebackground='royalblue1', bg='gray20', fg='white')
        m1.add_command(label='    New File..     ', command=self.new, image=imag, compound='left')
        m1.add_command(label='    Open..     ', command=self.op, image=imag1, compound='left')
        m1.add_separator()
        m1.add_command(label='     Save', command=self.saving, image=imag2, compound='left')
        m1.add_command(label='         Save as..', command=self.saveas)
        m1.add_separator()
        m1.add_command(label='Exit', command=self.closing, image=imag3, compound='left')

        mainmenu.add_cascade(label='File', menu=m1)
        m2 = Menu(mainmenu, tearoff=0, bg='gray20', fg='white', activebackground='royalblue1')
        m2.add_command(label='Undo         Ctrl + Z', command=self.undo)
        m2.add_command(label='Redo        Shift + Ctrl + Z', command=self.redo)
        m2.add_separator()
        m2.add_command(label='Find', command=lambda: self.find(sd.askstring('Find', 'Which Word to Find')))
        m2.add_command(label='Clear', command=self.clear)

        self.root.config(menu=mainmenu)

        mainmenu.add_cascade(label='Edit', menu=m2)

        m3 = Menu(mainmenu, tearoff=0, bg='gray20', fg='white', activebackground='royalblue1')
        m3.add_command(label='    Owner   ', command=self.msg)
        m3.add_command(label='    Rate us    ', command=self.rate)

        mainmenu.add_cascade(label='Info', menu=m3)

        self.root.mainloop()

    def closing(self):

        if len(self.text.get(1.0, END)) != 1:

            s = tsg.askyesnocancel('Closing Notepad', 'Want to save')
            if s:
                self.saveas()

        self.root.destroy()

    def find(self, query):
        if query is None:
            return 0
        
        self.check()
        c = '.'
        start = 1.0
        txt = self.text.get(1.0, END)
        for i in range(txt.count(query)):

            line = (self.text.search(query, start, END))

            self.text.tag_add('find', float(line))
            self.text.tag_config('find', background='yellow', foreground='green')

            a, s = line.split('.')
            ss = str(int(s) + 1)
            start = (a + c + ss)

    def clear(self):
        self.text.delete(1.0, END)

    def new(self):
        self.clear()

        self.filename = fg.asksaveasfilename(title='Name of file')
        try:
            self.filename = self.filename.split('/')
            self.filename = self.filename[len(self.filename) - 1]
        except Exception:
            pass

    def op(self):
        self.clear()

        fn = fg.askopenfilename()
        try:
            self.filename = open(fn, 'r')
            for ttt in self.filename.read():
                self.text.insert(END, ttt)
            self.filename.close()
            self.filename = open(fn, 'w')
        except Exception:
            print('Error in opening')

    def check(self):

        if len(self.text.get(1.0, END)) == 1:
            tsg.showerror('Error occured', 'No Text found')

    def undo(self):
        self.text.edit_undo()

    def redo(self):
        self.text.edit_redo()

    def saveas(self):
        self.filename = fg.asksaveasfile()
        self.filename.writelines(self.text.get(1.0, END))
        
        self.filename.close()

    def saving(self):

        try:

            self.filename.write(self.text.get(1.0, END))



        except Exception:
            try:
                self.filename = open(self.filename, 'w+')
                self.saving()
            except Exception:
                pass

    def msg(self):
        tsg.showinfo('Owner', 'Made by Tr1ten')

    def rate(self):
        a = tsg.askyesnocancel('Rate it', 'Do You Like our app')

        if a:
            tsg.askokcancel('Rate me', 'Rate us on playstore')

        else:
            tsg.askokcancel('Sorry', 'Please mail us if u facing any problem')
        

if __name__ == '__main__' :
    root = Tk()
    notepad = Notepad(root)
