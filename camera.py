import os
import random
import string
import time
import numpy as np
import picamera
from PIL import Image
import config


def _is_too_dark(camera):
    camera.capture('test.jpg')
    img = Image.open('test.jpg').convert('L')
    matrix = np.array(img.getdata())

    return matrix.std() < config.MIN_STD_DEV


def _get_low_light_camera():
    camera = picamera.PiCamera()
    camera.framerate = Fraction(1, 6)
    camera.shutter_speed = 6000000
    camera.exposure_mode = 'off'
    camera.iso = 800
    time.sleep(10)


def _get_ready_camera():
    camera = picamera.PiCamera()
    camera.brightness = 50
    camera.vflip = True
    camera.hflip = True
    time.sleep(2)

    if _is_too_dark(camera):
        return _get_low_light_camera()
    else:
        return camera


def _create_file_name():
    return ''.join(random.sample(string.ascii_letters, 8))


def take_photo(file_path):
    """Capture and save a camera image.

    :param file_path: path to the directory where the file should be saved
    :returns: the name of the new image file
    """

    camera = _get_ready_camera()
    file_name = '{}.jpg'.format(_create_file_name())
    camera.capture(os.path.join(file_path, file_name))

    return file_name

