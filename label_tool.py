import numpy as np
import cv2
import json
from os import listdir
from os.path import isfile, join
from datetime import datetime

def draw_context_line(img):
    for i in range(160, 720, 10):
        img= cv2.line(img,(0,i),(img.shape[1],i),(0,255,0),1)

def fill_lane(points_lines):
    for line in points_lines:
        for i in range(160, 720, 10):
            line.append(-2)

def locate_point(points_lines,num_line ,x, y ):
     new_x=-1,
     new_y=-1
     line =  points_lines[num_line]
     if(y<160):
        return  new_x, new_y

     pos_array = int(y/10) - 16
     if  pos_array >= len(line):
         return  new_x, new_y
     new_x = x
     line[pos_array] = new_x
     new_y = int(y/10)*10 +5
     return  new_x, new_y

def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    img = param[0]

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            new_x, new_y = locate_point(points_lines,param[1] ,x, y )
            #print(new_x, new_y )
            if new_y > 0:
                cv2.circle(img,(new_x,new_y),3 ,(255,0,0),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

    cv2.imshow('image',img)


def draw_final_points(img, points_lines):

    for i in range(4):
        line =  points_lines[i]
        y = 165
        for x in line:
            if x>0:
                cv2.circle(img,(x,y),4 ,(0,i*75,255),-1)
            y +=10


def create_img_label(points_lines, name ):

    img_label = {"lanes": points_lines, "h_samples": h_samples, "raw_file":"train/{}".format(name) }
    return img_label



drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
train_path = "C:/cam_context/train/"


h_samples = []
for i in range(160, 720, 10):
    h_samples.append(i)
img_files = [f for f in listdir(train_path) if isfile(join(train_path, f))]

set_labels = []

k = None
for name_file in img_files:
    current_line = 3
    points_lines = [ [],[],[],[]]
    fill_lane(points_lines)
    only_name = name_file
    name_file = train_path +name_file
    img = cv2.imread(name_file)
    img_copy = img.copy()
    draw_context_line(img)
    cv2.setMouseCallback('image',draw_circle)
    #cv2.imwrite(name_file.replace("png","jpg"),img )

    while(1):
        cv2.imshow('image',img)
        param = [img,current_line ]
        cv2.setMouseCallback('image',draw_circle,param)
        k = cv2.waitKey() & 0xFF

        if k == ord('m'):
            img =  img_copy.copy()
            draw_context_line(img)
            draw_final_points(img,points_lines)
            if(current_line>0):
                current_line -= 1

        elif k == ord('n'):
            break
        elif k == ord('z'):
            img =  img_copy.copy()
            draw_context_line(img)
            points_lines = [ [],[],[],[]]
            fill_lane(points_lines)
            current_line = 3
        elif k == 27:
            break
    img_label = create_img_label(points_lines, only_name)
    set_labels.append(img_label)

    if  k == 27:
        break

    now = datetime.now()
    str_time = now.strftime("%Y_%m_%d__%H_%M_%S")
    print("date and time:",str_time)
    file1 = open("train_label_{}.json".format(str_time),"w")
    for label  in set_labels:
        file1.writelines( str( label).replace("\'", "\"") +"\n")
    file1.close()
#with open('train_label.json', 'w') as outfile:
        #json.dump(set_labels, outfile,  indent=4)


cv2.destroyAllWindows()
