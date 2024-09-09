from customtkinter import *
import sqlite3
import os ,sys
from tkinter import messagebox
from tkinter import ttk
sys.path.insert(0, 'files/')
import Student_Routine as sr
import Faculty_Routine as fr


def logout_command(stud):
    stud.destroy()
    os.system("py RMS.py")

def login():
    if user_entry.get() == "" or pass_entry.get() == "":
        messagebox.showwarning("Blank Field", "Some Fields are Empty")
    else:
        user = str(dropdown.get())

        if user == "Student":
            if not user_entry.get().isdigit():
                messagebox.showwarning("Wrong input", "Enter integer without any spaces")

            conn = sqlite3.connect(r'Database\\Database.db')
            cursor = conn.execute(f"SELECT SID,PASS, NAME, ROLL, SECTION FROM STUDENT WHERE SID = {user_entry.get()}")
            cursor = list(cursor)
            if len(cursor) == 0:
                messagebox.showwarning('Invalid user', 'No such user found!')
            elif pass_entry.get() != cursor[0][1]:
                messagebox.showerror('Wrong password', 'Password Incorret!')
            else:
                stud = CTk()
                stud.title("Routine")
                stud.geometry("1000x530+180+100")

                stud_label = CTkLabel(
                    master=stud,
                    text=f"Welcome to RMS {cursor[0][2]}",
                    font=("consolas", 14, "italic"),
                    # pady=10
                )
                stud_label.pack()

                sec = cursor[0][4]

                details = CTkLabel(
                    master=stud,
                    text=f"Student ID : {cursor[0][0]} \t Roll : {cursor[0][3]} \t Section : {sec}",
                    font=("consolas", 14, "italic")
                )
                details.pack()

                title = CTkLabel(
                    master=stud,
                    text="CLASS ROUTINE",
                    font=("consolas", 27, "bold"),
                    pady=5
                )
                title.pack()
                sr.student_routine(stud,sec,user_entry.get())


                end_frame = CTkFrame(
                    stud,
                    fg_color = '#ebebeb',
                    bg_color="#ebebeb"
                )
                end_frame.pack(pady = 10 , padx = 5)

                logout = CTkButton(
                    master = end_frame,
                    text = "LOG OUT",
                    command = lambda : logout_command(stud),
                    font = ('consolas', 14 ,'bold'),
                    fg_color = '#FC3D39',
                    hover_color = '#E33437',
                    # border_width=1,
                    # height=30
                ).grid(row = 1, column = 1,pady=7, padx=15)
                quit = CTkButton(
                    master = end_frame,
                    text = "Exit",
                    command = stud.quit,
                    font = ('consolas', 14 ,'bold'),
                    fg_color = '#FC3D39',
                    hover_color = '#E33437',
                ).grid(row = 1, column = 2,padx = 15 )

                root.destroy()
                stud.mainloop()
                conn.close()


        elif user == "Faculty":
            conn = sqlite3.connect(r'Database\\Database.db')
            cursor = conn.execute(f"SELECT FID,PASS, NAME FROM FACULTY WHERE FID = '{user_entry.get()}'")
            cursor = list(cursor)
            if len(cursor) == 0:
                messagebox.showwarning('Invalid user', 'No such user found!')
            elif pass_entry.get() != cursor[0][1]:
                messagebox.showerror('Wrong password', 'Password Incorret!')
            else:
                fac = cursor[0][0]
                facu_root = CTk()
                facu_root.title("Routine")
                facu_root.geometry("1000x530+180+100")

                stud_label = CTkLabel(
                    master=facu_root,
                    text=f"Welcome to RMS {cursor[0][2]} sir/ma'am",
                    font=("consolas", 14, "italic"),
                    # pady=10
                )
                stud_label.pack()

                details = CTkLabel(
                    master=facu_root,
                    text=f"Faculty ID : {fac}",
                    font=("consolas", 14, "italic")
                )
                details.pack()

                title = CTkLabel(
                    master=facu_root,
                    text="FACULTY ROUTINE",
                    font=("consolas", 27, "bold"),
                    pady=5
                )
                title.pack()
                fr.faculty_routine(facu_root,fac)

                end_frame = CTkFrame(
                    facu_root,
                    fg_color = '#ebebeb',
                    bg_color="#ebebeb"
                )
                end_frame.pack(pady = 10 , padx = 5)

                logout = CTkButton(
                    master = end_frame,
                    text = "LOG OUT",
                    command = lambda : logout_command(facu_root),
                    font = ('consolas', 14 ,'bold'),
                    fg_color = '#FC3D39',
                    hover_color = '#E33437',
                    # border_width=1,
                    # height=30
                ).grid(row = 1, column = 1,pady=7, padx=15)
                quit = CTkButton(
                    master = end_frame,
                    text = "Exit",
                    command = facu_root.quit,
                    font = ('consolas', 14 ,'bold'),
                    fg_color = '#FC3D39',
                    hover_color = '#E33437',
                ).grid(row = 1, column = 2,padx = 15 )

                root.destroy()
                facu_root.mainloop()
                conn.close()


        elif user == "Admin":
            if pass_entry.get() == "Admin" and user_entry.get() == "Admin":
                root.destroy()
                os.system("py files\\Admin_Panel.py")
            elif user_entry.get() != "Admin":
                messagebox.showerror("Username Error", "Invalid Username")
            else :
                messagebox.showerror("Password Error","Incorrect Password")
        else:
            messagebox.showerror("Identity Error","Invalid User Type")

