import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk 
import datetime

days = 5
periods = 9
section = None
sid = None
butt_grid = []


day_names = [ 'Saturday', 'Sunday','Monday', 'Tuesday', 'Wednesday']
period_time = ['8:00-8:50','8:50-9:40','9:40-10:30','10:50-11:40','11:40-12:30','12:30-1:20','2:30-3:20','3:20-4:10','4:10-5:00']


    

def student_routine(root,sec,sid):

    global butt_grid
    global section
    section = sec
    # print(section)
    table = CTkFrame(
        root,
        corner_radius=0,
        fg_color = '#5783db'

    )
    table.pack()

    daytime_frame = CTkFrame(
    master=table,
    border_width=1,
    border_color='black',
    fg_color='#5783db',  
    corner_radius=0  
    )
    daytime_frame.grid(row=0, column=0)  

    label = CTkLabel(
    master=daytime_frame,
    text="DAY\\TIME",
    font=('Consolas', 16, 'bold'),
    #   fg_color='#a96c53',
    fg_color='#334357',
    text_color='white',
    width= 98,
    height= 60,
    )
    label.pack(padx=1, pady=1)
    for i in range(days):
        label_border = CTkFrame(
            master=table,
            # fg_color='#5783db', 
            border_width= 1,
            border_color='black',
            corner_radius = 0,
        ) 
        label_border.grid(row=i+1, column=0)

        label_border.configure(fg_color='#334357')


        b = CTkLabel(
            label_border,
            text=day_names[i],
            font=('Consolas', 16, 'bold'),
            width=98,
            height=60,
            text_color= 'white'
        )
        b.pack(padx = 1, pady = 1)

    for i in range(periods):
        label_border = CTkFrame(
            master=table,
            border_width= 1,
            border_color='black',
            corner_radius = 0,
        ) 
        label_border.grid(row=0, column=i+1)

        label_border.configure(fg_color='#334357')

        b = CTkLabel(
            label_border,
            text=period_time[i],
            font=('Consolas', 15, 'bold'),
            width=98,
            height=60,
            text_color='white'
        )
        b.pack(padx = 1, pady = 1)


    for i in range(days):
        b = []
        for j in range(periods):
            border_frame = CTkFrame(
                master=table,
                fg_color='#F1F1F1', 
                border_width= 1,
                border_color='black',
                corner_radius = 0,
            ) 
            border_frame.grid(row=i+1, column=j+1)

        
            bb = CTkButton(
            master=border_frame,
            text='',
            font=('Consolas', 14,'bold'),
            width=98,
            height=60,
            corner_radius=0,
            fg_color='#F1F1F1',
            hover_color='#bfbfbf',
            text_color='black',
            command=lambda x = i, y = j ,z=sec , s=sid: process_button(x, y, z, s)
            )
            bb.pack(padx=1, pady=1) 
            b.append(bb)

        butt_grid.append(b)
        b = []

    update_table(section)




