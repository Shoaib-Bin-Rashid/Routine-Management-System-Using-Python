import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
sid = Pass = conf_pass = name = roll = section = None


def create_treeview():
    tree['columns'] = ('SID', 'Pass', 'Name', 'Roll', 'Section')
    tree.column("#0", width=0, stretch=NO, anchor = tk.CENTER)
    tree.column("#1", width=50, stretch=NO, anchor = tk.CENTER)
    tree.column("#2", width=70, stretch=NO, anchor = tk.CENTER)
    tree.column("#3", width=180, stretch=NO, anchor = tk.CENTER)
    tree.column("#4", width=70, stretch=NO, anchor = tk.CENTER)
    tree.column("#5", width=50, stretch=NO, anchor = tk.CENTER)
    tree.heading('#0', text="")
    tree.heading('#1', text="SID")
    tree.heading('#2', text="Pass")
    tree.heading('#3', text="Name")
    tree.heading('#4', text="Roll")
    tree.heading('#5', text="Section")
    tree['height']= 12


def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT SID,PASS, NAME, ROLL, SECTION FROM STUDENT")
    for row in cursor:
        tree.insert("", 0, values=(row[0], row[1], row[2], row[3], row[4]))
    tree.place(x=510, y=100)


def add_data():
    sid = str(sid_entry.get())
    Pass = str(pass_entry.get())
    conf_pass = str(conf_pass_entry.get())
    name = str(name_entry.get()).upper()
    roll = str(roll_entry.get())
    section = str(sec_entry.get()).upper()

    if sid == "" or Pass == "" or conf_pass == "" or name == "" or roll == "" or section == "":
        messagebox.showwarning("Blank Field", "Some fields are empty! Please fill them out!")
        return

    if Pass != conf_pass:
        messagebox.showerror("Passwords mismatch", "Password did not match. Try again!")
        pass_entry.delete(0, END)
        conf_pass_entry.delete(0, END)
        return

    conn.execute(f"REPLACE INTO STUDENT (SID, PASS, NAME, ROLL, SECTION) VALUES ('{sid}','{Pass}','{name}', '{roll}', '{section}')")
    conn.commit()
    update_treeview()

    sid_entry.delete(0, END)
    pass_entry.delete(0, END)
    conf_pass_entry.delete(0, END)
    name_entry.delete(0, END)
    roll_entry.delete(0, END)
    sec_entry.delete(0, END)


