from flask import Flask, render_template, Response, redirect
from queue import Queue
app = Flask(__name__)
import json
import numpy as np
import cv2
from threading import Thread
import webbrowser

q = Queue(maxsize=10)

def compare_list(list1, list2):
    for element in list1:
        if element in list2:
            return True
    return False

data = {'msg':'','anm':[]}
# Load YOLOv3 model
net = cv2.dnn.readNet('yolov3.cfg', 'yolov3.weights')
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = net.getUnconnectedOutLayersNames()
cap : cv2.VideoCapture = None


animal_list = ["elephant", "bear", "zebra", "giraffe"]


def gen_frames():
    while True:
        ret, img = cap.read()
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(
            img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)   
        labs = []
        for lab in class_ids:
            labs.append(classes[lab])
        labs = list(set(labs))


        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_SIMPLEX
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(img, (round(x), round(y)),
                                (round(x + w), round(y + h)), color, 2)
                cv2.putText(img, label + ' ' + str(round(confidence, 2)),
                            (round(x), round(y) - 5), font, 0.5, color, 2)
            
        if  compare_list(labs, animal_list):
            for animal in animal_list:
                if animal in labs:
                    msg = f"Wild Animal Detected: {animal}"
                    break
        else:
            msg = "No Wild Animals"
        data['msg'] = msg
        data['anm'] = labs
        with open('static/data.json', 'w') as file:
            json.dump(data, file)

        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()

        try:
            q.put(img, block=False)
        except:
            pass
    try:
        cap.release()
    except: pass




def capture():
    while True:
        img = q.get()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)
        Thread(target=gen_frames).start()
    return Response(capture(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host = "0.0.0.0",debug=True)
