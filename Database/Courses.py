import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

course_code = course_name = course_type = None

def create_treeview():
    tree['columns'] = ('CourseCode', 'CourseName', 'CourseType')
    tree.column("#0", width=0, stretch=NO,anchor = tk.CENTER)
    tree.column("#1", width=90, stretch=NO,anchor = tk.CENTER)
    tree.column("#2", width=240, stretch=NO,anchor = tk.CENTER)
    tree.column("#3", width=85, stretch=NO,anchor = tk.CENTER)
    tree.heading('#0', text="")
    tree.heading('#1', text="Course Code")
    tree.heading('#2', text="Course Title")
    tree.heading('#3', text="Course Type")
    tree['height'] = 12

def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT COURSE_CODE, COURSE_NAME, COURSE_TYPE FROM COURSES")
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2])
        )
    tree.place(x=505, y=100)

def add_data():
    code = str(code_entry.get()).upper().strip()
    name = str(name_entry.get()).upper()
    ctype = str(type_entry.get()).capitalize()

    if code == "" or name == "" or ctype == "":
        messagebox.showwarning("Blank Field", "Some fields are empty! Please fill them out!")
        return

    conn.execute(f"REPLACE INTO COURSES (COURSE_CODE, COURSE_NAME, COURSE_TYPE) VALUES ('{code}','{name}', '{ctype}')")
    conn.commit()
    update_treeview()
    
    code_entry.delete(0, END)
    name_entry.delete(0, END)
    type_entry.delete(0, END)

def update_data():
    code_entry.delete(0, END)
    name_entry.delete(0, END)
    type_entry.delete(0, END)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Selection Error", "Select one course at a time to update!")
            return

        selected_course = tree.item(tree.selection()[0])['values']
        code_entry.insert(0, selected_course[0])
        name_entry.insert(0, selected_course[1])
        type_entry.insert(0, selected_course[2])
        
        conn.execute(f"DELETE FROM COURSES WHERE COURSE_CODE = '{selected_course[0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Selection Error", "Please select a course from the list first!")
        return

def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Selection Error", "Please select a course from the list first!")
        return
    for i in tree.selection():
        conn.execute(f"DELETE FROM COURSES WHERE COURSE_CODE = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()

conn = sqlite3.connect('Database/Database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS COURSES (
        COURSE_CODE CHAR(10) PRIMARY KEY,
        COURSE_NAME CHAR(50) NOT NULL,
        COURSE_TYPE CHAR(50) NOT NULL
    )
''')

root = CTk()
root.geometry('1000x480+180+120')
root.title('Courses Management')

full_frame = CTkFrame(
    root,
    width=1000, 
    height=480,
    fg_color = '#ebebeb',
    bg_color="#ebebeb"
)
full_frame.pack()

CTkLabel(
    master = full_frame,
    text='List of Courses',
    font=('Consolas', 28, 'bold')
).place(x=600, y=50)

CTkLabel(
    master = full_frame,
    text='Add or Update Courses',
    font=('Consolas', 28, 'bold')
).place(x=120, y=50)

CTkLabel(
    master = full_frame,
    text='Fill Up The Following Information',
    font=('Consolas', 14, 'italic'),
    pady=5
).place(x=145, y=80)

CTkLabel(
    master = full_frame,
    text='Course Code : ',
    font=('Consolas', 16)
).place(x=100, y=130)

code_entry = CTkEntry(
    master = full_frame,
    font=('Consolas', 16),
    width=240    
)
code_entry.place(x=230, y=130)

CTkLabel(
    master = full_frame,
    text='Course Name : ',
    font=('Consolas', 16)
).place(x=100, y=170)

name_entry = CTkEntry(
    master = full_frame,
    font=('Consolas', 16),
    width=240
)
name_entry.place(x=230, y=170)

CTkLabel(
    master = full_frame,
    text='Course Type : ',
    font=('Consolas', 16)
).place(x=100, y=210)

type_entry = CTkEntry(
    master = full_frame,
    font=('Consolas', 16),
    width=240
)
type_entry.place(x=230, y=210)

# Button 1
B1 = CTkButton(
    master = full_frame,
    text='Add Course',
    text_color='black',
    border_color= 'black',
    border_width=1.2,
    font = ('consolas', 16 ,'bold'),
    command=add_data,
    height=40,
    width = 160,
    fg_color = '#40f507',
    hover_color = '#46C263',
)
B1.place(x=140,y=400)

# Button2
B2 =CTkButton(
    master = full_frame,
    text='Update Course',
    font = ('consolas', 16 ,'bold'),
    command=update_data,
    text_color='black',
    border_color= 'black',
    border_width=1.2,
    height=40,
    width = 160
    # fg_color = 'yellow'
)
B2.place(x=420,y=400)


tree = ttk.Treeview(master = full_frame)
create_treeview()
update_treeview()

# Button3
B3 = CTkButton(
    master = full_frame,
    text='Delete Course',
    command=remove_data,
    font = ('consolas', 16 ,'bold'),
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

