import sqlite3
from customtkinter import *
from tkinter import messagebox
from tkinter import ttk
import random
import string
import time
import datetime

days = 5
periods = 9
fid = None
butt_grid = []


day_names = [ 'Saturday', 'Sunday','Monday', 'Tuesday', 'Wednesday']
period_time = ['8:00-8:50','8:50-9:40','9:40-10:30','10:50-11:40','11:40-12:30','12:30-1:20','2:30-3:20','3:20-4:10','4:10-5:00']


def create_codegen():
    cursor = conn.cursor()
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS CODE_GENERATOR (
            COURSE_CODE TEXT NOT NULL,
            DAY TEXT NOT NULL,
            TIME TEXT NOT NULL,
            CODE TEXT NOT NULL,
            GENERATE_TIME TEXT NOT NULL,
            VALID_TILL TEXT NOT NULL
        )
    """)
    conn.commit()

def generate_code(crs_code, sec, d, p):
    cursor = conn.cursor()
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    print("Generated Code:", code)

    gen_time = datetime.datetime.fromtimestamp(int(time.time()))
    validity = datetime.datetime.fromtimestamp(int(time.time()) + 1800)
    gt = gen_time.strftime("%I:%M %p")

    formatted_gen_time = gen_time.strftime("%d-%m-%Y %I:%M %p")
    formatted_validity = validity.strftime("%d-%m-%Y %I:%M %p")
    


    check = conn.execute(f"""
            SELECT CODE FROM CODE_GENERATOR 
            WHERE COURSE_CODE = '{crs_code}' AND DAY = '{day_names[d]}' AND TIME = '{period_time[p]}'
        """)
    row = check.fetchone()
    if row is not None:
        conn.execute(f"""
            DELETE FROM CODE_GENERATOR 
            WHERE COURSE_CODE = ? AND DAY = ? AND TIME = ?
        """, (crs_code, day_names[d], period_time[p]))
        conn.commit()
        conn.execute(f"""
            DELETE FROM PRESENT  
            WHERE CODE = '{row[0]}'
        """)
        conn.commit()
        print("Expired code deleted successfully.")

        
    cursor.execute("""
        INSERT INTO CODE_GENERATOR 
        (COURSE_CODE, DAY, TIME, CODE, GENERATE_TIME, VALID_TILL)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (crs_code, day_names[d], period_time[p], code, formatted_gen_time, formatted_validity))
    conn.commit()

    

    cursor.execute(f"""
            UPDATE ATTENDANCE 
            SET TOTAL_CLASS = TOTAL_CLASS + 1 
            WHERE COURSE_CODE = ? AND SECTION = ?
            """, (crs_code, sec))
    conn.commit()
    print(f"Total class updated for course code: {crs_code}, section: {sec}")



    generated_code = CTk()
    generated_code.title("Generated Code")
    generated_code.geometry("250x130+550+300")

    CTkLabel(
        generated_code,
        text = "Class Code :"+code,
        font=('Consolas', 16),
        pady =10
    ).pack()

    CTkLabel(
        generated_code,
        text = "Course Code :"+crs_code,
        font=('Consolas', 16),
        pady =10
    ).pack()
    

    CTkLabel(
        generated_code,
        text = "Generate Time :"+gt,
        font=('Consolas', 16),
        pady =10
    ).pack()

    generated_code.mainloop()

def faculty_routine(root,fac):
    
    global butt_grid
    global fid
    fid = fac
    print(fid)
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
            font=('Consolas', 13,'bold'),
            width=98,
            height=60,
            corner_radius=0,
            fg_color='#F1F1F1',
            hover_color='#bfbfbf',
            text_color='black',
            command=lambda x=i, y=j: process_button(x, y)
            )
            bb.pack(padx=1, pady=1) 
            b.append(bb)

        butt_grid.append(b)
        b = []

    update_table(fid)


