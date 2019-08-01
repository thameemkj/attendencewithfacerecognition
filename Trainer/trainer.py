import cv2
import numpy as np
import os
from . import merge_trained_files

def train(image_list,adm_no):
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(image_list,np.array([adm_no]*50))
    filename=str(adm_no)+".yml"
    recognizer.write(os.path.join("Database","Trainedfile",filename))
    merge_trained_files.merge(filename)
