import os
import shutil

path = '/home/project/oyj/VOCdevkit/tube/7.扫地杆'
new_path = '/home/project/oyj/VOCdevkit/tube/JPEGIMAGES'

for root, dirs, files in os.walk(path):
    for i in range(len(files)):
        if files[i][-3:] == 'jpg':
            file_path = root + '/' + files[i]
            new_file_path = new_path + '/' + files[i]
            shutil.mov(file_path, new_file_path)
