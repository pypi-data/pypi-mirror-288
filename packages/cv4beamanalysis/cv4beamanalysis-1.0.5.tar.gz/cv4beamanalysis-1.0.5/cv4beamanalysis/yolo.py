# Made by Isaac Joffe

import cv2
import numpy as np
from .yolov5 import detect as yolo
import os


if not os.path.exists("/tmp"):
    os.makedirs("/tmp")
    print("\"/tmp\" directory made")
else:
    print("\"/tmp\" directory already exists")
if not os.path.exists("/tmp/detect"):
    os.makedirs("/tmp/detect")
    print("\"/tmp/detect\" directory made")
else:
    print("\"/tmp/detect\" directory already exists")


def run_features(image_name, model_name):
    return yolo.get_data(weights=(model_name + "weights/best.pt"), source=image_name, data=(model_name + "data.yaml"), imgsz=(1280, 1280), project="/tmp/detect/")


def run_segmenter(image_name, model_name):
    return yolo.get_data(weights=(model_name + "weights/best.pt"), source=image_name, data=(model_name + "data.yaml"), imgsz=(192, 192), project="/tmp/detect/")


def main():
    return


if __name__ == "__main__":
    main()
