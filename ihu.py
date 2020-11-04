from time import sleep,time
import cv2
import face_recognition

#collect input to set the mode for the exam(course been taken)
print('<===== Welcome to the Ihufied Client Side =====>')
coursecode = input('Enter the course code: ')

#fetch all registered students images for the particular course been taken using the api
print('Remotely fetching student details, make sure you have a strong network connection...')
img = cv2.imread('obama.jpg',1)

reg_students = {"2015364030":img} 

#generate the known encodings of these images and store in a list
print("Initializing paramaters for {}...".format(coursecode))
count = 0
missed_face_locations = []
student_encodings = []
for reg_no,img in reg_students.items():
    face_locations = face_recognition.face_locations(img)
    if face_locations:
        student_encoding = face_recognition.face_encodings(img)[0]
        student_encodings.append(student_encoding)
        count = count + 1
        print("Getting locations in {0} of {1}".format(count,len(reg_students)))       
    else:
        print("No location found for student Id {}".format(i))
        missed_face_locations.append(reg_no)

if missed_face_locations:
    print("No locations were found for the following student ID(s): {}".format(missed_face_locations))
print("Done.")
    
#sense distance of the student to the device to ensure student is within range and display necessary messages


#create a video capture object
cap = cv2.VideoCapture(0)

#while loop  that is continuously reading the frames in the video and getting locations of the faces in the fram.
face_locations = []
unknown_encodings = []
while True:
    ret, frame = cap.read()

    #Resize frame for faster face_recognition computation
    small_frame = cv2.resize(frame, (0,0), fx=0.25,fy=0.25)

    #covert image to RGB color space
    rgb_small_frame = small_frame[:,:,::1]

    face_locations = face_recognition.face_locations(rgb_small_frame)

    if  len(face_locations) > 1:
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
            cv2.putText(frame,"Multiple detection",(left+6,bottom-6),font,0.5,(255,255,255),1)
        cv2.imshow('Window',frame)
        if cv2.waitKey(1) == ord('q'):
            break

    elif len(face_locations) == 1:
        print("A student is in position")

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
        