def update_data():
    sid_entry.delete(0, END)
    pass_entry.delete(0, END)
    conf_pass_entry.delete(0, END)
    name_entry.delete(0, END)
    roll_entry.delete(0, END)
    sec_entry.delete(0, END)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Selection Error", "Select one student at a time to update!")
            return

        tree_sid = tree.item(tree.selection()[0])['values'][0]
        cursor = conn.execute(f"SELECT * FROM STUDENT WHERE SID = '{tree_sid}'")

        cursor = list(cursor)
        sid_entry.insert(0, cursor[0][0])
        pass_entry.insert(0, cursor[0][1])
        conf_pass_entry.insert(0, cursor[0][1])
        name_entry.insert(0, cursor[0][2])
        roll_entry.insert(0, cursor[0][3])
        sec_entry.insert(0, cursor[0][4])

        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{cursor[0][0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Selection Error", "Please select a student from the list first!")
        return


def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Selection Error", "Please select a student from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM STUDENT WHERE SID = '{tree.item(i)['values'][0]}'")
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




conn = sqlite3.connect('Database\\Database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS STUDENT (
                    SID CHAR(10) PRIMARY KEY,
                    PASS CHAR(50) NOT NULL,
                    NAME CHAR(50) NOT NULL,
                    ROLL INTEGER NOT NULL,
                    SECTION CHAR(5) NOT NULL
                )''')

root = CTk()
root.geometry('1000x480+180+120')
root.title('Students')
full_frame = CTkFrame(
    root,
    width=1000, 
    height=480,
    fg_color = '#ebebeb',
    bg_color="#ebebeb"
)
full_frame.pack()
# Label1
Label1 = CTkLabel(
    master=full_frame,
    text='List of Students',
    font=('Consolas', 28, 'bold'),
)
Label1.place(x=600, y=50)

# Label2
Label2 = CTkLabel(
    master=full_frame,
    text='Add or Update Students',
    font=('Consolas', 28, 'bold')
)
Label2.place(x=120, y=50)

# Label3
Label3 = CTkLabel(
    master=full_frame,
    text='Fill Up The Following Informations',
    font=('Consolas', 14, 'italic')
)
Label3.place(x=150, y=85)

# Label4
Label4 = CTkLabel(
    master=full_frame,
    text='Student id:',
    font=('Consolas', 15)
)
Label4.place(x=75, y=130)

# Entry1
sid_entry = CTkEntry(
    master=full_frame,
    font=('Consolas', 15),
    height=25 ,
    width = 200
)
sid_entry.place(x=215, y=130)

# Label5
Label5 = CTkLabel(
    master=full_frame,
    text='Password:',
    font=('Consolas', 15)
)
Label5.place(x=75, y=170)

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
    height=26,
    width = 80
)
show_hide.place(x=422, y=170)

# Label6
Label6 = CTkLabel(
    master=full_frame,
    text='Confirm Password:',
    font=('Consolas', 15)
)
Label6.place(x=75, y=210)

# Entry 3 
conf_pass_entry = CTkEntry(
    full_frame,
    font=('Consolas', 12),
    height=25 ,
    width = 200,
    show="*"
)
conf_pass_entry.place(x=215, y=210)

    # SHOW Button 1
show_hide2 = CTkButton(
    full_frame,
    text="Show",
    command=show_conf_pass,
    font = ('consolas', 14 ,'bold'),
    height=26,
    width = 80
)
show_hide2.place(x=422,y=208)


# Label7
Label7 = CTkLabel(
    full_frame,
    text='Student Name:',
    font=('Consolas', 15)
).place(x=75, y=250)

# Entry4
name_entry = CTkEntry(
    full_frame,
    font=('Consolas', 15),
    height=25 ,
    width = 200
)
name_entry.place(x=215, y=250)

# Label8
Label8 = CTkLabel(
    full_frame,
    text='Roll no.:',
    font=('Consolas', 15)
).place(x=75, y=290)

# Entry5
roll_entry = CTkEntry(
    full_frame,
    font=('Consolas', 15),
    height=25 ,
    width = 200
)
roll_entry.place(x=215, y=290)

# Label9
Label9 = CTkLabel(
    full_frame,
    text='Section:',
    font=('Consolas', 15)
).place(x=75, y=330)

# Entry6
sec_entry = CTkEntry(
    full_frame,
    font=('Consolas', 15),
    height=25 ,
    width = 200
)
sec_entry.place(x=215, y=330)


B1 = CTkButton(
    full_frame,
    text='Add Student',
    text_color='black',
    border_color= 'black',
    border_width=1.2,
    font = ('consolas', 15 ,'bold'),
    command=add_data,
    height=40,
    width = 160,
    fg_color = '#40f507',
    hover_color = '#46C263',
)
B1.place(x=140,y=400)

# Button2
B2 =CTkButton(
    full_frame,
    text='Update Student',
    font = ('consolas', 15 ,'bold'),
    command=update_data,
    text_color='black',
    border_color= 'black',
    border_width=1.2,
    height=40,
    width = 160
    # fg_color = 'yellow'
)
B2.place(x=420,y=400)


tree = ttk.Treeview(full_frame)
create_treeview()
update_treeview()

# Button3
B3 = CTkButton(
    full_frame,
    text='Delete Student',
    command=remove_data,
    font = ('consolas', 15 ,'bold'),
    text_color='black',
    border_color= 'black',
    border_width=1.2,
    height=40,
    width = 160,
    fg_color = '#FC3D39',
    hover_color = '#E33437'
)
B3.place(x=700,y=400)

root.mainloop()
conn.close() 

