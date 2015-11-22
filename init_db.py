import os
import sys
import scipy.misc
from glob import glob

"""Before importing other modules, we need to add the project
settings to the path."""
os.environ['DJANGO_SETTINGS_MODULE'] = 'grimaces.settings'

from faces.models import Face

root_path = 'faces/static/faces/DATASET'

def parse_name(img_name):
    """returns the attributes encoded in the given
    image name (assumes following naming format:
    /YYYY/stage_num/stage_num-HH_MM:SS:MMM:face_num:gradient.jpg
    e.g.
    /2014/9/9-00_08:10:000:0:0.0.jpg."""
    img_attributes = {}
    img_attributes['img_name'] = img_name[12:]
    img_attributes['year'] = int(img_name.split('/')[-3])
    img_attributes['stage_num'] = int(img_name.split('/')[-2])
    time_string = img_name.split('-')[-1]
    img_attributes['time'] = ":".join(time_string.split(':')[:3])
    img_attributes['gradient'] = float(img_name.split(':')[-1][:-4])
    img = scipy.misc.imread(img_name)
    size = img.shape[0] * img.shape[1]
    img_attributes['size'] = size
    return img_attributes

def save_faces():
    img_names = [name for path in os.walk(root_path) for name 
        in glob(os.path.join(path[0], '*.jpg'))]
    attribute_sets = [parse_name(img_name) for img_name in img_names]

    for attribute_set in attribute_sets:
        face = Face(
                img_name=attribute_set['img_name'],
                year=attribute_set['year'],
                stage_num=attribute_set['stage_num'],
                time=attribute_set['time'],
                size=attribute_set['size'],
                gradient=attribute_set['gradient'])

        face.save()

save_faces()
