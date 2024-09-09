import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

days = 5
periods = 9
section = None
butt_grid = []


day_names = [ 'Saturday', 'Sunday','Monday', 'Tuesday', 'Wednesday']
period_time = ['8:00-8:50','8:50-9:40','9:40-10:30','10:50-11:40','11:40-12:30','12:30-1:20','2:30-3:20','3:20-4:10','4:10-5:00']


def update_class(d, p, tree, det):
    print(section,d,p)
    if len(tree.selection()) > 1:
        messagebox .showerror("Selection Error", "Select one course at a time!")
        det.destroy()
        return
    elif len(tree.selection()) == 0:
        messagebox.showerror("Selection Error", "Please select a course from the list!")
        det.destroy()
        return
    else:
        row = tree.item(tree.selection()[0])['values']

        if row[0] == 'No Class':
            conn.execute(f"DELETE FROM ROUTINE WHERE ID='{str(section)+str(d)+str(p)}'")
        else:
           conn.execute(f"""REPLACE INTO ROUTINE (ID, DAY, PERIOD, COURSE_CODE, SECTION, FID)
                 VALUES (?, ?, ?, ?, ?, ?)""",
             (str(section)+str(d)+str(p), day_names[d] , period_time[p] , row[1], section, row[0]))

        conn.commit()
        update_table()
    det.destroy()



def process_button(d, p):
    details = CTk() 
    details.geometry("600x400+400+150")


    cursor=conn.cursor()
    cursor.execute("SELECT COURSE_CODE FROM COURSES")
    course_list = [row[0] for row in cursor]
    # course_list.insert(0, 'No Class') 

    cursor.execute("""SELECT FACULTY.FID, FACULTY.NAME, FACULTY.COURSE1,
                      FACULTY.COURSE2, COURSES.COURSE_CODE, 
                      COURSES.COURSE_NAME, COURSES.COURSE_TYPE
                      FROM FACULTY
                      INNER JOIN COURSES ON
                      FACULTY.COURSE1 = COURSES.COURSE_CODE OR
                      FACULTY.COURSE2 = COURSES.COURSE_CODE
                      """)
    class_details = cursor.fetchall()

    CTkLabel(
        details,
        text='Select Course From The List',
        font=('Consolas', 16, 'bold')
    ).pack()

    CTkLabel(
        details,
        text=f'Day: {day_names[d]}',
        font=('Consolas', 16)
    ).pack()

    CTkLabel(
        details,
        text=f'Time : {period_time[p]}',
        font=('Consolas', 16)
    ).pack()

    tree = ttk.Treeview(details)
    tree['columns'] = ('FID', 'code','Cname', 'type')
    tree.column("#0", width=0, stretch=NO,anchor = tk.CENTER)
    tree.column("FID", width=80, stretch=NO,anchor = tk.CENTER)
    tree.column("code", width=100, stretch=NO,anchor = tk.CENTER)
    tree.column("Cname", width=220, stretch=NO,anchor = tk.CENTER)
    tree.column("type", width=100, stretch=NO,anchor = tk.CENTER)
    tree.heading('#0', text="")
    tree.heading('FID', text="Faculty ID")
    tree.heading('code', text="Course Code")
    tree.heading('Cname', text="Course Name")
    tree.heading('type', text="Course Type")

    for row in class_details:
        tree.insert(
            "",
            0,
            values=(row[0], row[4],row[5],row[6])
        )
    tree.insert("",0,values=('No Class','','',''))
    tree.pack(pady=10, padx=20)

    CTkButton(
        details,
        text="OK",
        command=lambda x=d, y=p, z=tree, r=details: update_class(x, y, z, r)
    ).pack(padx=15,pady=15)

    details.mainloop()


def select_sec(event=None):
    global section
    section = str(dropdown1.get())
    update_table()

def update_table():
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
                print(i, j, course_code)
            else:
                butt_grid[i][j].configure(
                    text="",
                    fg_color='#F1F1F1',
                    hover_color = '#bfbfbf'
                )
                butt_grid[i][j].update()

                
conn = sqlite3.connect(r'Database/Database.db')

conn.execute('CREATE TABLE IF NOT EXISTS ROUTINE\
            (ID CHAR(10) NOT NULL PRIMARY KEY,\
             DAY INT NOT NULL,\
             PERIOD INT NOT NULL,\
             COURSE_CODE CHAR(10) NOT NULL,\
             SECTION CHAR(5) NOT NULL,\
             FID CHAR(10) NOT NULL)')

root = CTk()
root.title('Routine Maker')
root.geometry("1000x480+180+120")

title = CTkLabel(
    root,
    text='CLASS ROUTINE',
    font=('Consolas', 28, 'bold'),
    text_color= '#a96c53',
    pady=14
)
title.pack()



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


    # if i%2 == 0:
    #     label_border.configure(fg_color='#334357')
    # else :
    #     label_border.configure(fg_color='#a96c53')

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


    # if i%2 == 0:
    #     label_border.configure(fg_color='#334357')
    # else :
    #     label_border.configure(fg_color='#a96c53')

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
        text='No Class',
        font=('Consolas', 14,'bold'),
        width=98,
        height=60,
        corner_radius=0,
        fg_color='#F1F1F1',
        hover_color='#bfbfbf',
        text_color='black',
        command=lambda x = i, y = j: process_button(x, y)
        )
        bb.pack(padx=1, pady=1) 
        b.append(bb)

    butt_grid.append(b)
    b = []

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