def show_pass():
    if pass_entry.cget("show") == "":
        pass_entry.configure(show="*")
        show_hide.configure(text="Show")
    else:
        pass_entry.configure(show="") 
        show_hide.configure(text="Hide")


root = CTk()
root.title("Routine Management System")
root.geometry("700x405+320+150")

Label1 = CTkLabel(
    master=root,
    text="ROUTINE MANAGEMENT SYSTEM",
    font=('Calibri', 32, 'bold'),
    pady=18
)
Label1.pack()

Label2 = CTkLabel(
    master=root,
    text="Welcome to RMS",
    font=('consolas', 14, 'italic'),
)
Label2.pack()

Label3 = CTkLabel(
    master=root,
    text="Login to your RMS ID",
    font=('consolas', 14, 'italic'),
)
Label3.pack()

frame = CTkFrame(
    master=root,
    height=900,
    width=500,
)
frame.pack(pady=12)

Label4 = CTkLabel(
    master=frame,
    text="Identity:",
    font=('consolas', 18,'bold'),
    pady=12,
    padx=12
)
Label4.grid(row=1, column=1)
 
dropdown = CTkComboBox(
    master=frame,
    values=['Student', 'Faculty', 'Admin'],
    width= 200,
    height= 30,
    dropdown_fg_color = 'white',
)
dropdown.grid(row=1, column=2,pady=12)
dropdown.set('Student')

Label5 = CTkLabel(
    master=frame,
    text="User ID:",
    font=('consolas', 18,'bold'),
    padx=12,
    pady = 12
)
Label5.grid(row=2, column=1)

user_entry = CTkEntry(
    master=frame,
    font=('consolas', 14),
    width=200,
    height= 30
)
user_entry.grid(row=2, column=2)

Label6 = CTkLabel(
    master=frame,
    text="Password:",
    font=('consolas', 18,'bold'),
    pady=12,
    padx=12
)
Label6.grid(row=3, column=1)

pass_entry = CTkEntry(
    master=frame,
    font=('consolas', 14),
    show="*",
     width=200,
    height= 30
)
pass_entry.grid(row=3, column=2)

# Show Button
show_hide = CTkButton(
    master=frame,
    text="Show",
    font = ('consolas', 14 ,'bold'), 
    # width=100,
    command=show_pass
)
show_hide.grid(row=3, column=3, padx=12)

loginButton = CTkButton(
    master=root,
    text="Login",
    command=login,
    font = ('consolas', 14 ,'bold'),
    fg_color = '#53D769',
    hover_color = '#46C263',
)
loginButton.pack(pady=10)

quit = CTkButton(
    master = root ,
    text = "Exit",
    command = root.quit,
    font = ('consolas', 14 ,'bold'),
    fg_color = '#FC3D39',
    hover_color = '#E33437',
    # height=40
).pack()

root.mainloop()
 