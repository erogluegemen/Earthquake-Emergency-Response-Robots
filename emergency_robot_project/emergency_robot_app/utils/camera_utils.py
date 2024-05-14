import cv2
import threading
from ultralytics import YOLO

class VideoCamera(object):
    def __init__(self, width=640, height=640):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        threading.Thread(target=self.update, args=()).start()

        self.model = YOLO('emergency_robot_app/models/yolov8n.pt')  # yolov8s.pt(smaller model)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.labels = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush' ]

    def __del__(self):
        self.video.release() 
    
    def get_frame(self):
        ret, frame = self.video.read()
        if not ret:
            print("Error reading frame from camera")
            return None
    
        imgs=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.model(imgs,verbose=False) 
        for i in range(len(results[0].boxes)):
            x1,y1,x2,y2=results[0].boxes.xyxy[i]
            score=results[0].boxes.conf[i]
            label=results[0].boxes.cls[i]
            x1,y1,x2,y2,score,label=int(x1),int(y1),int(x2),int(y2),float(score),int(label)
            name=self.labels[label]
            if score<0.5 or name != 'person' :
                continue
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
            text= 'Person detected!' + ' ' + str(format(score, '.2f'))
            cv2.putText(frame, text,(x1, y1-10), self.font, 1.2, (255,0,255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    def update(self):
        while True:
            self.get_frame()

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')