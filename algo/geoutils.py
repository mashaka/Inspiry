#####
# Author: Maria Sandrikova, Sergey Kolesnikov
# Copyright 2017, Inspiry
#####

from typing import List
import numpy as np
from geopy.distance import great_circle

import osm_rg_wikidata as rg

from .post import Post, City


def get_geo_distance(c_1: City, c_2: City) -> float:
    """
    Calculate distance between two cities in km
    """
    return great_circle(c_1.coordinates, c_2.coordinates).km


def update_geodata(posts: List[Post]):
    """
    Update geodata in posts via geocodeder with wikidata
    """
    coordinates = [post.coordinates[::-1] if post.coordinates is not None else None for post in posts]
    location_info = list(map(
        lambda x: rg.get(x, mode=1) if x is not None else None,
        coordinates))
    cc_list = list(map(
        lambda x: str(x['country_code']).upper()
        if x is not None else None,
        location_info))
    id_list = list(map(
        lambda x: str(x['id'])
        if x is not None else None,
        location_info))
    city_name_list = list(map(
        lambda x: str(x['city'])
        if x is not None else None,
        location_info))
    city_lat_list = list(map(
        lambda x: float(x["latitude"])
        if x is not None else None,
        location_info))
    city_lon_list = list(map(
        lambda x: float(x["longitude"])
        if x is not None else None,
        location_info))
    for i, post in enumerate(posts):
        if post.coordinates is not None:
            post.city = City(id_list[i], city_name_list[i], city_lat_list[i], city_lon_list[i], cc_list[i])
            post.country = cc_list[i]
        

