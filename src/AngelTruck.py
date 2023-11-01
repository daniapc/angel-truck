from vidSLAM.DataVisual import DataVisual
from vidSLAM.SLAM import Slam
from yolo.YoloService import Yolo
import cv2
import os
import base64

from Pillow import Pillow

class AngelTruck:
    def __init__(self, video, fov):
            self.video = video
            self.fov = fov
            self.images = []
            self.image_dict = {}
            self.objects_dict = {}

    def video_analisys(self):
        video_name = self.video
        fov = self.fov

        # video_name = args.video
        video_path = os.getcwd() + '/data/' + video_name
        cap = cv2.VideoCapture(video_path)
        count = 0
        slam = Slam(fov)
        yolo_path = os.getcwd()

        images = []
        image_dict = {}
        objects_dict = {}

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
                        str_index = str(index_lm_xyz)

                        file_name = video_name.replace('.mp4', str_index + '.jpg')
                        
                        cv2.imwrite(yolo_path + '/src/yolo/darknet/data/' + file_name, frame)

                        image_dict[index_lm_xyz] = file_name
                        # objects_dict[index_lm_xyz] = len(images)

        # se houver detecção de objetos, é adicionado o frame que fez a detecção

                    except:
                        continue

        # Press Q on keyboard to exit
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

        # Break the loop
            else:
                break

        cap.release()
        # cv2.destroyAllWindows()

        slam.buildMap()

        self.images = images
        self.image_dict = image_dict
        self.objects_dict = objects_dict

    def yolo_analysis(self):

        video_name = self.video
        # images = self.images
        image_dict = self.image_dict
        # objects_dict = self.objects_dict

        yolo = Yolo(video_name, os.getcwd())
        yolo_dict = {}

        i = 0
        for image_key in image_dict:
            file_name = image_dict[image_key]

            yolo_out = yolo.execute_yolo(file_name)

            if len(yolo_out) > 0:
                yolo_dict[image_key] = yolo_out

                # yolo_image = yolo.export_frame(image_key)
                # insert_index = objects_dict[image_key]

                # for iterator in range(30):
                #     images.insert(insert_index + i*30, yolo_image)
                
                # i = i + 1

            yolo.remove_file(image_key)

        # out_video_name = 'output.avi'
        # height, width, layers = images[0].shape

        # video = cv2.VideoWriter(out_video_name, 0, 60, frameSize=(width,height))
        
        # for image in images:
        #     video.write(image)
        # video.release()

        with open('yolo_dict.txt', 'w') as f:
            print(yolo_dict, file=f)

    def delete_yolo_files(self):
        image_dict = self.image_dict
        yolo = Yolo(self.video, os.getcwd())

        for image_key in image_dict:
            yolo.remove_file(image_key)


    def draw_map(self, x_len, y_len, tam):
        pillow = Pillow(x_len, y_len, tam)
        pillow.get_map()

    def encode_map(path):
        encoder = open("map.png","rb")
        encoded = base64.b64encode(encoder.read()).decode()
        encoder.close()

        return encoded