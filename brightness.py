import sys

from PIL import Image


def main():
    img = Image.open(sys.argv[1]).convert('L')
    pixels = img.size[0] * img.size[1]
    h = img.histogram()
    mu0 = 1.0 * sum([i * h[i] for i in range(len(h))]) / pixels

    print 'Average brightness: {0}'.format(round(mu0, 2))


if __name__ == '__main__':
    main()

