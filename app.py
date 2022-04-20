from flask import Flask, Response
from flask_cors import CORS
from waitress import serve
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

cap = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def getGolors(): 
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # RED
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_threshold = cv2.inRange(hsv_frame, low_red, high_red)
    countRed = np.sum(np.nonzero(red_threshold))

    if countRed >= 15000:
        red = True
    else:
        red = False

    # GREEN
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_threshold = cv2.inRange(hsv_frame, low_green, high_green)
    countGreen = np.sum(np.nonzero(green_threshold))

    if countGreen >= 15000:
        green = True
    else:
        green = False

    # BLUE
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_threshold = cv2.inRange(hsv_frame, low_blue, high_blue)
    countBlue = np.sum(np.nonzero(blue_threshold))

    if countBlue >= 15000:
        blue = True
    else:
        blue = False
        
    return {
        "Red": red, 
        "Green": green,
        "Blue": blue
    }
    

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000) #WAITRESS!