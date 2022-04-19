import pygame
import pygame.camera
import cv2
import time
import os
import glob
import shutil
import numpy as np
import matplotlib.pyplot as plt
import imagehash
import face_recognition
from PIL import Image
import mysql.connector

#This function is used to move the photos of the criminals into the file folder where i run it
def Move():
    chdir=('C:/Users/David Baruzzo/OneDrive/Desktop/Criminal_Pictures')
    dst_dir =('C:/Users/David Baruzzo/OneDrive/Desktop/Detective_Program')
    for jpgfile in glob.iglob(os.path.join(chdir, "*.jpg")):
        shutil.move(jpgfile, dst_dir)

#This function is used to Save a picture of the criminals(By Name and Id) and save it
def Take_Save_Picture(y):
    x='{}.jpg'.format(y)
    camera = cv2.VideoCapture(0)
    while True:
        return_value,image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imshow('Press s for save the picture or q to quit from camera',gray)
        if cv2.waitKey(1)& 0xFF == ord('s') or cv2.waitKey(1)& 0xFF == ord('S'):
            print("Picture saved with success!")
            cv2.imwrite(x,image)
            break
        if cv2.waitKey(1)& 0xFF == ord('q') or cv2.waitKey(1)& 0xFF == ord('Q'):
             print("Quit from camera")
             break
    camera.release()
    cv2.destroyAllWindows()
    
#This is the connection of MYSQL with python   
db = mysql.connector.connect(host="localhost",
                             user="root",
                             passwd="Davide123",
                             database="test"
                             )

                             
mycursor= db.cursor()
#This function is used to find that there is not a duplicate Id
def TakeAllId():
    arr=[]
    mycursor.execute("select Id from criminallist2")
    for i in mycursor:
        arr+=i
        if x in arr==True:
            return True
            break
        else:
            print("The person requested is not exist in the system")
            return False
#This function is used to show all the details of the database table criminals         
def Show():
    print("\nFullname ","Id  ","Phone   ","Address    ","\n")
    mycursor.execute("select FullName,Id,Phone,Address from criminallist2") #name of mytable in MYSQL
    for i in mycursor:
        print(i)
        
#This function is used to delete an existing photo of the criminals
def DeletePicture(img_name):
    try:    
        path=('C:/Users/David Baruzzo/OneDrive/Desktop\Detective_Program')
        os.remove(path + '/' + img_name)
        #Must to check if file exists 
        if os.path.exists(path + '/' + img_name) is False:
            print("The photo has been successfully deleted")
        else:
            print("Picture requested is not exists")
            return True
    except FileNotFoundError as var:
        print("Error Picture requested is not exists")
#This function is used to delete an criminals of the database table criminals by Name,Id and his Picture
def DeleteByNameAndId():
    try:
        arr=[]
        arr2=[]
        mycursor.execute("select Id from criminallist2")
        for i in mycursor:
            arr+=i
        mycursor.execute("select FullName from criminallist2")
        for j in mycursor:
            arr2+=j
        name=str(input("Enter your Name: "))
        Id=int(input("Enter the ID to delete the criminal: "))
        if Id in arr and name.upper() in arr2 or name.lower() in arr2:
            mycursor.execute("DELETE FROM criminallist2 WHERE Id='{}'".format(Id))
            db.commit()
            print("This person is free!")
            y=name.upper()+(str(Id))
            x='{}.jpg'.format(y)
            DeletePicture(x)
        else:
            print("The person requested is not in the system")
    except ValueError as var:
        print("Error input!Please enter the correct input!")
        
#This function is used to insert an criminals of the database table criminals
def Insert():
    arr=[]
    mycursor.execute("select Id from criminallist2")
    for i in mycursor:
        arr+=i
    while True:
        try:
            name=str(input("Enter your Name: "))
            Id=int(input("Enter your ID: "))
            Phone=int(input("Enter your Phone: "))
            Address= str(input("Enter your Address: "))      #str    int    int       str     str
            y=name.upper()+(str(Id))
            Photo=Take_Save_Picture(y)
            if Address!="":
                break
        except ValueError as var:
            print("Error input!Please enter the correct input!")
    if Id not in arr:
        mycursor.execute("insert into criminallist2(FullName,Id,Phone,Address,Photo)values('{}','{}','{}','{}','{}')".format(name.upper(), Id, Phone,Address,Photo))
        db.commit()
        print("All details added successfully!")
    else:
        print("This Id is alredy exist...")
        
