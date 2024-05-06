# import cv2
# import base64
# import asyncio
# import websockets

# async def video_feed(websocket, path):
#     cap = cv2.VideoCapture(0)  # Use the camera at index 0 (default camera)

#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         _, buffer = cv2.imencode('.jpg', frame)
#         data = base64.b64encode(buffer.tobytes()).decode('utf-8')
#         await websocket.send(data)

# if __name__ == '__main__':
#     start_server = websockets.serve(video_feed, "10.10.165.56", 8000)  # Replace with your actual IP address
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

import base64
import asyncio
import json
import cv2
import websockets
import pygame
from ultralytics import YOLO
from pymongo import MongoClient

# Initialize pygame mixer
pygame.mixer.init()

# Load the alert sound file (replace with your sound file)
alert_sound = pygame.mixer.Sound("alert.mp3")

# Load YOLOv8 model
model = YOLO("yolov8x.pt")

# Connect to MongoDB database
# client = MongoClient("localhost", 27017)
# db = client["obstacle_detection"]
# collection = db["objects_detected"]

async def video_feed(websocket, path):
    cap = cv2.VideoCapture(0)  # Use the camera at index 0 (default camera)

    while True:
        success, frame = cap.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        data = base64.b64encode(buffer.tobytes()).decode('utf-8')

        # Object detection with YOLO
        results = model.predict(frame, classes=[0, 7])
        count = 0
        truck = 0

        for r in results:
            img = r.plot()
            for box in r.boxes:
                class_id = r.names[box.cls[0].item()]
                cords = box.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                confidence = round(box.conf[0].item(), 2)
                if class_id == "person":
                    count += 1
                    # Play alert sound
                    alert_sound.play()
                if class_id == "truck":
                    truck += 1
                    # Play alert sound
                    alert_sound.play()

        # Update MongoDB with object counts
        # document = {"people": count, "truck": truck}
        # existing_document = collection.find_one()

        # if existing_document is None:
        #     collection.insert_one(document)
        # else:
        #     collection.update_one({}, {"$set": document})

        # Send message to WebSocket
        message = {"data": data, "person_count": count, "truck_count": truck}
        await websocket.send(json.dumps(message))

if __name__ == '__main__':
    start_server = websockets.serve(video_feed, "192.168.205.180", 8000)  # Replace with your actual IP address
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()



