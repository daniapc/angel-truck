from vidSLAM.DataVisual import DataVisual
from vidSLAM.SLAM import Slam
from yolo.YoloService import Yolo
import cv2
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('-video', nargs='?', type=str, default='lapti.mp4')
parser.add_argument('-fov', nargs='?', type=int, default=60)
args = parser.parse_args()

video_name = args.video
video_path = os.getcwd() + '/data/' + video_name
cap = cv2.VideoCapture(video_path)
count = 0
slam = Slam(args.fov)
yolo = Yolo(video_name, os.getcwd())

images = []
yolo_dict = {}

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    count = count + 1
    # Display the resulting frame
    frame = cv2.resize(frame, (800, 600))

    image = DataVisual.featureExtraction(frame)
    # images.append(image)

    if count >= 10:
      count = 0
      try:
        lm_xyz = slam.runSlam(frame)
        index_lm_xyz = len(lm_xyz)

        yolo_out = yolo.execute_yolo(frame, index_lm_xyz)

        # se houver detecção de objetos, é adicionado o frame que fez a detecção
        if len(yolo_out) > 0:
          yolo_dict[index_lm_xyz] = yolo_out

          yolo_image = yolo.export_frame(index_lm_xyz)
          for iterator in range(30):
            images.append(yolo_image)
        else:
          images.append(image)
        
        yolo.remove_file(index_lm_xyz)
      except:
        continue
    else:
      images.append(image)

    # Press Q on keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break

out_video_name = 'output.avi'
height, width, layers = images[0].shape

video = cv2.VideoWriter(out_video_name, 0, 60, frameSize=(width,height))

for image in images:
    video.write(image)
video.release()

with open('yolo_dict.txt', 'w') as f:
    print(yolo_dict, file=f)

# When everything done, release the video capture object
cap.release()

slam.buildMap()

# Closes all the frames
cv2.destroyAllWindows()




