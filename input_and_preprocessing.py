import datetime
import json
import cv2

# processes 1st frame of video so that it can be put inside absdiff() function
def starter_function(video):
  frame_count=0
  while video.isOpened():
    ret,frame_no_1=video.read()
    if frame_count==0:
      background_frame=frame_no_1
      background_resized_frame = cv2.resize(background_frame,(640,480))
      background_grayed_frame = cv2.cvtColor(background_resized_frame,cv2.COLOR_BGR2GRAY)
      background_blurred_frame = cv2.GaussianBlur(background_grayed_frame, (21, 21), 0)
      break
  # return 
  return video,background_blurred_frame

# we read frames into a queue 
def read_frames(video, queue):
    while True:
        ret, frame = video.read()
        if not ret: break
        if not queue.full():
            queue.put(frame)

# applies processing techniques to the frames of video
def part1(frame,background_blurred_frame):
  # resizing image
  resized_frame = cv2.resize(frame,(640,480))
  # change to grayscale
  grayscaled_frame = cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
  # use gaussian blur
  blurred_frame = cv2.GaussianBlur(grayscaled_frame, (21, 21), 0)
  # difference frame to black out background
  differenced_frame = cv2.absdiff(background_blurred_frame,blurred_frame)
  # apply threshold 
  thresholded_frame = cv2.threshold(differenced_frame,25,255,cv2.THRESH_BINARY)[1]
  # dilate 
  dilated_frame = cv2.dilate(thresholded_frame,None,2)
  # detect contours
  ctr,_ = cv2.findContours(dilated_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  # return stmt
  return ctr



def part2(cntr):
  cntr_area = cv2.contourArea(cntr)
  if cntr_area > 500:
    timestamp = str(datetime.datetime.now())
    event_type = 'Motion Detected'
    metric = cntr_area
    event = {'timestamp':timestamp,'event_type':event_type,'metric':metric}
    event = json.dumps(event)
    return event
  else:
    return None