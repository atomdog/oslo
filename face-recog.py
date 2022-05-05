import face_recognition
import cv2
import numpy as np
from keras.models import load_model
import collections
from fer import FER
import operator
import os

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.


# Load a second sample picture and learn how to recognize it.
def load_encodings():
    known_face_encodings = []
    directory = "faces"
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if(filename!=".DS_Store"):
                curr_image = face_recognition.load_image_file(os.path.join(root, filename))
                if(len(face_recognition.face_encodings(curr_image))>0):
                    curr = face_recognition.face_encodings(curr_image)[0]
                    known_face_encodings.append(curr)
    return(known_face_encodings)

# Create arrays of known face encodings and their names
known_face_encodings = load_encodings()
def load_names():
    known_face_names = []
    directory = "faces"
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if(filename!=".DS_Store"):
                name = filename[:len(filename)-4]
                known_face_names.append(name)
    return(known_face_names)

known_face_names = load_names()
model = load_model("emotionmodel.hdf5")
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
detector = FER(mtcnn=True)
process_this_frame = True
cv2.ocl.setUseOpenCL(False)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        op=detector.detect_emotions(rgb_small_frame)


        #rint(len(face_encodings))
        face_names = []
        counter = 0
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            print(face_locations[counter])
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if(name == "Unknown"):
                    top,right,bottom,left = face_locations[counter]
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    new_face = frame[top:bottom, left:right]
                    cv2.imshow("v", new_face)
                    cv2.imwrite("faces/face"+str(len(known_face_encodings))+".jpg", new_face)
                    known_face_encodings = load_encodings()
                    known_face_names = load_names()

            face_names.append(name)
            counter+=1
    process_this_frame = not process_this_frame
    print(face_names)
    faceemotions = []
    for x in range(0 , len(face_names)):
        faceemotions.append(["VOID"])
    ceb = [1000000]*len(face_names)
    counter=0
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        for x in range(0,len(ceb)):
            if x < len(op):
                eb = op[x]['box']
                etl = eb[0]*4
                etr = eb[1]*4
                ebl = eb[2]*4
                ebr = eb[3]*4
                if(((left-etl) + ((top-etr)))<ceb[counter]):
                    ceb[counter] = (left-etl) + ((top-etr))
                #print(op[x]['emotions'])
                    faceemotions[counter]=op[counter]['emotions']
            counter+1

    #print(len(faceemotions))
    # Display the results
    for (top, right, bottom, left), name, emotion in zip(face_locations, face_names, faceemotions):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if isinstance(emotion, list):
            pass
        else:
            emotetext = max(emotion.items(), key = lambda k : k[1])
            emotetext=str(emotetext)
            cv2.putText(frame, emotetext, (left + 6, bottom + 15), font, 0.5, (255, 255, 255), 1)
        #cv2.putText(frame, predicted_class, (right + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
