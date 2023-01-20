import os
from io import BytesIO

import numpy as numpy
import requests
from colormath.color_objects import sRGBColor
from colorthief import ColorThief
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

from downloadimages import download_images


def mosaic(imgsrc, projname, query, nimgs=50, himgs=250, vimgs=250, factor=5):
    projroot = f'{os.getcwd()}\\projects\\{projname}\\'
    
    response = requests.get(imgsrc)
    im = Image.open(BytesIO(response.content))
    
    initial_h = im.size[0]
    initial_v = im.size[1]

    hpieceres = int(round(initial_h/himgs)) # h res of a single piece of mosaic
    vpieceres = int(round(initial_v/vimgs)) # v res of a single piece of mosaic

    hres = int(round(initial_h/himgs))*himgs
    vres = int(round(initial_v/vimgs))*vimgs

    print(f'total image is {hres}x{vres}, printing {himgs*vimgs} images of size {hpieceres}x{vpieceres}')

    im = im.resize((hres,vres))

    print('t')
    im.save(f'{projroot}res{projname}.png')
    print('f')

    download_images(query, nimgs, f'{projroot}\\images\\')

    pieces = {}
    for filename in os.listdir(f'{projroot}\\images\\'):
        ct = ColorThief(f'{projroot}\\images\\' + filename)
        dc = ct.get_color(quality=1)
        pieces[filename] = dc

    print(pieces)

    def color_distance(rgb1, rgb2):
        rm = 0.5 * (rgb1[0] + rgb2[0])
        rd = ((2 + rm) * (rgb1[0] - rgb2[0])) ** 2
        gd = (4 * (rgb1[1] - rgb2[1])) ** 2
        bd = ((3 - rm) * (rgb1[2] - rgb2[2])) ** 2
        return (rd + gd + bd) ** 0.5

    newim = im.copy()
    newim = newim.resize((hres*factor, vres*factor))
    for i in tqdm(range(himgs*vimgs), desc='current image'):
        hindex = i % himgs # 0-himgs
        vindex = i // vimgs 
        reg = (hindex*hpieceres, vindex*vpieceres, (hindex+1)*hpieceres, (vindex+1)*vpieceres)
        region = im.crop(reg)
        region.save(f'{projroot}regions\\reg{vindex}_{hindex}.png')
        ct = ColorThief(f'{projroot}regions\\reg{vindex}_{hindex}.png')
        try:
            regcolor = ct.get_color(quality=1)
        except Exception as e:
            regcolor = (0,0,0)
            continue
        mind = 1000000
        minfname = ''
        for fname, piececolor in pieces.items():
            if color_distance(regcolor, piececolor) < mind:
                mind = color_distance(regcolor, piececolor)
                minfname = fname
        piece = Image.open(f'{projroot}\\images\\' + minfname)
        piece = piece.resize((hpieceres*factor, vpieceres*factor))
        reg = (hindex*hpieceres*factor, vindex*vpieceres*factor, (hindex+1)*hpieceres*factor, (vindex+1)*vpieceres*factor)
        newim.paste(piece, reg)

    newim.save(f'{projroot}final{projname}.png')
    return f'{projroot}final{projname}.png'
