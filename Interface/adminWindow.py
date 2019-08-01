from . import addStudent
from . import addTeacher
from tkinter import Tk,Button,Toplevel
import os

if(not os.path.exists("Database")):
    import setup_files_and_folders
    setup_files_and_folders.setup()
    
def adminWindow():
    root2=Toplevel()
    root2.focus_set()
    root2.lower()
    root2.title("Admin Window")
    root2.geometry("300x300+500+150")
    Button(root2,text="Add Student",width=15,height=3,command=addStudent.addStudent).pack()
    Button(root2,text="Add Teacher",width=15,height=3,command=addTeacher.addTeacher).pack()
    root2.mainloop()
