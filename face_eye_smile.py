import cv2
import os
from datetime import datetime

path = cv2.data.haarcascades
face_cascade = cv2.CascadeClassifier(path + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(path + "haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier(path + "haarcascade_smile.xml")

cap = cv2.VideoCapture(0)

# Video settings (must match the webcam frame size)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:          # some webcams return 0
    fps = 20

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
save_folder = os.path.dirname(os.path.abspath(__file__))

recording = False
writer = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        roi_top = gray[y : y + h // 2, x : x + w]
        eyes = eye_cascade.detectMultiScale(roi_top, 1.1, 10)
        if len(eyes) > 0:
            cv2.putText(frame, "Eyes Detected", (x, y - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        roi_bottom = gray[y + h // 2 : y + h, x : x + w]
        smiles = smile_cascade.detectMultiScale(roi_bottom, 1.7, 20)
        if len(smiles) > 0:
            cv2.putText(frame, "Smiling", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Save the frame (with boxes and text) if recording
    if recording:
        writer.write(frame)
        # Red dot and REC label (shown on screen only, not saved)
        cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
        cv2.putText(frame, "REC", (50, 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Smart Face Detector", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        if not recording:
            name = datetime.now().strftime("recording_%Y%m%d_%H%M%S.mp4")
            file_path = os.path.join(save_folder, name)
            writer = cv2.VideoWriter(file_path, fourcc, fps, (width, height))
            recording = True
            print("Recording started:", file_path)
        else:
            recording = False
            writer.release()
            writer = None
            print("Recording stopped and saved")

    elif key == ord("q"):
        break

# Clean up
if writer is not None:
    writer.release()
cap.release()
cv2.destroyAllWindows()