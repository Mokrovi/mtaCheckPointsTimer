import keyboard
import time
from FIndCheckpoint import find_point
import json
import cv2
import mss
import numpy

def convertor(timestart, timecheck):
    point = round(timecheck - timestart, 2)
    minutes = int(point // 60)
    seconds = point % 60
    return f"{minutes}:{seconds:.2f}".replace('.', ':')


previouse_lap = []
best_lap = []
mon = {"top": 400, "left": 0, "width": 1920, "height": 50}

while True:
    if keyboard.is_pressed('s') & keyboard.is_pressed('alt'):
        current_lap = []
        readble_time = []

        time.sleep(3)
        start_race_time = time.time()
        current_lap.append(start_race_time) # Первый чекпоинт старта
        readble_checkpoint = convertor(current_lap[0], current_lap[0])

        sct = mss.mss()

        while True:
            img = numpy.asarray(sct.grab(mon))

            if find_point(img):
                check_time = time.time()
                if check_time - current_lap[-1] > 2:
                    current_lap.append(check_time)

                    readble_checkpoint = convertor(current_lap[0], check_time)
                    readble_time.append(readble_checkpoint)

            if keyboard.is_pressed('f') & keyboard.is_pressed('alt'): # Конец гонки
                break

        print(len(readble_time))
        for j in range(0, len(readble_time)):
            print(readble_time[j])


    if keyboard.is_pressed('ctrl') & keyboard.is_pressed('q'):
        break