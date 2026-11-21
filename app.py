import cv2
from cv2.gapi import concatVert
face_cascade = cv2.CascadeClassifier("C:\\Users\\vigne\\OneDrive\\Desktop\\MYsql\\face and object\\haarcascade_frontalface_default.xml")

cap=cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  

codecs = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec for the output video
recorded=cv2.VideoWriter('output.avi', codecs, 20.0, (frame_width, frame_height))  # Create a VideoWriter object 

while True:
    ret, frame =cap.read()
    if not ret:
        print("Could not read from webcam")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    recorded.write(frame)  # Write the frame to the output video file
    cv2.imshow('frame', frame)  # Display the frame in a window

    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

     #scale factor 1.1----zoom level  
     # minNeighbour= 5  it will check five time for the that it is a orginal face 
     # 3 - lose checking and 5 -- safe checking  6-- strict checking 
      # (x,y)- top = left corner  
      #((x+w,y+h)
       #x--how far from the left
       #y-how far from top 
       #w-- widht of afce
       #h-- height of face  
    cv2.imshow("webcam face detection ",frame)

    if cv2.waitKey(1)& 0xFF==ord('q') : 
        break

cap.release()
cv2.destroyAllWindows()


     