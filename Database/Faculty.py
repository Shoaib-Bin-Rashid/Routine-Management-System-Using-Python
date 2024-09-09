import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk 

sid = Pass = conf_pass = name = roll = section = None

def create_treeview():
    tree['columns'] = ('FID', 'Pass', 'Name', 'Course1', 'Course2')
    tree.column("#0", width=0, stretch=NO,anchor = tk.CENTER)
    tree.column("#1", width=50, stretch=NO,anchor = tk.CENTER)
    tree.column("#2", width=50, stretch=NO,anchor = tk.CENTER)
    tree.column("#3", width=220, stretch=NO,anchor = tk.CENTER)
    tree.column("#4", width=60, stretch=NO,anchor = tk.CENTER)
    tree.column("#5", width=60, stretch=NO,anchor = tk.CENTER)
    tree.heading('#0', text="")
    tree.heading('#1', text="FID")
    tree.heading('#2', text="Pass")
    tree.heading('#3', text="Name")
    tree.heading('#4', text="Course 1")
    tree.heading('#5', text="Course 2")
    tree['height'] = 12

def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT FID, PASS, NAME, COURSE1 ,COURSE2 FROM FACULTY")
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2], row[3],row[4])
        )
    tree.place(x=510, y=100)

def add_data():
    fid = str(fid_entry.get())
    Pass = str(pass_entry.get())
    conf_pass = str(conf_pass_entry.get())
    name = str(name_entry.get()).upper()
    Course1 = str(crs1_entry.get()).upper()
    Course2 = str(crs2_entry.get()).upper()

    if fid == "" or Pass == "" or conf_pass == "" or name == "" or Course1 == "" :
        messagebox.showwarning("Blank Field", "Some fields are empty! Please fill them out!")
        return

    if Pass != conf_pass:
        messagebox.showerror("Passwords mismatch", "Password did not match. Try again!")
        pass_entry.delete(0, END)
        conf_pass_entry.delete(0, END)
        return
  

    conn.execute(f"REPLACE INTO FACULTY (FID, PASS, NAME, COURSE1, COURSE2) "
                 f"VALUES ('{fid}', '{Pass}', '{name}', '{Course1}', '{Course2}')")
    conn.commit()
    update_treeview()
    
    fid_entry.delete(0, END)
    pass_entry.delete(0, END)
    conf_pass_entry.delete(0, END)
    name_entry.delete(0, END)
    crs1_entry.delete(0, END)
    crs2_entry.delete(0, END)

def update_data():
    fid_entry.delete(0, END)
    pass_entry.delete(0, END)
    conf_pass_entry.delete(0, END)
    name_entry.delete(0, END)
    crs1_entry.delete(0, END)
    crs2_entry.delete(0, END)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Selection Error", "Select one faculty member at a time to update!")
            return

        tree_fid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM FACULTY WHERE FID = '{tree_fid}'")

        cursor = list(cursor)
        fid_entry.insert(0, cursor[0][0])
        pass_entry.insert(0, cursor[0][1])
        conf_pass_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        crs1_entry.insert(0, cursor[0][3])
        crs2_entry.insert(0, cursor[0][4])
        
        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Selection Error", "Please select a faculty member from the list first!")
        return

def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Selection Error", "Please select a faculty member from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM FACULTY WHERE FID = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()

def show_pass():
    if pass_entry.cget("show") == "":
        pass_entry.configure(show="*")
        show_hide.configure(text="Show")
    else:
        pass_entry.configure(show="") 
        show_hide.configure(text="Hide")


def show_conf_pass():
    if conf_pass_entry.cget("show") == "":
        conf_pass_entry.configure(show="*")
        show_hide2.configure(text="Show")
    else:
        conf_pass_entry.configure(show="") 
        show_hide2.configure(text="Hide")


conn = sqlite3.connect('Database/Database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS FACULTY (
        FID CHAR(10) PRIMARY KEY,
        PASS CHAR(50) NOT NULL,
        NAME CHAR(50) NOT NULL,
        COURSE1 CHAR(50) NOT NULL,
        COURSE2 CHAR(50) NOT NULL
    )