def process_button(d, p):
    details = CTk()
    # details.geometry("300x350+530+180")
    details.geometry("520+180")
    global fid
    cursor = conn.execute(f"SELECT SECTION, COURSE_CODE FROM ROUTINE\
        WHERE DAY='{day_names[d]}' AND PERIOD='{period_time[p]}' AND FID='{fid}'")
    print(day_names[d],period_time[p],fid)
    row = cursor.fetchone()
    sec = "None"

    if row is not None:
        print("Details found")
        sec = row[0]
        crs_code = row[1]
        print(sec,crs_code)
        

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
        crs_code = course_name = course_type = fname  = 'None'

    CTkLabel(
         details,
         text='Class Details', 
         font=('Consolas', 26, 'bold')
    ).pack(pady=15)

    CTkLabel(
         details,
         text='Day: '+day_names[d], 
         font=('Consolas',16), 
    ).pack(padx=20)

    CTkLabel(
         details,
         text='Class Time: '+period_time[p], 
         font=('Consolas',16), 
    ).pack(padx=20)

    CTkLabel(
         details,
         text='Section: '+str(sec), 
         font=('Consolas',16), 
    ).pack(padx=20)

    CTkLabel(
         details,
         text='Course Code: '+crs_code, 
         font=('Consolas',16), 
    ).pack(padx=20)

    CTkLabel(
         details,
         text='Course Name: '+course_name, 
         font=('Consolas',16), 
    ).pack(padx=20)

    CTkLabel(
         details,
         text='Course Type: '+course_type, 
         font=('Consolas',16), 
    ).pack(padx=20)

    CTkLabel(
         details,
         text='Faculty ID: '+str(fid), 
         font=('Consolas',16), 
    ).pack(padx=20)

    CTkLabel(
         details,
         text='Faculty Name: '+fname, 
         font=('Consolas',16), 
    ).pack(padx=20)

    if crs_code !='None':
        create_codegen()
        otpframe = CTkFrame(
            details,
            )
        otpframe.pack(pady=5,padx =30)

        CTkLabel(
            otpframe,
            text='Take Attendance : ',
            font=('Consolas', 16),
        ).grid(padx=10,row = 1 , column = 1)

        CTkButton(
            otpframe,
            text="Generate Code",
            font=('Consolas',16,'bold'),
            command=lambda: generate_code(crs_code, sec, d, p),
            fg_color = '#53D769',
            hover_color = '#46C263',
        ).grid(pady=10,padx=10,row = 1 , column = 2)


    CTkButton(
        details,
        text="OK",
        font=('Consolas',16),
        command=details.destroy
    ).pack(pady=20)

    details.mainloop()


def select_fac(event=None):
    global fid
    fid = str(dropdown.get())
    update_table(fid)



def update_table(fid):
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SECTION, COURSE_CODE FROM ROUTINE\
                WHERE DAY='{day_names[i]}' AND PERIOD='{period_time[j]}' AND FID='{fid}'")
            row = cursor.fetchone()

            if row is not None: 
                print("Row is not empty , row = ",row)
                sec,crs_code = row

                cur1 = conn.execute(f"SELECT COURSE_TYPE FROM COURSES WHERE COURSE_CODE='{crs_code}'")
                row1 = cur1.fetchone()
                crs_type = row1[0]

                if crs_type == 'Theory':
                    butt_grid[i][j].configure(
                        text=f"Sections: {sec}\n Theory" ,
                        fg_color='#5BA4FC',
                        hover_color='#5897EE'
                    )
                else:
                    butt_grid[i][j].configure(
                        text=f"Section: {sec}\n Sessional",
                        fg_color='#53D769' ,
                        hover_color='#46C263' 
                    )
                butt_grid[i][j].update()

            else:
                # print("Row is empty")
                butt_grid[i][j].configure(
                    text="",
                    fg_color='#F1F1F1',
                    hover_color='#bfbfbf'
                )
                butt_grid[i][j].update()



conn = sqlite3.connect(r'Database/Database.db')
if __name__ == "__main__":
    
    root = CTk()
    root.title('Faculty-wise Routine')
    root.geometry("1000x480+180+120")

    title = CTkLabel(
    root,
    text='FACULTY-WISE ROUTINE',
    font=('Consolas', 28, 'bold'),
    text_color= '#a96c53',
    pady=14
    )
    title.pack()

    print("fid before", fid)
    faculty_routine(root,fid)

    fac_select_f = CTkFrame(
        root,
        corner_radius = 0,
    )
    fac_select_f.pack(pady=9)

    CTkLabel(
        fac_select_f,
        text='Select faculty :',
        font=('Consolas', 16, 'bold'),
        padx = 10,
    ).grid(row = 1, column = 1 )

    cursor = conn.execute("SELECT DISTINCT FID FROM FACULTY")
    fac_li = [row[0] for row in cursor]
    dropdown = ttk.Combobox(
        fac_select_f,
        values=fac_li,
    )
    dropdown.grid(row=1, column=2)
    dropdown.current(0)

    dropdown.bind("<<ComboboxSelected>>", select_fac)
    select_fac() 


    root.mainloop()
    conn.close()