#This function is used to check a criminal if is existing in the database table criminals by a picture(recognition faces) 
def Check_TheCriminal(y):
    x='{}.jpg'.format(y)
    camera = cv2.VideoCapture(0)
    while True:
        return_value,image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imshow('image',gray)
        if cv2.waitKey(1)& 0xFF == ord('s') or cv2.waitKey(1)& 0xFF == ord('S'):
            print("Picture saved with success!")
            cv2.imwrite(x,image)
            DIRECTORY=('C:/Users/David Baruzzo/OneDrive/Desktop\Detective_Program')
            for f in os.listdir(DIRECTORY):
                if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
                    picture_of_me = face_recognition.load_image_file(f)
                    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
                    unknown_picture = face_recognition.load_image_file(x)
                    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
                    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
                    if results[0] == True:
                        print("Catch it!This guy is in the criminal system!",f)
                        img=cv2.imread(f,0)
                        cv2.imshow(f,img)
                        print("Press 0 to close all open windows")
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                    else:
                        print("This guy is NOT in the criminal system.")
            break
        
        if cv2.waitKey(1)& 0xFF == ord('q') or cv2.waitKey(1)& 0xFF == ord('Q'):
             print("Quit from camera")
             break
    camera.release()
    cv2.destroyAllWindows()
    
#This function is a simple inner join of 2 tables of the database( to show all details of the criminals)
def SeeAllDetailsOfCriminal():
    print("\nId  ","  Fullname  ","date_of_capture","release_date "," Address","\n")
    mycursor.execute("select Id,Fullname,date_of_capture,release_date,Address from criminalsdetails inner join criminallist2 using(Id,FullName) ;")
    for i in mycursor:
        print(i)
        
#This function is to show all the faces of the criminals existing
def AllFacesOfCriminals():
    print("Press 0 to close all open windows")
    DIRECTORY=('C:/Users/David Baruzzo/OneDrive/Desktop\Detective_Program')#the path of the pictures
    for f in os.listdir(DIRECTORY):
        if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
            img=cv2.imread(f,0)
            cv2.imshow(f,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        
        
#This function is the menu that I call all functions by user number input 
def DETECTIVE():
    print("\n")
    print("                                 WELCOME TO DETECTIVE MENU")
    print("\nTo choose from the menu you have to enter a number from 0 to 7")
    print("\n")
    print("1.Show all Criminals\n"
          "\n2.Insert a new criminal in the the database table\n"
          "\n3.Delete a criminal by ID\n"
          "\n4.Are you in the system?Let me take a picture of you\n"
          "\n5.Show all details of the Criminals\n"
          "\n6.View all the faces of the Criminals\n"
          "\n7.Delete specific picture from the system")
          
    choise = 10
    while  True:        
        try:
            if choise == 1:
                print("\nCriminals database")
                Show()
                DETECTIVE()
                break
                print("----------------------------------------------------------------")
            if choise == 2:
                Insert()
                DETECTIVE()
                break
            if choise ==3:
                print("Enter a ID to delete from database the criminal")
                DeleteByNameAndId()
                DETECTIVE()
                break
            if choise ==4:
                print("Are this guy a criminal?Let me check")
                while True:
                    try:
                        name=str(input("Enter your Name: "))
                        Id=int(input("Enter your ID: "))
                        if name!="" and Id!=0:
                            break
                    except ValueError as e:
                        print("Id must be a Number,please enter a correct ID")
                y=name.upper()+(str(Id))
                Check_TheCriminal(y)
                DETECTIVE()
                break
            if choise == 5:
                SeeAllDetailsOfCriminal()
                DETECTIVE()
                break
            if choise == 6:
                AllFacesOfCriminals()
                DETECTIVE()
                break
            if choise == 7:
                while True:
                    try:
                        name=str(input("Enter your Name: "))
                        Id=int(input("Enter your ID: "))
                        if name!="" and Id!=0:
                            break
                    except ValueError as e:
                        print("Id must be a Number,please enter a correct ID")
                y=name.upper()+(str(Id)+".jpg")
                DeletePicture(y)
                DETECTIVE()
                break
            elif choise ==0:
                print("                          THANK FOR USED DETECTIVE SYSTEM")
                break
            choise=int(input("\nCHOOSE FROM DETECTIVE MENU: "))
        except ValueError as var:
            print("Error input,you have to choose from the menu!")

DETECTIVE()
