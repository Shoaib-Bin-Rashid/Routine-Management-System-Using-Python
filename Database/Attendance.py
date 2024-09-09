import sqlite3
from customtkinter import *
from tkinter import ttk
import tkinter as tk

course_code = 'None'
tree = None



def create_treeview():
    global tree 
    tree = ttk.Treeview(root)
    tree['columns'] = ('SID', 'Name', 'Roll', 'Section', 'Total Class', 'Present', 'Percentage')
    tree.column("#0", width=0, stretch=NO, anchor=tk.CENTER)
    tree.column("#1", width=80, stretch=NO, anchor=tk.CENTER)
    tree.column("#2", width=200, stretch=NO, anchor=tk.CENTER)
    tree.column("#3", width=100, stretch=NO, anchor=tk.CENTER)
    tree.column("#4", width=100, stretch=NO, anchor=tk.CENTER)
    tree.column("#5", width=100, stretch=NO, anchor=tk.CENTER)
    tree.column("#6", width=100, stretch=NO, anchor=tk.CENTER)
    tree.column("#7", width=120, stretch=NO, anchor=tk.CENTER)
    tree.heading('#0', text="")
    tree.heading('#1', text="SID")
    tree.heading('#2', text="Name")
    tree.heading('#3', text="Roll")
    tree.heading('#4', text="Section")   
    tree.heading('#5', text="Total Class")   
    tree.heading('#6', text="Present")   
    tree.heading('#7', text="Percentage (%)")   
    tree['height'] = 16

def update_treeview():
    global course_code
    if tree is None:
        print("Tree is none")
        return 
    for row in tree.get_children():
        tree.delete(row)
    print("Selected Course Code:", course_code)
    cursor = conn.execute("""
            SELECT SID, NAME, ROLL, SECTION, TOTAL_CLASS, PRESENT, PERSENTAGE
            FROM ATTENDANCE
            WHERE COURSE_CODE = ?
        """, (course_code,))

    details = cursor.fetchall()
    for row in details:
        tree.insert("", 0, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        print(row[0], row[1], row[2], row[3],row[4],row[5],row[6])
    tree.pack(padx=10)


def select_crs(event=None):
    global course_code
    course_code = str(dropdown.get())
    print("Droppdown course code: " + course_code)
    # update_table()
    update_treeview()

def update_table():
    cursor.execute("""SELECT DISTINCT COURSE_CODE FROM COURSES""")
    courses = [row[0] for row in cursor]

    for course in courses:
        cursor.execute("""
            SELECT SID, NAME, ROLL, SECTION FROM STUDENT
        """)
        students = cursor.fetchall()

        for student in students:
            sid, name, roll, section = student
            cursor.execute("""
                INSERT OR IGNORE INTO ATTENDANCE (SID, NAME, ROLL, COURSE_CODE, SECTION, TOTAL_CLASS, PRESENT, PERSENTAGE)
                VALUES (?, ?, ?, ?, ?, 0, 0, 0)
            """, (sid, name, roll, course, section))
    conn.commit()



conn = sqlite3.connect(r'Database/Database.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS ATTENDANCE(
    SID TEXT,
    NAME TEXT,
    ROLL INTEGER,
    COURSE_CODE TEXT,
    SECTION TEXT, 
    TOTAL_CLASS INTEGER,
    PRESENT INTEGER,
    PERSENTAGE REAL,
    UNIQUE(SID, COURSE_CODE, SECTION)  
)
""")

    
cursor.execute("SELECT DISTINCT COURSE_CODE FROM COURSES")
courses = [row[0] for row in cursor]


root = CTk()
root.title("Student Attendance")
root.geometry('1000x480+180+120')

title_label = CTkLabel(
    root,
    text="Students Attendance List",
    font=('Consolas', 28, 'bold'),
    text_color='#a96c53',
    pady=20,
)
title_label.pack()

tree = ttk.Treeview(root)
create_treeview()
update_treeview()

crs_select_f = CTkFrame(root, corner_radius=0)
crs_select_f.pack(pady=15)

CTkLabel(
    crs_select_f,
    text='Select Course :',
    font=('Consolas', 16, 'bold'),
    padx=10,
    # fg_color='#ededed'
).grid(row=1, column=1)

dropdown = ttk.Combobox(
    crs_select_f, 
    values=courses
)
dropdown.grid(row=1, column=2)
dropdown.current(0)


dropdown.bind("<<ComboboxSelected>>", select_crs)
select_crs()


root.mainloop()
