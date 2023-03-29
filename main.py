import cv2
import mediapipe as mp
import pyautogui
from datetime import datetime,timedelta

'''
mediapipe
opencv-python
pyautogui
'''

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
src_w, src_h = pyautogui.size()
difference_geo = 0
current_geo = 0
close_time = 0

while True:
    _, img_of_current_instance = cam.read()
    img_of_current_instance = cv2.flip(img_of_current_instance, 1)
    rgb_frame = cv2.cvtColor(img_of_current_instance, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = img_of_current_instance.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        #for another eye
        right = [landmarks[374],landmarks[386]]
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(img_of_current_instance, (x, y), 4, (0, 0, 0))
            if id == 1:
                screen_x = src_w * landmark.x
                screen_y = src_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)
                #
                current_geo = screen_y
            if id == 1 and (right[0].y - right[1].y) < 0.004:
            	pyautogui.scroll(difference_geo - current_geo)
            difference_geo = current_geo
            #
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            #cv2.rectangle(img_of_current_instance,(x,x+100),(y,y+50),(0,127,255))
            cv2.ellipsis(img_of_current_instance,(x,y),(8,4),color=(0,127,255))
            #cv2.circle(img_of_current_instance, (x, y), 8, (0,127,255))
        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)
        #
		if (left[0].y - left[0].y) < 0.004 and (right[0].y - right[1].y) < 0.004:
			if close_time == 0:
				close_time = datetime.now() + timedelta(seconds=5)
			if time.time() >= close_time:
				pyautogui.alert('virtual mouse is closed','virtual mouse','exit')
				break
		else:
			close_time = 0
		#
    cv2.imshow('Virtual mouse', img_of_current_instance)
    cv2.waitKey(1)




exit(0)