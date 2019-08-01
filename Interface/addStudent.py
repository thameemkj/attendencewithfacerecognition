from tkinter import *
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror,askyesno,askokcancel
import cv2
import os
from PIL import Image,ImageTk
from Trainer import trainer
import openpyxl as xl

detector=cv2.CascadeClassifier(os.path.join("Trainer","haarcascade_frontalface_default.xml"))
unique_ids=os.path.join("Database","unique_ids_list.txt")
list_images=[]
student_image=None
unique_ids_list=[]
row=None
row2=None

def addStudent():
    global row
    global row2
    book=xl.load_workbook(os.path.join("Database","Students","Attendence.xlsx"))
    sheet=book["January"]
    row=1
    while(True):
        if(sheet['A{0}'.format(row)].value==None):
            break
        row+=1
    book2=xl.load_workbook(os.path.join("Database","teachers_and_students.xlsx"))
    sheet2=book2.active
    row2=1
    while(True):
        if(sheet2['A{0}'.format(row2)].value==None):
            break
        row2+=1
    global root_label
    global unique_ids_list
    f=open(unique_ids,"r")
    unique_ids_list=f.read().split()
    f.close()   
    root=Toplevel()
    root.focus_set()
    root.title("Add Student")
    root.geometry("400x300+500+50")
    
    F0=Frame(root)
    F0.pack()
    F5=Frame(root)
    F5.pack()
    F1=Frame(root)
    F1.pack()
    F2=Frame(root)
    F2.pack()
    F3=Frame(root)
    F3.pack()
    F4=Frame(root)
    F4.pack(pady=5)

    classes=['1','2','3','4','5','6','7','8','9','10']
    
    root_label=Label(F0,text="Photo")
    root_label.pack(pady=5)
    Label(F5,text="AdmisionNo",width=15,height=2,font=('',15)).pack(side="left",anchor=W,expand=YES,fill=BOTH,pady=1)
    E4=Entry(F5,width=30)
    E4.pack(side="left",anchor=W,expand=YES,fill=X,pady=1)
    Label(F1,text="Name ",width=15,height=2,font=('',15)).pack(side="left",anchor=W,expand=YES,fill=BOTH,pady=1)
    E1=Entry(F1,width=30)
    E1.pack(side="left",anchor=W,expand=YES,fill=X,pady=1)
    Label(F2,text="Class ",width=15,height=2,font=('',15)).pack(side="left",anchor=W,expand=YES,fill=BOTH,pady=1)
    E2=Combobox(F2,values=classes,width=27)
    E2.pack(side="left",anchor=W,expand=YES,fill=X,pady=1)
    Label(F3,text="RollNo ",width=15,height=2,font=('',15)).pack(side="left",anchor=W,expand=YES,fill=BOTH,pady=1)
    E3=Entry(F3,width=30)
    E3.pack(side="left",anchor=W,expand=YES,fill=X,pady=1)
    
    def submit():
        global list_images
        global student_image
        global row
        global row2
        student_admno=E4.get()
        student_name=E1.get()
        student_class=E2.get()
        student_rollno=E3.get()
       
        if((student_admno=='') or (not student_admno.isdigit()) or (student_name=='') or (student_class not in classes) or (len(student_rollno)<1) or (len(student_rollno)>2) or (len(list_images)!=50) or (not student_rollno.isdigit())):
            showerror("Error Submit","Something is wrong in your inputs..!!!")
            root.focus_set()
        elif(student_admno in unique_ids_list):
            showerror("Error Submit","A student in this admission number already exists")
            root.focus_set()
        elif(askyesno("Confirm Submit","Hope you have entered right datas.\nAre you sure to submit ?")):
            global root_label
            root.lift()
            root_label.destroy()
            root_label=Label(F0,text="Photo")
            root_label.pack(pady=5)
            root.geometry("400x300+500+50")
            E1.delete(0,END)
            E2.delete(0,END)
            E3.delete(0,END)
            E4.delete(0,END)
            f=open(unique_ids,"a")
            f.write(student_admno+'\n')
            f.close()
            for sheet in book.worksheets:
                sheet['A{0}'.format(row)]=student_admno
                sheet['B{0}'.format(row)]=student_name
            book.save(os.path.join("Database","Students","Attendence.xlsx"))
            row+=1
            sheet2['A{0}'.format(row2)].value=student_admno
            sheet2['B{0}'.format(row2)].value=student_name
            sheet2['C{0}'.format(row2)]="Students"
            book2.save(os.path.join("Database","teachers_and_students.xlsx"))
            row2+=1
            cv2.imwrite(os.path.join("Database","Students","Images",student_class,student_rollno+".jpg"),student_image)
            trainer.train(list_images,int(student_admno))
        else:
            root.focus_set()            
    
    def setimage(image):
        global student_image
        student_image=cv2.flip(image,1)
        cv2image=cv2.cvtColor(student_image,cv2.COLOR_BGR2RGBA)
        img2=Image.fromarray(cv2image)
        img2=img2.resize((300,350),Image.ANTIALIAS)
        img2=ImageTk.PhotoImage(img2)
        root.geometry("400x640+500+5")
        root_label.configure(image=img2)
        root_label.image=img2

    def record():
        global list_images
        list_images=[]
        if(askokcancel("WARNING","Look at the camera\nand sit steady")):
            root.focus_set()
            count=0
            cam=cv2.VideoCapture(0)
            ret,t_img=cam.read()
            while(True):
                ret,img=cam.read()
                img=cv2.flip(img,1)
                gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                faces=detector.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5)
                
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    if(len(faces)==1):
                        count+=1
                        list_images.append(gray[y:y+h,x:x+w])
                cv2.imshow("image",img)
                k=cv2.waitKey(100)&0xff
                if(k==27):
                    break
                elif(count>=50):
                    break
            cam.release()
            cv2.destroyAllWindows()
            setimage(t_img)
        
    Button(F4,text="RECORD",width=10,height=2,command=record).pack(side=LEFT,pady=5,padx=5)
    Button(F4,text="CANCEL",width=10,height=2,command=root.destroy).pack(side=LEFT,pady=5,padx=5)
    Button(F4,text="SUBMIT",width=10,height=2,command=submit).pack(side=LEFT,pady=5,padx=5)

    root.bind("<Escape>",lambda e:root.destroy())
    root.bind("<Return>",lambda e: submit())
    root.mainloop()


if __name__=="__main__":
    addStudent()
