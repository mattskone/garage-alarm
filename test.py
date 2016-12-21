from fractions import Fraction
import sys
import time

from picamera import PiCamera


def get_camera():
    camera = PiCamera()
    camera.hflip = True
    camera.vflip = True

    return camera


def custom():
    c = get_camera()
    iso = int(sys.argv[1])
    ss = int(sys.argv[2])
    c.framerate = Fraction(1000000, ss)
    c.ss = ss
    c.iso = iso
    print 'Capturing with ISO {0}, shutter speed {1}, and frame rate {2}'.format(iso, ss, c.framerate)
    time.sleep(10)
    c.exposure_mode = 'off'
    c.capture('temp/temp.jpg')
    c.close()


def main():
    iso_list = [100, 200, 400, 800]
    ss_list = [50000, 500000, 2500000, 5000000]
    for iso in iso_list:
        for ss in ss_list:
            c = get_camera()
            c.framerate = Fraction(1000000, ss) 
            c.ss = ss
            c.iso = iso
            time.sleep(10)
            c.exposure_mode = 'off'
            print 'Capturing with ISO {0}, shutter speed {1}, and frame rate {2}'.format(iso, ss, c.framerate)
            print 'Gains: {0}'.format(c.awb_gains)
            filename = 'test_{0}_{1}_{2}.jpg'.format(iso, ss, float(c.framerate))
            c.capture('temp/' + filename)
            c.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        custom()
    else:
        main()
    print 'Done'

