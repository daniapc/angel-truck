import cv2 
import subprocess
import os

class Yolo:

    def __init__(self, video_name, path):
        self.pred_array = []
        self.video_name = video_name
        self.path = path

    def execute_yolo(self, file_name):

        # str_index = str(index)
        # file_name = self.video_name.replace('.mp4', str_index + '.jpg')
        
        # cv2.imwrite(self.path + '/src/yolo/darknet/data/' + file_name, image) 

        try:
            output = subprocess.run(
                'cd \'' + self.path + '/src/yolo/darknet/\' && ' +
                './darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights data/' + file_name + ' -out ' + file_name.replace('.jpg', 'pred'),
                shell=True,
                check=True,  # Behave like check_call
                text=True,  # Capture stdout, stderr as text, not bytes
                capture_output=True,  # Capture to internal .stdout, .stderr
            )
        except Exception as e:
            print(str(e))

        detected_objects = str(output.stdout).split('\n')
        detected_objects.pop(0)
        detected_objects.pop()

        return detected_objects
        
    def export_frame(self, index):
        str_index = str(index)
        file_name = self.video_name.replace('.mp4', str_index + 'pred.jpg')

        return cv2.imread(self.path + '/src/yolo/darknet/'+file_name)
    
    def remove_file(self, index):
        str_index = str(index)
        file_name = self.video_name.replace('.mp4', str_index + 'pred.jpg')

        src_file = self.path + '/src/yolo/darknet/data/'+file_name.replace('pred', '')
        pred_file = self.path + '/src/yolo/darknet/'+file_name

        if os.path.isfile(src_file):
            os.remove(src_file) 
        if os.path.isfile(pred_file):
            os.remove(pred_file) 