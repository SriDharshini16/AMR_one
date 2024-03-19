#!/usr/bin/env python3

import cv2 
import rospy
#import cv2
import mediapipe as mp
from geometry_msgs.msg import Twist
# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


cap = cv2.VideoCapture(-1)
print(cap.isOpened())


if not cap.isOpened():
	print("cannot open camera")
while True:
	rospy.init_node('susan',anonymous=True)
	ret, frame = cap.read()
	if not ret:
		break
	# Convert the frame to RGB
	frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# Detect hands in the frame
	results = hands.process(frame_rgb)

	if results.multi_hand_landmarks:
		for landmarks in results.multi_hand_landmarks:
		    # Assuming landmarks[8] corresponds to the tip of the index finger
		    index_finger_tip = landmarks.landmark[8]
		    
		    # Assuming landmarks[4] corresponds to the tip of the thumb
		    thumb_tip = landmarks.landmark[4]
		    
		    # Calculate the distance between index finger tip and thumb tip
		    distance = abs(index_finger_tip.y - thumb_tip.y)
		    vel_pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
		    vel_msg=Twist()
		    if distance < 0.05:
		    	print("Printing forward")
		    	vel_msg.linear.x=0.5
		    	vel_msg.angular.y=0.0
		    	vel_pub.publish(vel_msg)
		    else:
		    	print("Printing backward")
		    	vel_msg.linear.x=-0.5
		    	vel_msg.angular.y=0.0
		    	vel_pub.publish(vel_msg)
			# Code to control the printer to move backward

	cv2.imshow("Gesture Recognition", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()









# Initialize OpenCV
#cap = cv2.VideoCapture(0)

#while cap.isOpened():
 #   ret, frame = cap.read()
#    if not ret:
#        break
    
    
