import bpy
import bmesh

import os

from math import *
from mathutils import *
from bpy_extras import image_utils

from .Utilities import *
from .Blender import*
from .Resources import *

def main(filepath, files, clear_scene):
    if clear_scene:
        clearScene()

    folder = (os.path.dirname(filepath))

    for i, j in enumerate(files):

        path_to_file = (os.path.join(folder, j.name))

        file = open(path_to_file, 'rb')
        filename =  path_to_file.split("\\")[-1]
        file_extension =  os.path.splitext(path_to_file)[1]
        file_size = os.path.getsize(path_to_file)

        br = BinaryReader(file, "<")
        
                

    