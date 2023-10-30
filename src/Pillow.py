from PIL import Image
from PIL import ImageDraw

import json

x_len = 800
y_len = 600


img = Image.new('RGB', (x_len, y_len), color='white')

I1 = ImageDraw.Draw(img)

f = open('lm_x.txt', "r")

all_lines = f.readlines()
x_lines = []

for line in all_lines:
    x_lines.append(float(line[:-1])*10+ x_len/2)

f = open('lm_y.txt', "r")

all_lines = f.readlines()
y_lines = []

for line in all_lines:
    y_lines.append(float(line[:-1])*10+ y_len/2)

print(y_lines)

f = open('yolo_dict.txt', "r")

yolo_dict_str = f.read()
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

# for line in all_lines:
#     y_lines.append(float(line[:-1])*10+ y_len/2)

print(y_lines)

for i in range(len(x_lines)):
    x1 = x_lines[i]
    y1 = y_lines[i]

    I1.ellipse((x1, y1, x1+10, y1+10), fill = 'blue', outline ='blue')

for i in range(len(x_lines)):
    x1 = x_lines[i]
    y1 = y_lines[i]
    if i in yolo_dict:
        object = yolo_dict[i]
        I1.text((x1, y1), object, fill=(255, 0, 0))

img.show()
 
# Save the edited image
img.save("map.png")