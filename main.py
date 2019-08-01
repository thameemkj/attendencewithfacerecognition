from tkinter import *
from tkinter.messagebox import askyesno,showinfo,showerror
import cv2
import os
import time
from Interface import adminWindow
import openpyxl as xl
import mark_attendence

book=xl.load_workbook(os.path.join("Database","teachers_and_students.xlsx"))
sheet=book.active
row=1
while(True):
    if(sheet['A{0}'.format(row)].value==None):
        break
    row+=1
ids=[cell[0].value for cell in sheet['A1:A{0}'.format(row)]]
names=[cell[0].value for cell in sheet['B1:B{0}'.format(row)]]
cats=[cell[0].value for cell in sheet['C1:C{0}'.format(row)]]
root=Tk()
root.title("Register")
root.geometry("300x300+500+150")
F1=Frame(root)
F1.pack(side="left")

def get_name_cat(unique_id):
    return (names[ids.index(str(unique_id))],cats[ids.index(str(unique_id))])

def takeAttendence():
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    cond=True
    try:
        recognizer.read(os.path.join("Database","Trainedfile","main.yml"))
    except:
        showerror("Error","You have not added anyone to the database")
        cond=False
    detector=cv2.CascadeClassifier(os.path.join("Trainer","haarcascade_frontalface_default.xml"))
    cam=cv2.VideoCapture(0)
    cam.set(3,640)
    cam.set(4,480)
    
    while(cond):
        ret,img=cam.read()
        img=cv2.flip(img,1)
        cv2.imshow("Camera",img)
        k=cv2.waitKey(10)&0xff
        if(k==27):
            break
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=detector.detectMultiScale(gray,1.2,5)
        for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                if(len(faces)==1):
                    id,confidence=recognizer.predict(gray[y:y+h,x:x+w])
                    if(confidence<40):
                        name,cat=get_name_cat(id)
                        if(askyesno("Confirmation","Are you {} ?".format(name))):
                            if(mark_attendence.mark(str(id),cat)):
                                showinfo("Done","Attendance has been marked for {} .".format(name))
                                cond=False
                            else:
                                showerror("Error","Couldn't mark attendance for {} .".format(name))
                                cond=False                         
                    else:                    
                        cv2.putText(img,"Cant recognize you",(x+5,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)                
    cam.release()
    cv2.destroyAllWindows()  
            
Button(F1,text="Admin",width=15,height=3,command=adminWindow.adminWindow).pack(padx=100)
Button(F1,text="Take My Attendence",width=20,height=3,command=takeAttendence).pack()

root.mainloop()


