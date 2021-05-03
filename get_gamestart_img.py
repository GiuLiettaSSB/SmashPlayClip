import os,sys,glob,cv2,imagehash,shutil
from PIL import Image


def Image_identification(TARGET,TEST,threshold=15):
    SAVE = []
    for i in TARGET:
        count = 0
        target_hash = imagehash.average_hash(Image.open(i))
        for j in TEST:
            test_hash = imagehash.average_hash(Image.open(j))
            haming = abs(target_hash-test_hash)
            if haming<=threshold:
                count += 1
        if count>len(TEST)//4:
            SAVE.append(i)
        print("checked: ",i)
    return SAVE


if __name__ == '__main__':
    TARGET_DIR_PATH = sys.argv[1]
    TARGET_IMG_PATH = glob.glob(TARGET_DIR_PATH+"/*.jpg")
    TEST_IMG_PATH = glob.glob("positive_datas/*.jpg")

    SAVE_IMG_PATH = Image_identification(TARGET_IMG_PATH,TEST_IMG_PATH)

    for i in TARGET_IMG_PATH:
        if i not in SAVE_IMG_PATH:
           os.remove(i)
