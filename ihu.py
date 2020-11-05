import cv2
import face_recognition

#collect input to set the mode for the exam(course been taken)
print('<===== Welcome to the Ihufied Client Side =====>')
coursecode = input('Enter the course code: ')

#fetch all registered students images for the particular course been taken using the api
print('Remotely fetching student details, make sure you have a strong network connection...')
img1 = cv2.imread('/home/pi/Desktop/Ihu/image/obama.jpg',1)
img2 = cv2.imread('/home/pi/Desktop/Ihu/image/nonso.jpg',1)

reg_students = {"2015364030":img1,"2015364080":img2} 

#generate the known encodings of these images and store in a list
print(f"Initializing paramaters for {coursecode}...")
count = 0
missed_face_locations = []
known_encodings = []
student_regno = []
for reg_no,img in reg_students.items():
    face_locations = face_recognition.face_locations(img)
    if face_locations:
        known_encoding = face_recognition.face_encodings(img)[0]
        known_encodings.append(known_encoding)
        student_regno.append(reg_no)
        count = count + 1
        print("Getting locations in {0} of {1}".format(count,len(reg_students)))       
    else:
        print("No location found for student Id {}".format(i))
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
    
#while loop  that is continuously reading the frames in the video and getting locations of the faces in the fram.
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
            print("Captured student image, Verifying...Verification window would dissappear after 5s")
            cv2.waitKey(10000)
            cv2.destroyAllWindows()
            cap.release
            break
    if True in match:
        print('A match has been found analyzing...')
        match_index = match.index(True)
        reg_no = student_regno[match_index]

        #use the reg no to further process students info and display with necessary voice notification
        print(f'Student ID: {reg_no} has been confirmed! ')
    else:
        print(f"No match found")

    print("<===== Press 'Y' to continue, 'N' to quit =====>")
    flag = input('Do you want to continue(Y/N): ')
        
