import cv2
import face_recognition
import picamera
import numpy as np
from requests import get
import base64
from tkinter import *
from PIL import Image,ImageTk
import tkinter.font as tkFont
from tkinter import ttk
import time
import random

'''
for the ihu.py to work, you will have to have the ihufied app running in background or online. if online, change
the url variable on line 17 to the online url.
'''
root=Tk()
root.title("IHUFIED")
root.attributes('-alpha',0.5)
root.geometry('1024x600')

#Font styles
logostyle=tkFont.Font(family="Lucida Grande", size=12)
fontstyle=tkFont.Font(family="Hevetical",size=20)
papystyle=tkFont.Font(family="papyrus",size=10)

#colours
skyblue="#74d9f6"
lightgray="#bbbec2"
ihugrey="#303337"
ihublack="#212121"
ihublue="#878dbd"
buttonblue="#007bff"



#CREATING ALL FRAMES
titleBar=LabelFrame(root,bg=ihugrey, width=1024, height=600)
titleBar.grid(row=0,column=0, columnspan=12, sticky="EW", ipadx=0, ipady=0, padx=0, pady=0)

WelcomeFrame=LabelFrame(root,bg="#303337", width=1024, height=600)
WelcomeFrame.grid(row=1,column=0,sticky="EW", columnspan=12,padx=0,pady=0)
WelcomeFrame.grid_propagate(0)

# WelcomeFrame.rowconfigure(0,weight=4)
# WelcomeFrame.columnconfigure(0,weight=4)

#open background image
bg=Image.open("background.png")

#resize
resized_bg=bg.resize((1024,600),Image.ANTIALIAS)
 
New_bg =ImageTk.PhotoImage(resized_bg)
back_ground=Label(WelcomeFrame,image=New_bg)
back_ground.place(x=0,y=0,relwidth=1,relheight=1)


logo=Label(titleBar,text="IHUFIED!", font=logostyle,bg=ihugrey,fg="white").grid(row=0,column=0,padx=0,pady=0)


#FRAMES END
#EXAM MODE

#DESTROYER FUNCTION IS USED TO CLEAR SCREEN
def destroyer():
    for previous in WelcomeFrame.winfo_children():
        previous.destroy()
    for prev in titleBar.winfo_children():
        prev.destroy()
    logo=Label(titleBar,text="IHUFIED!", font=logostyle,bg=ihugrey, fg="white")
    logo.grid(row=0,column=1,padx=0,pady=0)
    home=Button(titleBar,text="Analyze video",font=logostyle,padx=0,pady=0,bg=buttonblue,fg="white",borderwidth=0,border=0)
    home.grid(row=0,column=8,padx=(765,0),ipady=0)
    
    
def destroyed(message):
    for previous in WelcomeFrame.winfo_children():
        previous.destroy()
    for prev in titleBar.winfo_children():
        prev.destroy()
    logo=Label(titleBar,text=message, font=logostyle,bg=ihugrey, fg="white")
    logo.grid(row=0,column=0,padx=0,pady=0)
    back_button=Button(titleBar,
                       text="Back",font=logostyle,padx=10,
                       pady=0,fg="white",bg=buttonblue,command= exam_setup).grid(row=0,column=1,padx=300)

#     home=Button(titleBar,text="Analyze video",font=logostyle,padx=0,pady=0,bg=buttonblue,fg="white",borderwidth=0,border=0)
#     home.grid(row=0,column=8,padx=(357,0),ipady=0)

#EXAMSETUP IS USED TO COLLECT THE COURSE CODE
def exam_setup():
    destroyer()

    #collect input to set the mode for the exam(course been taken)

    code_label=Label(WelcomeFrame,text="Enter Course Code: ",bg=ihugrey,fg="white").grid(row=0,column=0,padx=(250,5),pady=(195,10))
    course_code=Entry(WelcomeFrame,width=40)
    course_code.grid(row=0,column=1,pady=(200,10), padx=(40,100))
    back_button=Button(titleBar, text="Back",font=logostyle,padx=10,pady=0,fg="white",bg=buttonblue,command= back).grid(row=0,column=0)
    
    #this takes the input and call the function fetch details
    submit_code= Button(WelcomeFrame,text="Submit",bg=buttonblue,border=0,fg="white",command=lambda:fetch_details(course_code.get())).grid(row=1,column=1,pady=(0,100), padx=(0,20))
