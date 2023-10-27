import DataVisual
import SLAM
import cv2
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument('-video', nargs='?', type=str, default='drive.mp4')
parser.add_argument('-video', nargs='?', type=str, default='lapti.mp4')
parser.add_argument('-fov', nargs='?', type=int, default=60)
args = parser.parse_args()

cap = cv2.VideoCapture(args.video)
count = 0
slam = SLAM.Slam(args.fov)
images = []

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    count = count + 1
    # Display the resulting frame
    frame = cv2.resize(frame, (800, 600))

    image = DataVisual.featureExtraction(frame)
    images.append(image)

    if count >= 10:
      count = 0
      try:
        lm_xyz = slam.runSlam(frame)
        print(len(lm_xyz))
      except:
        continue

    # Press Q on keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break

video_name = 'output.avi'
height, width, layers = images[0].shape

video = cv2.VideoWriter(video_name, 0, 60, frameSize=(width,height))

for image in images:
    video.write(image)
video.release()

# When everything done, release the video capture object
cap.release()

slam.buildMap()

# Closes all the frames
cv2.destroyAllWindows()




