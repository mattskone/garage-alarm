import os
import string
import random
import time
import picamera
import config


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
    """Capture and save a camera image.

    :param file_path: path to the directory where the file should be saved
    :returns: the name of the new image file
    """

    camera = _get_ready_camera()
    file_name = '{}.jpg'.format(_create_file_name())
    camera.capture(os.path.join(config.NEW_TRIAL_DIR, file_name))

    return file_name

