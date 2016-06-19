import os
import string
import random
import time
import picamera


def _get_ready_camera():
    camera = picamera.PiCamera()
    camera.brightness = 50
    camera.vflip = True
    camera.hflip = True
    time.sleep(2)

    return camera


def _create_file_name():
    return ''.join(random.sample(string.ascii_letters, 8))


def take_photo(file_path):
    camera = _get_ready_camera()
    file_name = '{}.jpg'.format(_create_file_name())
    full_file_path = os.path.join(file_path, file_name)
    camera.capture(full_file_path)

    return file_name

