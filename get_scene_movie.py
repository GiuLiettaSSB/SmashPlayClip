#from command.ps1
#> python get_scene_movie.py movie/xxx.mp4

import re,os,sys,glob
from datetime import datetime
import subprocess


def load_data(file):
    ffout_path = "output/"+os.path.splitext(os.path.basename(file))[0]+"/ffout.txt"
    f = open(ffout_path,mode='r',encoding='UTF-8')
    data = f.read()
    f.close()
    return data


def get_end_time(data):
    date_pattern = re.compile(r'time=(\d{2}:\d{2}:\d{2})')
    match = re.findall(date_pattern,data)
    dt = datetime.strptime(match[0], '%H:%M:%S')
    endTime = dt.hour * 60 * 60 + dt.minute * 60 + dt.second
    return endTime


def get_times(data):
    pattern = r'pts_time:([0-9]+\.[0-9]+)'
    timeList = re.findall(pattern, data)
    timeList = [float(n) for n in timeList]
    return timeList





def get_file_list(path):
    fileList = glob.glob(path+"/*.jpg")
    return fileList


def get_time_index(fileList):
    pattern = r'([1-9]+[0-9]*).jpg'
    index = []
    for i, fl in enumerate(fileList):
        temp = re.findall(pattern, fl)
        if(temp != None):
            index.append(temp[0])
    index = [int(n) - 1 for n in index]
    return index





def write_file(fileName, text):
    f = open(fileName, 'w')
    f.write(text)
    f.close()


def generate_movie(timeList,basename):
    text = ''
    for i in range(len(timeList)-1):
        delta = timeList[i + 1] - timeList[i]
        cmd = 'ffmpeg -ss %s' % timeList[i] + \
            ' -i movie/' + basename + '.mp4  -vcodec h264_nvenc -b:v 1000k -t %g' % delta + \
            ' movie/' + basename + '/' + basename + '%s.mp4' % i
        print(cmd)
        if not os.path.isdir('movie/'+ basename):
            os.makedirs('movie/'+ basename)
        subprocess.call(cmd, shell=True)
        text += 'file movie/'+ basename + '/' + str(i) + '.mp4\n'
    return text





if __name__ == '__main__':
    MOVIE_FULL_PATH = sys.argv[1] #movie/xxx.mp4
    BASE_NAME = os.path.splitext(os.path.basename(MOVIE_FULL_PATH))[0] #xxx
    IMAGE_DIR_PATH = "output/" + BASE_NAME + "/" #output/xxx
    
    FFOUT_DATA = load_data(MOVIE_FULL_PATH)
    ENDTIME_DATA = get_end_time(FFOUT_DATA)
    TIMELIST_DATA_TMP = get_times(FFOUT_DATA)
    
    
    IMAGE_PATH_LIST = get_file_list(IMAGE_DIR_PATH)
    IDX = get_time_index(IMAGE_PATH_LIST)


    TIMELIST_DATA = [TIMELIST_DATA_TMP[i] for i in IDX]
    TIMELIST_DATA.append(TIMELIST_DATA_TMP[-1])
    text = generate_movie(TIMELIST_DATA,BASE_NAME)

    write_file('mylist.txt', text)