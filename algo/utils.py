#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import numpy as np


def make_module_name(filepath: str) -> str:
    name = delete_extension(filepath)
    name = name.replace('\\', '.')
    name = name.replace('/', '.')
    name = name if name[0] != '.' or len(name) == 1 else name[1:]
    return name


def delete_extension(filepath: str) -> str:
    dot_ind = filepath.rfind('.')
    if dot_ind == -1:
        return filepath
    return filepath[:dot_ind]


def extract_coordinates(location_dict: dict) -> tuple:
    """
    Extract cordinates from geojson
    """
    if location_dict['type'] == 'Point':
        return tuple(location_dict['coordinates'])
    elif location_dict['type'] == 'Polygon':
        coords = np.mean(location_dict['coordinates'], axis=1)[0].tolist()
        return tuple(coords)
    else:
        raise ValueError('Unexpected location format',
                         location_dict['type'], 'in json')
