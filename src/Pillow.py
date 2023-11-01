from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#x_len = 800
#y_len = 600

class Pillow:
    def __init__(self, x_len, y_len, tam):
        self.x_len = x_len
        self.y_len = y_len
        
        self.x_lines = []
        self.y_lines = []
        self.x_cam = []
        self.y_cam = []

        self.tam = tam

        self.yolo_dict = {}

    def get_map(self):
        tam = self.tam

        img = Image.new('RGB', (self.x_len, self.y_len), color='white')
        I1 = ImageDraw.Draw(img)

        self.x_lines = self.get_list_from_txt('lm_x.txt', self.x_len)
        self.y_lines = self.get_list_from_txt('lm_y.txt', self.y_len)
        self.x_cam = self.get_list_from_txt('cam_x.txt', self.x_len)
        self.y_cam = self.get_list_from_txt('cam_y.txt', self.y_len)

        self.yolo_dict = self.get_yolo_dict_from_txt('yolo_dict.txt')

        camx0 = self.x_cam[0]
        camy0 = self.y_cam[0]

        for i in range(len(self.x_lines)):
            x1 = self.x_lines[i]
            y1 = self.y_lines[i]

            I1.ellipse((y1, x1, y1+tam, x1+tam), fill = 'blue', outline ='blue')

        for i in range(1, len(self.x_cam)):
            camx1 = self.x_cam[i]
            camy1 = self.y_cam[i]

            I1.ellipse((camy1, camx1, camy1+tam, camx1+tam), fill = 'red', outline ='red')

        I1.ellipse((camy0, camx0, camy0+tam, camx0+tam), fill = 'green', outline ='green')

        font = ImageFont.truetype(font="data/arial.ttf",size=tam*2)

        for i in range(len(self.x_lines)):
            x1 = self.x_lines[i]
            y1 = self.y_lines[i]
            if i in self.yolo_dict:
                object = self.yolo_dict[i]
                I1.text((y1, x1), font=font, text=object, fill='black')

        img.show()
        
        # Save the edited image
        img.save("map.png")


    def get_list_from_txt(self, path, ref):
        f = open(path, "r")

        all_lines = f.readlines()
        coord_list = []

        for line in all_lines:
            coord_list.append(float(line[:-1])*10+ ref/2)

        return coord_list

    def get_yolo_dict_from_txt(self, path):
        f = open(path, "r")

        yolo_dict_str = f.read()
        if '{}' in yolo_dict_str:
            return {}
        yolo_dict_str = yolo_dict_str[1:]
        yolo_dict_str = yolo_dict_str[:-3]
        yolo_dict_str = yolo_dict_str.replace('[', '').replace(' ', '').replace('\'','')
        temp_list = yolo_dict_str.split('],')

        yolo_dict = {}
        for element in temp_list:
            index = element.index(':')
            key = int(element[0:index])
            value = element[index + 1:]
            yolo_dict[key] = value
        
        return yolo_dict

# pillow = Pillow(800, 600, 7)
# pillow.get_map()




