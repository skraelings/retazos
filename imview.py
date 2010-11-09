#!/usr/bin/python

"""
Small wrapper around the feh image viewer to open files from dolphin or
konqueror that share the same directory that the file clicked

author = Reynaldo Baquerizo Micheline
date = 17/06/09
mail = reynaldomic@gmail.com
revision = 0.4
"""

import os
import sys
import glob
import subprocess

FILE_FORMATS = ('jpeg', 'jpg', 'png', 'tiff', 'gif', 'bmp')
               

def find_image_files(image):
    _images = []
    curr_file = os.path.basename(image)
    if os.path.isdir(os.path.dirname(image)):
        os.chdir(os.path.dirname(image))
    for frmt in FILE_FORMATS:
        _images.extend(glob.glob("*." + frmt))
        _images.extend(glob.glob("*." + frmt.upper()))
    _images.sort()
    # Hacemos que la imagen que fue "clicked" vaya primero en el container,
    # corriendo todas las demas hacia la izquierda. De otra forma no importa
    # que imagen le demos click siempre empieza en el mismo lugar.
    pos = _images.index(curr_file)
    images = _images[pos:]
    images.extend(_images[:pos])
    # agregamos un par de apostrofes a todas las imagenes debido a los espacios
    # en blanco en algunos nombres de ficheros.
    # for idx in xrange(len(images)):
    #     images[idx] = '"' + images[idx] + '"'
    images = map(lambda name: '"' + name + '"', images)
    return " ".join(images)
    
def main(image):
    images = find_image_files(image)
    subprocess.call('feh --geometry 800x600 %s' % images, shell=True)

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1]))
    except IndexError:
        print("No files given")
        sys.exit(1)
