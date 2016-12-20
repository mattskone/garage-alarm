from fractions import Fraction
import io
import os
import random
import string
import time

from picamera import PiCamera
from PIL import Image

import config


class Camera(object):

    ISO_LIST = [100, 200, 320, 400, 500, 640, 800]

    def __init__(self, storage_path):
        self.camera = self._get_camera()
        self.file_path = storage_path or config.NEW_TRIAL_PATH
        self.min_brightness = config.MIN_BRIGHTNESS
        self.max_brightness = config.MAX_BRIGHTNESS
        self.min_ss = 30000
        self.max_ss = 6000000

    def _get_camera(self):
        c = PiCamera()
        c.hflip = c.vflip = True

        return c

    def _create_file_name(self):
        base_name = ''.join(random.sample(string.ascii_letters, 8))
        file_name = '{0}.jpg'.format(base_name)

        return file_name

    def _get_brightness(self, img):
        num_pixels = img.size[0] * img.size[1]
        h = img.histogram()
        brightness = sum([i * h[i] for i in range(len(h))]) / num_pixels
        print 'Brightness: {0}'.format(brightness)
        self.current_brightness = brightness

    def _max_settings_reached(self):
        if (self.camera.iso >= 800 or
            self.camera.shutter_speed >= 6000000):
            print 'Max settings reached'
            return True

    def _is_correct_brightness(self, img):
        self._get_brightness(img)
        if (self.current_brightness > self.min_brightness and
            self.current_brightness < self.max_brightness):
            print 'Brightness is within limits'
            return True

        if self._max_settings_reached():
            return True

        print 'Brightness is not within limits'

    def _change_ss(self):
        current_ss = self.camera.exposure_speed
        new_ss = min(self.max_ss, current_ss + 500000)
        print 'New shutter speed: {0}'.format(new_ss)
        self.camera.framerate = Fraction(1000000, new_ss)
        self.camera.shutter_speed = new_ss

    def _change_iso(self):
        current_iso = self.camera.analog_gain
        for iso in self.ISO_LIST:
            if iso > current_iso:
                print 'New ISO: {0}'.format(iso)
                self.camera.iso = iso
                break

    def _adjust_brightness(self):
        if self.current_brightness < self.min_brightness:
            if self.camera.exposure_mode not in ['night', 'off']:
                print 'Exposure mode: night'
                self.camera.exposure_mode = 'night'
            else:
                if self.camera.exposure_speed < self.max_ss:
                    self._change_ss()
                else:
                    self._change_iso()
                sleep_duration = 5 / self.camera.framerate  # Capture 5 frames
                print 'Sleeping for {0} seconds'.format(sleep_duration)
                time.sleep(sleep_duration)
                print 'Exposure mode: off'
                self.camera.exposure_mode = 'off'
        else:
            # gradient adjust brightness down
            pass

    def _shoot(self):
        stream = io.BytesIO()
        print 'Shooting image'
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        img = Image.open(stream)

        return img

    def _make_ready_image(self):
        img = self._shoot()
        while not self._is_correct_brightness(img):
            self._adjust_brightness()
            img = self._shoot()

        return img

    def take_photo(self):
        try:
            img = self._make_ready_image()
        finally:
            self.camera.close()
        file_name = self._create_file_name()
        img.save(os.path.join(self.file_path, file_name))

        return file_name
