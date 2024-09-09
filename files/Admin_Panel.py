from customtkinter import *
import os

def stud():
    # root.destroy()
    os.system("py Database/Students.py")


def fac():
    # root.destroy()
    os.system("py Database/Faculty.py")


def crs():
    # root.destroy()
    os.system("py Database/Courses.py")

def rout():
    os.system("py Database/Routine.py")

def stud_rout():
    os.system("py files/Student_Routine.py")

def fac_rout():
    os.system("py files/Faculty_Routine.py")

def attd():
    os.system("py Database/Attendance.py")
def class_details():
    os.system("py Database/Class_Details.py")

def logout_command():
    root.destroy()
    os.system("py RMS.py")

root = CTk()
root.geometry("1000x480+180+120")
root.title("Admin Panel")


label1 = CTkLabel(
    master=root,
    text="A D M I N I S T R A T O R",
    font = ('consolas', 32 ,'bold'),
    text_color= '#a96c53',
    pady=15
)
label1.pack()

label2 = CTkLabel(
    master=root,
    text="Welcome to Routine Management System",
    font=('consolas', 14, 'italic')
)
label2.pack()

label3 = CTkLabel(
    master=root,
    text="You are the Administrator",
    font=('consolas', 14, 'italic')
)
label3.pack()

frame1 = CTkFrame(master=root)
frame1.pack(pady=12)

label_modify = CTkLabel(
    master=frame1,
    text="SYSTEM DASHBOARD",
    text_color= "green",
    font = ('consolas', 23, 'bold')
)
label_modify.pack(side = TOP, pady=5)

button1 = CTkButton(
    master=frame1,
    text="Students",
    command=stud,
    text_color='black',
    border_width=1,
    height=40,
    width=170,
    font = ('consolas', 15 , 'italic','bold'),
)
button1.pack(side=LEFT, pady=10, padx=10)

button2 = CTkButton(
    master=frame1,
    text="Faculty Members",
    command=fac,
    font = ('consolas', 15 , 'italic','bold'),
    border_width=1,
    text_color='black',
    height=40,
    width=170,
)
button2.pack(side=LEFT, pady=10, padx=10)

button3 = CTkButton(
    master=frame1,
    text="Courses",
    command=crs,
    font = ('consolas', 15 , 'italic','bold'),
    text_color='black',
    border_width=1,
    height=40,
    width=170
)
button3.pack(side=LEFT, pady=10, padx=10)

button4 = CTkButton(
    master=frame1,
    text="Routine",
    command=rout,
    text_color='black',
    font = ('consolas', 15 , 'italic','bold'),
    border_width=1,
    height=40,
    width=170
)
button4.pack(side=LEFT, pady=10, padx=10)

frame2 = CTkFrame(master=root)
frame2.pack(pady=12)

label_tools = CTkLabel(
    master=frame2,
    text_color= "green",
    text="SETTINGS",
    font = ('consolas', 23, 'bold'),
)
label_tools.pack(pady=10) 

button5 = CTkButton(
    master=frame2,
    text="View Section-wise",
    command=stud_rout,
    # font = ('Galaxy', 15 ,'bold'),
    text_color = 'black',
    font = ('consolas', 15 , 'italic','bold'),
    border_width=1,
    height=40,
    width=170
)
button5.pack(side=LEFT, pady=10, padx=10)

button6 = CTkButton(
    master=frame2,
    text="View Faculty-wise",
    command=fac_rout,
    font = ('consolas', 15 , 'italic','bold'),
    text_color = 'black',
    border_width=1,
    height=40,
    width=170
)
button6.pack(side=LEFT, pady=10, padx=10)

button7 = CTkButton(
    master=frame2,
    text="Attendance",
    command=attd,
    font = ('consolas', 15 , 'italic','bold'),
    text_color = 'black',
    border_width=1,
    height=40,
    width=170
)
button7.pack(side=LEFT, pady=10, padx=10)

button8 = CTkButton(
    master=frame2,
    text="Class Details",
    command=class_details,
    font = ('consolas', 15 , 'italic','bold'),
    text_color = 'black',
    border_width=1,
    height=40,
    width=170
)
button8.pack(side=LEFT, pady=10, padx=10)

logout = CTkButton(
    master = root ,
    text = "LOG OUT",
    command = logout_command,
    font = ('consolas', 16 ,'bold'),
    fg_color = '#FC3D39',
    hover_color = '#E33437',
    border_width=1,
    height=30
).pack(pady=7, padx=10)

quit = CTkButton(
    master = root ,
    text = "EXIT",
    command = root.quit,
    font = ('consolas', 16 ,'bold'),
    fg_color = '#FC3D39',
    hover_color = '#E33437',
    border_width=1,
    height=30
).pack(pady=7, padx=10)

root.mainloop()
