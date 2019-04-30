from PIL import ImageGrab
import os
import time

x_pad = 451
y_pad = 230


def screenGrab():
    box = (x_pad, y_pad, x_pad + 449, y_pad + 440)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
            '.png', 'PNG')


def main():
    screenGrab()


if __name__ == '__main__':
    main()