def back():
    global New_bg
    for previous in WelcomeFrame.winfo_children():
        previous.destroy()
    for prev in titleBar.winfo_children():
        prev.destroy()
    #open background image
    bg=Image.open("background.png")

    #resize
    resized_bg=bg.resize((1024,600),Image.ANTIALIAS)
     
    New_bg =ImageTk.PhotoImage(resized_bg)
    back_ground=Label(WelcomeFrame,image=New_bg)
    back_ground.place(x=0,y=0,relwidth=1,relheight=1)


    logo=Label(titleBar,text="IHUFIED!", font=logostyle,bg=ihugrey,fg="white").grid(row=0,column=0,padx=0,pady=0)


    #WELCOME PAGE/FRAME
    welcome=Label(WelcomeFrame,text="Welcome to the Ihufied Client Side!", font=fontstyle,bg="#ffffff")
    welcome.grid(row=0, column=0,padx=150, pady=(160,0))
    choice=Label(WelcomeFrame,text="Kindly select a work mode below: ",font=logostyle,bg="#ffffff").grid(row=1,column=0,pady=(0,5),padx=10)
    exam_mode=Button(WelcomeFrame,text="EXAM MODE",font=logostyle,bg="#ffffff",command=exam_setup,border=0).grid(row=3,column=0,pady=(20,10),padx=10)
    video=Button(WelcomeFrame,text="ANALYSE VIDEO",font=logostyle,bg="#ffffff",border=0).grid(row=4,column=0,padx=10,pady=(0,20))

#img=ImageTk.PhotoImage(Image.open("registered_student"))
needed_data = {}
all_details = {}
global seat_number
seat_number = []
#img=ImageTk.PhotoImage(Image.open('registered_student_img/2015364011.png'))
#imgl=Label(WelcomeFrame,image=img)

    
#DECODE IMAGE DECODES THE API CALL RESULT AND SAVES THE GENERATED FACE ENCODINGS
def decode_images(students):
    destroyer()
    '''
    this function is used to change the students images to raw format and store in a folder created
    '''
    back_button=Button(titleBar,
                       text="Back",font=logostyle,padx=10,
                       pady=0,fg="white",bg=buttonblue,command= exam_setup).grid(row=0,column=0)
    ini_text='{} students are registered for this course'.format(len(students))
    ini_message=Label(WelcomeFrame,text=ini_text,font=papystyle,bg=ihugrey,fg=ihublue)
    ini_message.grid(row=1,column=1,pady=(195,0),padx=(350,0))
    for student in students:
        all_details[str(student['reg_no'])] = student
        '''
            the next three lines converts/encodes the string formatted image back to base64 (refer to project ihufied/app/main/views.py line 35 for more understanding ), which is then decoded
            to raw image format and stored in the folder "registered_student_img" using the reg number of the 
            student.
        '''
        image_encode = student['img'].encode('utf-8')
        image_decode = base64.decodebytes(image_encode)
        image_result = open('registered_student_img/{}.png'.format(student['reg_no']), 'wb')
        image_result.write(image_decode)
        
        #this performs the openCV function on the image and stores it in the key 'img' of the students dictionary
        cv_img = cv2.imread('registered_student_img/{}.png'.format(student['reg_no']),1)

        #NB. if line 40 returns error because of the 'image_decode' change 'image_decode' to 'registered_student_img/{}'.format(student['reg_no'])
        back_button=Button(titleBar, text="Back",font=logostyle,padx=10,pady=0,fg="white",bg=buttonblue,command= back).grid(row=0,column=0)
        #change the image value to the reg number of the student because that is what is used to save it in  the folder
        student['img'] = cv_img

        #this inserts the students regnumber and image to the needed_data dictionary
        needed_data[student['reg_no']] = student['img']  
        count = 0
        missed_face_locations = []
        known_encodings = []
        student_regno = []
        for reg_no,img in needed_data.items():
             face_locations = face_recognition.face_locations(img)
             if face_locations:
                 count = count + 1
                 loc_message="Generating face prints in {0} of {1}".format(count,len(students))
                 Getting_message= Label(WelcomeFrame, text=loc_message, font=papystyle,bg=ihugrey,fg=ihublue)
                 Getting_message.grid(row=2,column=1,padx=(320,0))
                 root.update_idletasks()
                 time.sleep
                 known_encoding = face_recognition.face_encodings(img,model="large")[0]
                 known_encodings.append(known_encoding)
                 student_regno.append(reg_no)       
             else:
#                  no_loc="No location found for student ID: {}".format(reg_no)
#                  noloc_message= Label(WelcomeFrame, text=no_loc, font=logostyle)
#                  noloc_message.grid(row=3,column=1)
                 missed_face_locations.append(reg_no)
        seat_number =  random.sample(range(1,count+1), count)
        print(seat_number)
        print("This is count: {}".format(count))
        if missed_face_locations:
