import keyboard
import time
from FIndCheckpoint import find_point
import json
import cv2
import mss
import numpy

def convertor(timestart, timecheck):
    point = round((timecheck - timestart), 2)
    if point // 60 == 0:
        readble_time.append(repr(point).replace('.', ':'))
    else:
        minuts = repr(point // 60) + ":" + repr(point % 60).replace('.', ':')
        readble_time.append(minuts)


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

        sct = mss.mss()

        while True:
            img = numpy.asarray(sct.grab(mon))


            if find_point(img):
                if time.time() - current_lap[-1] > 2:
                    current_lap.append(time.time())
            if keyboard.is_pressed('f') & keyboard.is_pressed('alt'): # Конец гонки
                break
        print()
    if keyboard.is_pressed('ctrl') & keyboard.is_pressed('q'):
        break