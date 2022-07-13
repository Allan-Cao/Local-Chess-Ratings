from tkinter import *
from tkinter import messagebox
from glicko2 import Player
from tinydb import TinyDB, Query
db = TinyDB('db.json') #this is the database of all the chess players
ID = Query()
import pickle
import time
def process_match(id1,id2,result):
    if id1<len(db) and id2<len(db):
        if result == 3:
            result = 1
        elif result == 2:
            result = 0.5
        else:
            result = 0
        old_rating = db.search(ID.id == id1)[0]['rating']
        old_rd = db.search(ID.id == id1)[0]['rd']
        old_vol = db.search(ID.id == id1)[0]['vol']
        op_rating = db.search(ID.id == id2)[0]['rating']
        op_rd = db.search(ID.id == id2)[0]['rd']
        op_vol = db.search(ID.id == id2)[0]['vol']
        temp = Player(old_rating,old_rd,old_vol)
        temp.update_player([op_rating],[op_rd],[result])
        with open('Backups/'+time.strftime("%Y%m%d-%H%M%S"),'wb+') as f:
            pickle.dump(db.all(),f)
        db.update({'rating': temp.rating,'rd': temp.rd,'vol': temp.vol}, ID.id == id1)
        temp = Player(op_rating,op_rd,op_vol)
        if result == 1:
            result = 0
        elif result == 0:
            result = 1
        else:
            result = 0.5
        temp.update_player([old_rating],[old_rd],[result])
        db.update({'rating': temp.rating,'rd': temp.rd,'vol': temp.vol}, ID.id == id2)
        return True
    else:
        return False
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
def new_player():
    if messagebox.askyesno(title='Admins Only Please!', message='Are you Allan, Maxim, Tony or Wojtek?'):
        if hasNumbers(str(txt4.get())) or len(str(txt4.get())) == 0:
            messagebox.showerror(title='ADMINS ONLY!!!', message='Error! You must be an Admin!')
            txt4.delete(0, END)
#            return
        else:
            db.insert({'name': str(txt4.get()), 'rating':1500,'rd':350,'vol':0.06,'id':len(db)})
            messagebox.showinfo(title='Member Added', message='Member has been added with name %s and ID %s' % (txt4.get(),str(len(db)-1)))
            txt4.delete(0, END)
#            return
def determine_rating(getid):
    try:
        return(db.search(Query().id == int(getid))[0]['rating'])
    except:
        return(0)
def getrating():
    if int(txt3.get())<len(db):
        messagebox.showinfo(title='Rating Check', message=str(db.search(Query().id == int(txt3.get()))[0]['name'])+'\'s rating is '+str(determine_rating(int(txt3.get()))))
        txt3.delete(0, END)
    else:
        messagebox.showerror("Error!", "There was a problem processing your ID. Please try again!")
        txt3.delete(0, END)

window = Tk()
window.attributes("-fullscreen", True)
window.title("Chess Rating GUI")
selected = IntVar()
btn_list = [
'7',  '8',  '9',
'4',  '5',  '6',
'1',  '2',  '3', '0',
'Delete','Clear']
txt = None

class NumPad(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.grid()
        self.numpad_create()
    def command(self, b):
        global txt
        if b.isnumeric() and len(txt.get()) < 25:
            txt.insert(END,b)
        elif b == 'Clear':
            txt.delete(0, END)
        elif b == 'Delete':
            txt.delete(len(txt.get())-1,END)
    def numpad_create(self):
        r = 1
        c = 0
        for b in btn_list:
            cmd = lambda b=b: self.command(b)
            self.b= Button(self, text=b,bg = "#42f498",activebackground = '#fff', activeforeground = "#42f498", padx = 2, pady = 2,fg = '#fff', width=5,command=cmd).grid(row=r,column=c)
            c += 1
            if c > 2:
                c = 0
                r += 1
def reset_inputs():
    rad1.deselect()
    rad2.deselect()
    rad3.deselect()
    selected = 0
    txt1.delete(0, END)
    txt2.delete(0, END)
def clicked():
    if messagebox.askyesno(title='Rating Update Verification', message='Are you sure the information you entered is accurate?'):
        global txt
        try:
            inputs = [int(txt1.get()),int(txt2.get()),selected]
        except:
            messagebox.showerror("Whoops!", "One or more input fields empty!")
            return
        if selected == 0:
            messagebox.showerror("Whoops!", "Select a game outcome!")
            return
        if int(txt1.get()) == int(txt2.get()):
            messagebox.showerror("Whoops!", "You can't play yourself!")
            return
        if process_match(inputs[0],inputs[1],selected):
            lines = ['Rating Successfuly Updated!',
            str(db.search(Query().id == int(txt1.get()))[0]['name'])+'\'s new rating is '+str(determine_rating(int(txt1.get()))),
            str(db.search(Query().id == int(txt2.get()))[0]['name'])+'\'s new rating is '+str(determine_rating(int(txt2.get())))]
            messagebox.showinfo(title='Rating Update', message="\n".join(lines))
            reset_inputs()
        else:
            messagebox.showerror("Error!", "There was a problem processing your ID. Please try again!")
        txt1.config(text="")
        txt2.config(text='')
    else:
        return
   
numpad = NumPad(window)
numpad.grid(column=0,row=6)

lbl = Label(window, text = 'IDs Please:').grid(column=0,row=1)
lbl1 = Label(window, text = 'Player 1').grid(column=1,row=0)
lbl2 = Label(window, text = 'Player 2').grid(column=2,row=0)

txt1 = Entry(window,width=10)
txt1.grid(column=1, row=1)
txt2 = Entry(window,width=10)
txt2.grid(column=2, row=1)
txt3 = Entry(window,width=10)
txt3.grid(column=1, row=5)
txt4 = Entry(window,width=10)
txt4.grid(column=1, row=7)

rad1 = Radiobutton(window,text='Player 1 Won', value=3, variable=selected)
rad1.grid(column=0, row=2)
rad2 = Radiobutton(window,text='Draw!', value=2, variable=selected)
rad2.grid(column=1, row=2)
rad3 = Radiobutton(window,text='Player 2 Won', value=1, variable=selected)
rad3.grid(column=2, row=2) 

player = True

lb4 = Label(window, text="Rating Check")
lb4.grid(column=1, row=4)
lb4 = Label(window, text="")
lb4.grid(column=1, row=6)
btn = Button(window, text="Submit Result", command=clicked)
btn.grid(column=1, row=3)

btn3 = Button(window, text="Get Rating", command=getrating)
btn3.grid(column=2, row=5)
btn3 = Button(window, text="Add New Player", command=new_player)
btn3.grid(column=2, row=7)

def callback_entry1_focus(event):
    global txt
    txt = txt1
def callback_entry2_focus(event):
    global txt
    txt = txt2
def callback_entry3_focus(event):
    global txt
    txt = txt3
def callback_entry4_focus(event):
    global txt
    txt = txt4    
txt1.bind("<FocusIn>", callback_entry1_focus)
txt2.bind("<FocusIn>", callback_entry2_focus)
txt3.bind("<FocusIn>", callback_entry3_focus)
txt4.bind("<FocusIn>", callback_entry4_focus)

window.geometry('480x320')
window.mainloop()