def process_button(d, p ,sec,sid):
    details = CTk()
    details.geometry("1000x480+180+120")

    full_frame = CTkFrame(
    details,
    width=1000, 
    height=410,
    fg_color = '#ebebeb',
    bg_color="#ebebeb"
    )
    full_frame.pack()
    
    global section
    sec = section

    id = str(sec)+str(d)+str(p)
    conn = sqlite3.connect('Database\\Database.db')
    cursor = conn.execute(f"SELECT COURSE_CODE, FID FROM ROUTINE\
                WHERE ID='{id}'")
    row = cursor.fetchone()
    print(id,row)
    if row is not None:
        print("Details found")
        crs_code,fid = row

        cur1 = conn.execute(f"SELECT COURSE_NAME, COURSE_TYPE FROM COURSES\
            WHERE COURSE_CODE='{crs_code}'")
        row1 = cur1.fetchone()
        course_name , course_type = row1

        cur2 = conn.execute(f"SELECT NAME FROM FACULTY\
            WHERE FID='{fid}'")
        row2 = cur2.fetchone()
        fname = row2[0]
    else:
        print("Details Not found")
        crs_code = fid = course_name = course_type = fname  = 'None'

    cur3 = conn.execute(f"SELECT SID FROM STUDENT WHERE SECTION = '{sec}'")
    row3 = cur3.fetchall()
    total = 0 
    for rows in row3:
        total = total + 1

    cur4 = conn.execute(f"""SELECT GENERATE_TIME FROM CODE_GENERATOR WHERE
                        COURSE_CODE = '{crs_code}' AND DAY = '{day_names[d]}' AND TIME = '{period_time[p]}'
                        """)
    row4 = cur4.fetchone()
    if row4:
        gen_time = str(row4[0])
    else:
        gen_time = "Class Did Not Held"


    tree = ttk.Treeview(full_frame)
    tree['columns'] = ('SID', 'Name', 'Join Time')
    tree.column("#0", width=0, stretch=NO, anchor = tk.CENTER)
    tree.column("#1", width=65, stretch=NO, anchor = tk.CENTER)
    tree.column("#2", width=195, stretch=NO, anchor = tk.CENTER)
    tree.column("#3", width=140, stretch=NO, anchor = tk.CENTER)
    tree.heading('#0', text="")
    tree.heading('#1', text="SID")
    tree.heading('#2', text="Student Name")
    tree.heading('#3', text="Join Time")
    tree['height']= 14

    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute(f"""SELECT SID, NAME, JOIN_TIME FROM PRESENT WHERE 
                            DAY = '{day_names[d]}' AND PERIOD = '{period_time[p]}' 
                            AND SECTION = '{sec}' 
                        """)
    present = 0
    row5 = cursor.fetchall()
    if row5:
        for row in row5:
            tree.insert("", 0, values=(row[0], row[1], row[2]))
            present = present + 1
    else: 
        print("No class held")
        
    tree.place(x=520, y=95)

    CTkLabel(
         full_frame,
         text='Present Students', 
         font=('Consolas', 32, 'bold'),
         text_color= '#a96c53',
    ).place(x=550, y=35)

    CTkLabel(
         full_frame,
         text='Class Details', 
         font=('Consolas', 32, 'bold'),
         text_color= '#a96c53',
    ).place(x=155, y=35)

    CTkLabel(
         full_frame,
         text='Day: '+day_names[d], 
         font=('Consolas',16), 
    ).place(x=100, y=90)

    CTkLabel(
         full_frame,
         text='Class Time: '+period_time[p], 
         font=('Consolas',16), 
    ).place(x=100, y=122)

    CTkLabel(
         full_frame,
         text='Section: '+str(sec), 
         font=('Consolas',16), 
    ).place(x=100, y=154)

    CTkLabel(
         full_frame,
         text='Course Code: '+crs_code, 
         font=('Consolas',16), 
    ).place(x=100, y=186)

    CTkLabel(
         full_frame,
         text='Course Name: '+course_name, 
         font=('Consolas',16), 
    ).place(x=100, y=218)

    CTkLabel(
         full_frame,
         text='Course Type: '+course_type, 
         font=('Consolas',16), 
    ).place(x=100, y=250)


    CTkLabel(
         full_frame,
         text='Faculty Name: '+fname, 
         font=('Consolas',16), 
    ).place(x=100, y=282)

    CTkLabel(
         full_frame,
         text='Class Held On: '+gen_time, 
         font=('Consolas',16), 
    ).place(x=100, y=314)

    CTkLabel(
         full_frame,
         text='Total Students: '+str(total), 
         font=('Consolas',16), 
    ).place(x=100, y=346)

    CTkLabel(
         full_frame,
         text='Total Present: '+str(present), 
         font=('Consolas',16), 
    ).place(x=100, y=378)
    

    CTkButton(
        details,
        text="Done",
        font=('Consolas',16,'bold'),
        command=details.destroy
    ).pack(pady=15)

    


    details.mainloop()

def select_sec(event=None):
    global section
    section = str(dropdown1.get())
    update_table(section)

def update_table(section):
    print("Update",section)
    conn = sqlite3.connect(r'Database/Database.db')
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute("SELECT ROUTINE.COURSE_CODE, ROUTINE.FID, COURSES.COURSE_TYPE \
                 FROM ROUTINE \
                 JOIN COURSES ON ROUTINE.COURSE_CODE = COURSES.COURSE_CODE \
                 WHERE ROUTINE.DAY=? AND ROUTINE.PERIOD=? AND ROUTINE.SECTION=?",
                (day_names[i] , period_time[j],section))
                
            row = cursor.fetchone()

            if row is not None:
                course_code, faculty_id, course_type = row

                butt_grid[i][j].configure(
                    text=f"{course_code}\n{faculty_id}",
                    fg_color='#5BA4FC' if course_type == 'Theory' else '#53D769',
                    hover_color='#5897EE' if course_type == 'Theory' else '#46C263'
                )
                butt_grid[i][j].update()
            else:
                butt_grid[i][j].configure(
                    text="",
                    fg_color='#F1F1F1',
                    hover_color = '#bfbfbf'
                )
                butt_grid[i][j].update()

conn = sqlite3.connect(r'Database/Database.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS PRESENT (
                   SID TEXT,
                   NAME TEXT,
                   COURSE_CODE TEXT,
                   SECTION TEXT,
                   DAY TEXT,
                   PERIOD TEXT,
                   CODE TEXT,
                   JOIN_TIME TEXT
                 )""")

if __name__ == "__main__":

    

    

    root = CTk()
    root.title('Student Routine')
    root.geometry("1000x480+180+120")

    title = CTkLabel(
    root,
    text='CLASS ROUTINE',
    font=('Consolas', 28, 'bold'),
    text_color= '#a96c53',
    # text_color= 'green',
    pady=14
    )
    title.pack()
    print(section)
    student_routine(root,section,sid)

    sec_select_f = CTkFrame(
        root,
        corner_radius = 0,
    )
    sec_select_f.pack(pady=9)

    CTkLabel(
        sec_select_f,
        text='Select section :',
        font=('Consolas', 16, 'bold'),
        padx = 10,
    ).grid(row = 1, column = 1 )


    cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
    sections = [row[0] for row in cursor]

    dropdown1 = ttk.Combobox(
        sec_select_f,
        values=sections,
    )
    dropdown1.grid(row=1, column=2)
    dropdown1.current(0)

    dropdown1.bind("<<ComboboxSelected>>", select_sec)
    select_sec() 


    root.mainloop()
    conn.close()
