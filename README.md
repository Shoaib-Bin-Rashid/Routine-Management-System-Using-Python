# Routine Management System

**Project Overview**  
The Routine Management System is an application developed with Python and Tkinter for managing academic routines. It provides a streamlined interface for students, faculty, and administrators to interact with class schedules, attendance, and student information.

### Features

1. **Login System**

   - Supports login for three user types: students, faculty, and admins.
   - Validates empty fields, incorrect usernames, and wrong passwords.
   - Includes a password visibility toggle for user convenience.

2. **Faculty Section**

   - Faculty members can view their class routines.
   - By selecting a class, faculty can view class details and generate a Join Code to start the class.
   - This code is used by students to mark attendance.

3. **Student Section**

   - Students can view their class routines.
   - They can enter a Join Code provided by the faculty to mark their attendance. The code is valid for 30 minutes, with the flexibility to modify this duration.

4. **Admin Panel**
   - **Student Section:** Admins can add, update, delete, and view all student information.
   - **Faculty & Courses Section:** Admins can manage faculty members and course details.
   - **Routine Section:** Admins can create and update class schedules and assign faculty to sections.
   - **Attendance Tracking:** Detailed attendance records are available for each course, with attendance percentages for students.
   - **Class Details:** Admins can view which students are present in a currently running class or check attendance from past classes.

### Additional Features

- **View Section-Wise Routine:** Admins can access the complete schedule for any section.
- **View Faculty-Wise Routine:** Admins can view and manage the schedules of individual faculty members.

### Technology Stack

- **Language:** Python
- **GUI Library:** Tkinter
- **Database:** SQLite

### Watch the Presentation Video

Check out the full video demo of the project on YouTube: [Routine Management System Using Python & CustomTkinter](https://www.youtube.com/watch?v=DdlkMcehpEM)
