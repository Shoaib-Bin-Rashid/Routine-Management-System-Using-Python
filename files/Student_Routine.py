import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import datetime

days = 5
periods = 9
section = None
sid = None
butt_grid = []


day_names = [ 'Saturday', 'Sunday','Monday', 'Tuesday', 'Wednesday']
period_time = ['8:00-8:50','8:50-9:40','9:40-10:30','10:50-11:40','11:40-12:30','12:30-1:20','2:30-3:20','3:20-4:10','4:10-5:00']


def submit(code,code_entry, sid, actualcode, d, p, conn):
    print("Entry is ", code_entry)
    if code_entry == '':
        messagebox.showerror("Blank Error", "Enter a code first!")
    elif code_entry == actualcode:
        cursor = conn.execute("""
            SELECT COURSE_CODE, CODE, VALID_TILL 
            FROM CODE_GENERATOR 
            WHERE CODE = ? AND DAY = ? AND TIME = ?
        """, (code_entry, day_names[d], period_time[p]))
        
        row = cursor.fetchone()
        
        if row is not None:
            crs = row[0]
            cde = row[1]
            end_time = row[2]
            
            current_time = datetime.datetime.now()
            validity_time = datetime.datetime.strptime(end_time, "%d-%m-%Y %I:%M %p")
            
            if current_time <= validity_time:
                print("Attendance has been recorded")
                
                cursor2 = conn.execute("""
                    SELECT PRESENT, TOTAL_CLASS 
                    FROM ATTENDANCE 
                    WHERE COURSE_CODE = ? AND SID = ?
                """, (crs, sid))
                print(crs, sid)
                row2 = cursor2.fetchone()
                
                if row2 is not None:
                    print("Inside row2")
                    pre = int(row2[0])
                    total_class = int(row2[1])                  
                    conn.execute("""
                        UPDATE ATTENDANCE 
                        SET PRESENT = ? 
                        WHERE COURSE_CODE = ? AND SID = ?
                    """, (pre + 1, crs, sid))
                    conn.commit()
                    print("Updated Present : ", pre + 1)

                    new_present = pre + 1
                    percentage = (new_present * 100) / total_class
                    
                    conn.execute("""
                        UPDATE ATTENDANCE
                        SET PERSENTAGE = ?
                        WHERE COURSE_CODE = ? AND SID = ?
                    """, (percentage, crs, sid))
                    conn.commit()


                    messagebox.showinfo("Success", "Attendance has been successfully recorded!")
                    code.destroy()

                else:
                    cursor5 = conn.execute("""
                        SELECT NAME, SECTION , ROLL 
                        FROM STUDENT
                        WHERE SID = ?
                    """, (sid,))
                    
                    row4 = cursor5.fetchone()
                    
                    if row4:
                        name, sec ,roll= row4
                        
                        cursor6 = conn.execute("""
                                SELECT TOTAL_CLASS
                                FROM ATTENDANCE
                                WHERE COURSE_CODE = ?
                            """, (crs,))      
                        row6 = cursor6.fetchone()

                        if row6 is None or row6[0] is None:
                            totalcls = 1
                            percentage = 100
                        else:
                            totalcls = row6[0]
                            percentage = 100

                        conn.execute("""
                            INSERT INTO ATTENDANCE 
                            (SID, NAME, COURSE_CODE, SECTION, ROLL, TOTAL_CLASS, PRESENT, PERSENTAGE)
                            VALUES (?, ?,?, ?, ?, ?, ?, ?)
                        """, (sid, name, crs, sec,roll, totalcls, 1, percentage))
                        conn.commit()
                        messagebox.showinfo("Success", "Attendance has been successfully recorded!")
                        code.destroy()

                cursor3 = conn.execute("""
                        SELECT NAME, SECTION 
                        FROM STUDENT
                        WHERE SID = ?
                    """, (sid,))
                    
                row3 = cursor3.fetchone()
                    
                if row3:
                    name, sec = row3
                        
                    cursor4 = conn.execute("""
                        INSERT INTO PRESENT 
                        (SID, NAME, COURSE_CODE, SECTION, DAY, PERIOD, CODE, JOIN_TIME)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (sid, name, crs, sec, day_names[d], period_time[p], cde, current_time.strftime("%d-%m-%Y %I:%M %p")))
                    print(sid, name, crs, sec, day_names[d], period_time[p], cde, current_time.strftime("%d-%m-%Y %I:%M %p"))
                    conn.commit()
            else:
                messagebox.showerror("Expired Code", "The code has expired!")
                code.destroy()
        else:  
            print("No details found!")  
    else:
        messagebox.showwarning("Not Matched", "Code did not match! Try again")

        



def student_present(course,sid,d,p):
    code = CTk()
    code.title("Class Code")
    code.geometry("+520+300")

    cursor = conn.execute(f"""
            SELECT CODE FROM CODE_GENERATOR 
            WHERE COURSE_CODE = '{course}' AND DAY = '{day_names[d]}' AND TIME = '{period_time[p]}'
        """)
    row = cursor.fetchone()
    if row is not None:
        cd = row[0]

        codelabel_text = f"Class Join Code: {cd}"
    else:
        codelabel_text = "No code was generated for this class"

    CTkLabel(
        code,
        text=codelabel_text,
        font=('Consolas', 16)
    ).pack(padx=60, pady=10)

    CTkLabel(
        code,
        text="Enter Class Code:",
        font=('Consolas', 16)
    ).pack(padx=60, pady=10)

    code_entry = CTkEntry(
        code,
        font=('Consolas', 14),
    )
    code_entry.pack(padx=60, pady=10)

    submit_button = CTkButton(
        code,
        text="Submit",
        command=lambda: submit(code,code_entry.get(),sid,cd,d,p,conn),
        font=('Consolas', 14, 'bold'),
        fg_color='#53D769',
        hover_color='#46C263'
    )
    submit_button.pack(padx = 60,pady=10)

    cancel_button = CTkButton(
        code,
        text="Cancel",
        command=code.destroy,
        font=('Consolas', 14, 'bold'),
        fg_color='#FC3D39',
        hover_color='#E33437'
    )
    cancel_button.pack(padx = 60,pady=10)

    code.mainloop()


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
    # details.geometry("300x350+530+180")
    details.geometry("480+180")
    
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

    CTkLabel(
         details,
         text='Class Details', 
         font=('Consolas', 26, 'bold')
    ).pack(pady=15)

    CTkLabel(
         details,
         text='Day: '+day_names[d], 
         font=('Consolas',16), 
    ).pack(padx=30)

    CTkLabel(
         details,
         text='Class Time: '+period_time[p], 
         font=('Consolas',16), 
    ).pack(padx=30)

    CTkLabel(
         details,
         text='Section: '+str(sec), 
         font=('Consolas',16), 
    ).pack(padx=30)

    CTkLabel(
         details,
         text='Course Code: '+crs_code, 
         font=('Consolas',16), 
    ).pack(padx=30)

    CTkLabel(
         details,
         text='Course Name: '+course_name, 
         font=('Consolas',16), 
    ).pack(padx=30)

    CTkLabel(
         details,
         text='Course Type: '+course_type, 
         font=('Consolas',16), 
    ).pack(padx=30)

    CTkLabel(
         details,
         text='Faculty ID: '+fid, 
         font=('Consolas',16), 
    ).pack(padx=30)

    CTkLabel(
         details,
         text='Faculty Name: '+fname, 
         font=('Consolas',16), 
    ).pack(padx=30)

    if crs_code !='None':
        otpframe = CTkFrame(
            details,
            )
        otpframe.pack(pady=5,padx =30)

        CTkLabel(
            otpframe,
            text='Give Present :',
            font=('Consolas', 16),
        ).grid(padx=10,row = 1 , column = 1)

        CTkButton(
            otpframe,
            text="Enter Code",
            font=('Consolas',16,'bold'),
            command= lambda: student_present(crs_code,sid,d,p),
            fg_color = '#53D769',
            hover_color = '#46C263',
            text_color= '#FFFFFF',
        ).grid(pady=10,padx=10,row = 1 , column = 2)


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
if __name__ == "__main__":

    root = CTk()
    root.title('Student Routine')
    root.geometry("1000x480+180+120")

    title = CTkLabel(
    root,
    text='SECTION-WISE ROUTINE',
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