''')

root = CTk()
root.geometry('1000x480+180+120')
root.title('Faculty Members')

full_frame = CTkFrame(
    root,
    width=1000, 
    height=480,
    fg_color = '#ebebeb',
    bg_color="#ebebeb"
)
full_frame.pack()

CTkLabel(
    full_frame,
    text='List of Faculty Members',
    font=('Consolas', 26, 'bold')
).place(x=540, y=50)

CTkLabel(
    full_frame,
    text='Add/Update Faculty Members',
    font=('Consolas', 26, 'bold')
).place(x=100, y=50)

CTkLabel(
    full_frame,
    text='Fill Up The Following Information',
    font=('Consolas', 14, 'italic'),
    pady = 5
).place(x=158, y=75)

# Label 1
CTkLabel(
    full_frame,
    text='Faculty ID:',
    font=('Consolas', 15)
).place(x=75, y=130)

# Entry 1
fid_entry = CTkEntry(
    master=full_frame,
    font=('Consolas', 15),
    height=25 ,
    width = 200  
)
fid_entry.place(x=215, y=130)

# Label 2
CTkLabel(
    full_frame,
    text='Password:',
    font=('Consolas', 15)
).place(x=75, y=170)

# Entry 2
pass_entry = CTkEntry(
    master=full_frame,
    font=('consolas', 15),
    show="*",
    height=25 ,
    width = 200
)
pass_entry.place(x=215, y=170)

# SHOW Button 1
show_hide = CTkButton(
    master=full_frame,
    text="Show",
    command=show_pass,
    font = ('consolas', 14 ,'bold'),
    height=25,
    width = 80
)
show_hide.place(x=422, y=170)


# Label 3
CTkLabel(
    full_frame,
    text='Confirm Password:',
    font=('Consolas', 15)
).place(x=75, y=210)

    # Entry 3 
conf_pass_entry = CTkEntry(
    full_frame,
    font=('Consolas', 12),
    height=25 ,
    width = 200,
    show="*"
)
conf_pass_entry.place(x=215, y=210)

# SHOW Button 2
show_hide2 = CTkButton(
    full_frame,
    text="Show",
    command=show_conf_pass,
    font = ('consolas', 14 ,'bold'),
    height=25,
    width = 80
)
show_hide2.place(x=422,y=210)

CTkLabel(
    full_frame,
    text='Faculty Name:',
    font=('Consolas', 15),
).place(x=75,y = 248)


name_entry = CTkEntry(
    full_frame,
    font=('Consolas', 15),
    height=25,
    width = 200,
)
name_entry.place(x=215, y=250)

CTkLabel(
    full_frame,
    text='Course 1 Code:',
    font=('Consolas', 15)
).place(x=75, y=290)

crs1_entry = CTkEntry(
    full_frame,
    font=('Consolas', 15),
    height=25,
    width=200
)
crs1_entry.place(x=215, y=290)

CTkLabel(
    full_frame,
    text='Course 2 Code:',
    font=('Consolas', 15)
).place(x=75, y=330)

crs2_entry = CTkEntry(
    full_frame,
    font=('Consolas', 15),
    height=25,
    width=200
)
crs2_entry.place(x=215, y=330)

B1 = CTkButton(
    full_frame,
    text='Add Faculty Member',
    text_color='black',
    border_color= 'black',
    border_width=1.2,
    font = ('consolas', 15 ,'bold'),
    command=add_data,
    height=40,
    width = 200,
    fg_color = '#40f507',
    hover_color = '#46C263',
)
B1.place(x=120,y=395)

# Button2
B2 =CTkButton(
    full_frame,
    text='Update Faculty Member',
    font = ('consolas', 15 ,'bold'),
    command=update_data,
    text_color='black',
    border_color= 'black',
    border_width=1.2,
    height=40,
    width = 200
    # fg_color = 'yellow'
)
B2.place(x=400,y=395)


tree = ttk.Treeview(full_frame)
create_treeview()
update_treeview()

# Button3
B3 = CTkButton(
    full_frame,
    text='Delete Faculty Member',
    command=remove_data,
    font = ('consolas', 15 ,'bold'),
    text_color='black',
    border_color= 'black',
    border_width=1.2,
    height=40,
    width = 200,
    fg_color = '#FC3D39',
    hover_color = '#E33437'
)
B3.place(x=700,y=395)

root.mainloop()
conn.close() 