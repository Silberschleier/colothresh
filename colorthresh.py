import argparse
from PIL import Image


class Filter():
    def __init__(self):
        pass

    def filter(self, image, **kwargs):
        pixel = image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                a, b, c = pixel[i, j]
                pixel[i, j] = self.modify(a, b, c, **kwargs)

        return image

    def modify(self, a, b, c, **kwargs):
        return a, b, c


class HSVThreshold(object, Filter):
    def filter(self, image, **kwargs):
        return super(HSVThreshold, self).filter(image.convert("HSV"), **kwargs)

    def modify(self, a, b, c, **kwargs):
        if c > kwargs["threshold"]:
            return 0, 0, 255
        else:
            return a, 255, c


class RGBThreshold(object, Filter):
    def filter(self, image, **kwargs):
        return super(RGBThreshold, self).filter(image.convert("RGB"), **kwargs)

    def modify(self, a, b, c, **kwargs):
        t = kwargs["threshold"]

        # Red
        if a > t:
            a = 255
        else:
            a = 0

        # Green
        if b > t:
            b = 255
        else:
            b = 0

        # Blue
        if c > t:
            c = 255
        else:
            c = 0

        return a, b, c


'''
Argument parsing is handled at this point
'''
parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input file')
parser.add_argument('--output', type=str, default='-', help='Output file')
parser.add_argument('--threshold', type=int, choices=range(0, 255), default=180)
parser.add_argument('--colormodel', type=str, choices=['hsv', 'rgb'], default='rgb', help="The color-model to use")
args = parser.parse_args()

# Read the image
im = Image.open(args.input)

if args.colormodel == 'rgb':
    im = RGBThreshold().filter(im, threshold=args.threshold)
elif args.colormodel == 'hsv':
    im = HSVThreshold().filter(im, threshold=args.threshold)

if args.output == '-':
    im.show()
else:
    im.convert("RGB").save(args.output)