#              def view_list():
#                  face_frame=LabelFrame(WelcomeFrame,text="missed",width=200,height=200)
#                  face_frame.grid(row=1,column=2)
#                  for regno in missed_face_location:
#                      no_face=Label(Welcome)
             missed_loc= "No faceprint generated for the following student ID(s):".format(missed_face_locations)
             missed_loc_message= Label(WelcomeFrame, text=missed_loc, font=papystyle,bg=ihugrey,fg=ihublue)
             missed_loc_message.grid(row=3,column=1,padx=(250,5))
             for stu in missed_face_locations:
                 missed=Label(WelcomeFrame,text=stu,font=papystyle, bg=ihugrey,fg=ihublue)
                 missed.grid(row=3,column=2)
                 
        if len(known_encodings) + len(missed_face_locations) == len(students):
            done=Label(WelcomeFrame,text="System is ready for verification",font=papystyle, bg=ihugrey,fg=ihublue)
            done.grid(row=2,column=1,padx=(320,0))
            Verify=Button(WelcomeFrame,text='Start verification',font=papystyle,bg=buttonblue,border=0,borderwidth=0, command=lambda:start_verification(known_encodings,student_regno,all_details,seat_number))
            Verify.grid(row=4,column=1,padx=(330,10), pady=(10,75))
        
        #FETCH DETAILS IS USED TO DO THE API CALL
def fetch_details(coursecode):
    destroyer()
    back_button=Button(titleBar, text="Back",font=logostyle,padx=10,
                       pady=0,fg="white",bg=buttonblue,command= back).grid(row=0,column=0)
    message= "Remotely fetching student details,ensure network connection is strong..."
    loading=Label(WelcomeFrame,text=message, font=papystyle,bg=ihugrey,fg=ihublue)
    loading.grid(row=0,column=1,pady=(195,10),padx=(250,5))
    progress_bar=ttk.Progressbar(WelcomeFrame,orient=HORIZONTAL,length=300,mode='determinate')
    progress_bar.grid(row=2,column=1,pady=(0,100),padx=(250,5))
#     
    
    #this is the url where the details are being fetched from
    #this is the url where the details are being fetched from
    url = 'http://ihufied-ihu.herokuapp.com/'

    #in the app/main/views.py the route to obtain students info is getuser
    url_course_code = url+'getuser/{}'.format(coursecode)


    
    '''
    execute the fetch function and store them
    The result is already a dictionary which contains the students firstname, lastname, reg_no, and img.
    The img is encoded in base64 which will be decoded in line 64
    '''
            
    reg_students = get(url_course_code).json()
    
    for x in range(5):
        progress_bar['value'] +=20
        root.update_idletasks()
        time.sleep(1)
        if reg_students and progress_bar['value'] == 60 :
            get_ready=Label(WelcomeFrame,text="Initializing parameter....", font=papystyle,bg=ihugrey,fg=ihublue)
            get_ready.grid(row=1,column=1,pady=(0,5),padx=(100,0))
        elif reg_students and progress_bar['value'] ==100:
            decode_images(reg_students)
def display_match(student,known_encodings, student_regno,students,seat_number):
    global New
    
    if student == 0:
        message = "No Match Found"
        destroyed(message)
        back_button=Button(WelcomeFrame, text="Next",
                       font=logostyle,padx=10,pady=0,fg="white",bg=buttonblue,
                       command=lambda: start_verification(known_encodings,
                                                          student_regno,students,seat_number))
        back_button.grid(row=1, column=4)
    else:
        
        message="Student with registration number {} has been verified!".format(student['reg_no'])
        destroyed(message)
        back_button=Button(WelcomeFrame, text="Next",
                       font=logostyle,padx=10,pady=0,fg="white",bg=buttonblue,
                       command=lambda: start_verification(known_encodings,
                                                          student_regno,students,seat_number))
        
        
        back_button.grid(row=1, column=4)
        print(seat_number)
        if seat_number:
         seat=seat_number.pop()
         seat_tag=Label(WelcomeFrame,text= "Seat Number:",font=papystyle,bg=ihugrey,fg=ihublue)
         seat_tag.grid(row=0,column=4)
         seat_no=Label(WelcomeFrame, text=seat,font=papystyle,bg=ihugrey,fg=ihublue)
         seat_no.grid(row=0,column=5)
        New =ImageTk.PhotoImage(Image.open("registered_student_img/{}.png".format(student['reg_no'])))
        pic=Label(WelcomeFrame,image=New)
        pic.grid(row=0,column=0)
        f_tag=Label(WelcomeFrame,text="First Name: ",font=papystyle,bg=ihugrey,fg=ihublue)
        f_tag.grid(row=2,column=0,padx=(0,200))
        fname=student['firstname']
        firstname=Label(WelcomeFrame,text=fname,font=papystyle,bg=ihugrey,fg=ihublue)
        firstname.grid(row=2,column=1,padx=0)
        
        l_tag=Label(WelcomeFrame,text="Last Name: ",font=papystyle,bg=ihugrey,fg=ihublue)
        l_tag.grid(row=3,column=0,padx=(0,200))
        lname=student['lastname']
        lastname=Label(WelcomeFrame,text=lname,font=papystyle,bg=ihugrey,fg=ihublue)
        lastname.grid(row=3,column=1,padx=0)
        
        reg_tag=Label(WelcomeFrame,text="Registration No: ",font=papystyle,bg=ihugrey,fg=ihublue)
        reg_tag.grid(row=1,column=0,padx=(0,180))
        rnum=student['reg_no']
        regi_no=Label(WelcomeFrame,text=rnum,font=papystyle,bg=ihugrey,fg=ihublue)
        regi_no.grid(row=1,column=1,padx=0)
    
    
