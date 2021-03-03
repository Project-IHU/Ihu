import cv2
import face_recognition
from requests import get
import base64

'''
for the ihu.py to work, you will have to have the ihufied app running in background or online. if online, change
the url variable on line 17 to the online url.
'''


#collect input to set the mode for the exam(course been taken)
print('<===== Welcome to the Ihufied Client Side =====>')
coursecode = input('Enter the course code: ')

#this is the url where the details are being fetched from
url = 'http://10.0.2.2:5000/'

#in the app/main/views.py the route to obtain students info is getuser
url_course_code = url+'getuser/{}'.format(coursecode)

#this dictionary holds only the regnumber associated with the image of the student
needed_data = {}

def decode_images(students):
    '''
    this function is used to change the students images to raw format and store in a folder created
    '''
    
    print('{} students are registered for this course'.format(len(students)))
    for student in students:
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

        #change the image value to the reg number of the student because that is what is used to save it in  the folder
        student['img'] = cv_img

        #this inserts the students regnumber and image to the needed_data dictionary
        needed_data[student['reg_no']] = student['img']

#fetch all registered students images for the particular course being taken using the api
print('Remotely fetching student details, make sure you have a strong network connection...')

'''
execute the fetch function and store them
The result is already a dictionary which contains the students firstname, lastname, reg_no, and img.
The img is encoded in base64 which will be decoded in line 64

'''
reg_students = get(url_course_code).json()

#img1 = cv2.imread('/home/pi/Desktop/Ihu/image/obama.jpg',1)
#img2 = cv2.imread('/home/pi/Desktop/Ihu/image/nonso.jpg',1)

decode_images(reg_students)
print(needed_data)
#reg_students = {"2015364030":img1,"2015364080":img2} 

#generate the known encodings of these images and store in a list
print(f"Initializing paramaters for {coursecode}...")
count = 0
missed_face_locations = []
known_encodings = []
student_regno = []
for reg_no,img in needed_data.items():
    face_locations = face_recognition.face_locations(img)
    if face_locations:
        count = count + 1
        print("Getting locations in {0} of {1}".format(count,len(reg_students)))
        known_encoding = face_recognition.face_encodings(img)[0]
        known_encodings.append(known_encoding)
        student_regno.append(reg_no)       
    else:
        print(f"No location found for student ID: {reg_no}")
        missed_face_locations.append(reg_no)

if missed_face_locations:
    print("No locations were found for the following student ID(s): {}".format(missed_face_locations))
print("Done.")
    
#sense distance of the student to the device to ensure student is within range and display necessary messages


#initialize flag variable to y
flag = 'y'

while flag.lower() == 'y':
    
    #create a video capture object
    cap = cv2.VideoCapture(0)
    
    #this while loop that is continuously reading the frames in the video and getting locations of the faces in the fram.
    face_locations = []
    unknown_encoding = []
    while True:
        ret, frame = cap.read()

        #Resize frame for faster face_recognition computation
        small_frame = cv2.resize(frame, (0,0), fx=0.25,fy=0.25)

        #covert image to RGB color space
        rgb_small_frame = small_frame[:,:,::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        cv2.imshow('Ihufied', frame)
        cv2.waitKey(1)
    
        if  len(face_locations) > 1:
            cv2.destroyAllWindows()
            cap.release()
            print("Multiple Faces detected!")

            for (top,right,bottom,left) in face_locations:

                #Scale back up face locations
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                #Draw a box around the face
                cv2.rectangle(frame, (left,top),(right,bottom),(0,0,255),2)

                #Draw a label below the face
                cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255),cv2.FILLED)
                font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                cv2.putText(frame,"Multiple face detection",(left+6,bottom-6),font,0.5,(255,255,255),1)
            cv2.imshow('Multiple Image Error',frame)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyWindow('Multiple Image Error')
                cap.release()
                break

        elif len(face_locations) == 1:
            print("A student is in position")
            cv2.destroyAllWindows()
            cap.release()
            unknown_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)
            match = face_recognition.compare_faces(known_encodings,unknown_encoding[0])
            for (top,right,bottom,left) in face_locations:

                #Scale up face locations
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                #Draw a box around the face
                cv2.rectangle(frame, (left,top),(right,bottom),(0,255,0),2)

                #Draw a label below the face
                cv2.rectangle(frame,(left,bottom-30),(right,bottom),(0,255,0),cv2.FILLED)
                font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                cv2.putText(frame,"Verifying",(left+6,bottom-6),font,0.5,(255,255,255),1)
            cv2.imshow('Verification',frame)
            print("Captured student image, Verifying...Verification window would dissappear after 10s")
            cv2.waitKey(10000)
            cv2.destroyAllWindows()
            cap.release
            break
    if True in match:
        print('A match has been found analyzing...')
        match_index = match.index(True)
        reg_no = student_regno[match_index]

        #use the reg no to further process students info and display with necessary voice notification
        print(f'Student ID: {reg_no} has been validated! ')
    else:
        print(f"No match found")

    print("<===== Press 'Y' to continue, 'N' to quit =====>")
    flag = input('Do you want to continue(Y/N): ')
        
