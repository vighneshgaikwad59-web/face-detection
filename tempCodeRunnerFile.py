import cv2

face_cascade = cv2.CascadeClassifier("Face & Object Detection/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("Face & Object Detection/haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier("Face & Object Detection/haarcascade_smile.xml")