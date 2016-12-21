from fractions import Fraction
import io
import logging
import os
import random
import string
import time

from picamera import PiCamera
from PIL import Image

import config


logger = logging.getLogger(__name__)


class Camera(object):

    ISO_LIST = [100, 200, 320, 400, 500, 640, 800]

    def __init__(self, storage_path=None):
        self.camera = self._get_camera()
        self.file_path = storage_path or config.NEW_TRIAL_DIR
        self.min_brightness = config.MIN_BRIGHTNESS
        self.max_brightness = config.MAX_BRIGHTNESS
        self.min_ss = 30000
        self.max_ss = 6000000

    def __del__(self):
        self.camera.close()

    def _get_camera(self):
        c = PiCamera()
        c.hflip = c.vflip = True

        return c

    def _create_file_name(self):
        base_name = ''.join(random.sample(string.ascii_letters, 8))
        file_name = '{0}.jpg'.format(base_name)

        return file_name

    def _get_brightness(self, img):
        img_grey = img.convert('L')
        num_pixels = img.size[0] * img_grey.size[1]
        h = img_grey.histogram()
        brightness = sum([i * h[i] for i in range(len(h))]) / num_pixels
        logger.info('Brightness: {0}'.format(brightness))
        self.current_brightness = brightness

    def _max_settings_reached(self):
        diff = abs(self.max_ss - self.camera.exposure_speed)
        if (self.camera.iso >= max(self.ISO_LIST) and
            diff <= self.max_ss * 0.001):
                logger.info('Max settings reached')
                return True

    def _is_correct_brightness(self, img):
        self._get_brightness(img)
        if (self.current_brightness > self.min_brightness and
            self.current_brightness < self.max_brightness):
            logger.info('Brightness is within limits')
            return True

        if self._max_settings_reached():
            return True

        logger.info('Brightness is not within limits')

    def _change_ss(self):
        current_ss = self.camera.exposure_speed
        new_ss = min(self.max_ss, current_ss + 500000)
        logger.info('New shutter speed: {0}'.format(new_ss))
        self.camera.framerate = Fraction(1000000, new_ss)
        self.camera.shutter_speed = new_ss

    def _change_iso(self):
        current_iso = self.camera.analog_gain * 100
        for iso in self.ISO_LIST:
            if iso > current_iso:
                logger.info('New ISO: {0}'.format(iso))
                self.camera.iso = iso
                return

        logger.info('New ISO: {0}'.format(max(self.ISO_LIST)))
        self.camera.iso = max(self.ISO_LIST)

    def _adjust_brightness(self):
        if self.current_brightness < self.min_brightness:
            if self.camera.exposure_mode not in ['night', 'off']:
                logger.info('Exposure mode: night')
                self.camera.exposure_mode = 'night'
                time.sleep(3)
            else:
                logger.info('Analog Gain: {0}'.format(self.camera.analog_gain))
                logger.info('ISO: {0}'.format(self.camera.iso))
                logger.info('SS/ES: {0} {1}'.format(self.camera.shutter_speed,
                                                    self.camera.exposure_speed))
                diff = abs(self.max_ss - self.camera.exposure_speed)
                if diff > self.max_ss * 0.001:
                    self._change_ss()
                else:
                    self._change_iso()
                sleep_duration = 1 / self.camera.framerate
                logger.info('Sleeping for {0} seconds'.format(int(sleep_duration)))
                time.sleep(sleep_duration)
                logger.info('Exposure mode: off')
                self.camera.exposure_mode = 'off'
        else:
            # TODO: gradient adjust brightness down
            pass

    def _shoot(self):
        stream = io.BytesIO()
        logger.info('Shooting image')
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        img = Image.open(stream)

        return img

    def _make_ready_image(self):
        img = self._shoot()
        while not self._is_correct_brightness(img):
            self._adjust_brightness()
            img = self._shoot()

        return img

    def _reset_camera(self):
        self.camera.exposure_mode = 'auto'
        self.camera.iso = 0
        self.camera.shutter_speed = 0
    def take_photo(self):
        img = self._make_ready_image()
        file_name = self._create_file_name()
        img.save(os.path.join(self.file_path, file_name))
        self._reset_camera()

        return file_name