def start_verification(known_encodings,student_regno,student,seat_number):
     
  #initialize flag variable to y
     flag = 'y' 
     
     while flag.lower() == 'y':
      
           # Get a reference to the Raspberry Pi camera.
        camera = picamera.PiCamera()
        camera.resolution = (320, 240)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        
        #this while loop that is continuously reading the frames in the video and getting locations of the faces in the fram.
        face_locations = []
        unknown_encoding = []
        while True:
            
                # Grab a single frame of video from the RPi camera as a numpy array
              camera.capture(output, format="rgb")

                #Resize frame for faster face_recognition computation
              small_frame = cv2.resize(output, (0,0), fx=0.25,fy=0.25)

              #covert image to RGB color space
              rgb_small_frame = small_frame[:,:,::-1]

              #covert image to BGR color space
              frame = output[:,:,::-1]

     
              face_locations = face_recognition.face_locations(rgb_small_frame)
              cv2.imshow('Ihufied', frame)
              cv2.waitKey(1)
          
              if  len(face_locations) > 1:
                  cv2.destroyAllWindows()
                  camera.close()
                  #print("Multiple Faces detected!")
                  multiple_face=output    
                  for (top,right,bottom,left) in face_locations:
     
                      #Scale back up face locations
                      top *= 4
                      right *= 4
                      bottom *= 4
                      left *= 4
     
                      #Draw a box around the face
                      cv2.rectangle(multiple_face, (left,top),(right,bottom),(0,0,255),2)
     
                  #Draw a label below the face
                      cv2.rectangle(multiple_face,(left,bottom-35),(right,bottom),(0,0,255),cv2.FILLED)
                      font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                      cv2.putText(multiple_face,"Multiple face detection",(left+6,bottom-6),font,0.5,(255,255,255),1)
                  cv2.imshow('Multiple Image Error',frame)
                  cv2.waitKey(1000)
                  cv2.destroyWindow('Multiple Image Error')
                  camera.close
                  break
     
              elif len(face_locations) == 1:
                  print("A student is in position")
                  cv2.destroyAllWindows()
                  camera.close()
                  unknown_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations, model="large")
                  match = face_recognition.compare_faces(known_encodings,unknown_encoding[0], tolerance=0.45)
                  for (top,right,bottom,left) in face_locations:
     
                      #Scale up face locations
                      top *= 4
                      right *= 4
                      bottom *= 4
                      left *= 4
     
     
                      #Draw a label below the face
                      cv2.rectangle(output,(left,bottom-30),(right,bottom),(0,255,0),cv2.FILLED)
                      font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                      cv2.putText(output,"Verifying",(left+6,bottom-6),font,0.5,(255,255,255),1)
                      cv2.imshow('Verification',frame)
                      print("Captured student image, Verifying...Verification window would dissappear after 10s")
                      cv2.waitKey(500)
                      cv2.destroyAllWindows()
                      camera.close()
                      break
                  if True in match:
                      print('A match has been found analyzing...')
                      match_index = match.index(True)
                      reg_no = student_regno[match_index]
                      
                      
                      #use the reg no to further process students info and display with necessary voice notification
                      
                      #DISPLAY STUDENT THAT HAS BEEN FOUND
                      display_match(student[str(reg_no)],known_encodings,student_regno,student, seat_number)  
                  else:
                      display_match(0,known_encodings,student_regno,student,seat_number)  


    
#WELCOME PAGE/FRAME
welcome=Label(WelcomeFrame,text="Welcome to the Ihufied Client Side!", font=fontstyle,bg="#ffffff")
welcome.grid(row=0, column=0,padx=170, pady=(160,0))
choice=Label(WelcomeFrame,text="Kindly select a work mode below: ",font=logostyle,bg="#ffffff").grid(row=1,column=0,pady=(0,5),padx=10)
exam_mode=Button(WelcomeFrame,text="EXAM MODE",font=logostyle,bg="#ffffff",command=exam_setup,border=0).grid(row=3,column=0,pady=(20,10),padx=10)
video=Button(WelcomeFrame,text="ANALYSE VIDEO",font=logostyle,bg="#ffffff",border=0).grid(row=4,column=0,padx=10,pady=(0,20))



root.mainloop()
