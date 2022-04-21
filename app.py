from flask import Flask, Response, request
from flask_cors import CORS
from waitress import serve
from PIL import Image
import cv2
import numpy as np
import io
import base64

app = Flask(__name__)
CORS(app)

def stringToImage(base64_string):
    stripped = base64_string.replace("data:image/png;base64,", "")
    imgdata = base64.b64decode(stripped)
    return Image.open(io.BytesIO(imgdata))

def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# def gen_frames():
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#     cap.release()
#     cv2.destroyAllWindows()

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/capture')
# def getGolors(): 
#     cap = cv2.VideoCapture(0, cv2.CAP_V4L)
#     _, frame = cap.read()
#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
#     # RED
#     low_red = np.array([161, 155, 84])
#     high_red = np.array([179, 255, 255])
#     red_threshold = cv2.inRange(hsv_frame, low_red, high_red)
#     countRed = np.sum(np.nonzero(red_threshold))

#     if countRed >= 15000:
#         red = True
#     else:
#         red = False

#     # GREEN
#     low_green = np.array([25, 52, 72])
#     high_green = np.array([102, 255, 255])
#     green_threshold = cv2.inRange(hsv_frame, low_green, high_green)
#     countGreen = np.sum(np.nonzero(green_threshold))

#     if countGreen >= 15000:
#         green = True
#     else:
#         green = False

#     # BLUE
#     low_blue = np.array([94, 80, 2])
#     high_blue = np.array([126, 255, 255])
#     blue_threshold = cv2.inRange(hsv_frame, low_blue, high_blue)
#     countBlue = np.sum(np.nonzero(blue_threshold))

#     if countBlue >= 15000:
#         blue = True
#     else:
#         blue = False
        
#     return {
#         "Red": red, 
#         "Green": green,
#         "Blue": blue
#     }

@app.route('/capture', methods=["POST"])
def process_image():
    request_data = request.get_json(force=True)
    im = stringToImage(request_data['photo'])
    image = toRGB(im)

    # RED
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_threshold = cv2.inRange(image, low_red, high_red)
    countRed = np.sum(np.nonzero(red_threshold))

    if countRed >= 15000:
        red = True
    else:
        red = False
        
    # GREEN
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_threshold = cv2.inRange(image, low_green, high_green)
    countGreen = np.sum(np.nonzero(green_threshold))

    if countGreen >= 15000:
        green = True
    else:
        green = False

    # BLUE
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_threshold = cv2.inRange(image, low_blue, high_blue)
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

# if __name__ == "__main__":
#     serve(app, host='0.0.0.0', port=5000) #WAITRESS!