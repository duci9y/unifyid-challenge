# Boilerplate from https://stackoverflow.com/a/20304716/1593651

import requests
from PIL import Image
import random
from math import sin, cos

# 64 bytes (!) of entropy are enough for non-crypto purposes
DEFAULT_LENGTH = 64
response = requests.get('https://www.random.org/cgi-bin/randbyte?nbytes={0}&format=f'.format(DEFAULT_LENGTH), timeout=10)
raw_bytes = response.content

random.seed(raw_bytes)

img = Image.new('RGB', (128, 128), 'black') # create a new black image
pixels = img.load() # create the pixel map

# attempt at being artsy
rseed, gseed, bseed = None, None, None
rotator = random.randint(0, 2)

for i in range(img.size[0]):
    for j in range(img.size[1]):

        if i * j % 512 == 0:
            rseed, gseed, bseed = [random.random() for _ in range(3)]
        
        r = sin(rseed * i * 0.01) * 255
        g = cos(gseed * j * -0.05) * 255
        b = sin(bseed * i * j * 0.001) * 255

        data = [int(r), int(g), int(b)]

        pixels[i, j] = tuple([data[m % 3] for m in range(rotator, rotator + 3)])

img.show()
