#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import json

from .utils import extract_coordinates


class City:
    def __init__(self, id: str, name: str, lat: float, lon: float, country_id: str):
        self.id = id
        self.name = name
        self.coordinates = (lat, lon)
        self.country_id = country_id

    def serialize(self) -> dict:
        city_dict = dict()
        city_dict['id'] = self.id
        city_dict['location'] = self.get_location()
        city_dict['countryId'] = self.country_id
        return city_dict

    def get_location(self) -> dict:
        location_dict = dict()
        location_dict['coordinates'] = list(self.coordinates)
        location_dict['type'] = 'Point'
        return location_dict


class Post:
    """
    Represents a piece of content from social media
    """
    def __init__(self, post_dict: dict):
        """
        Initialize post from its json representation
        """
        self.id = post_dict['_id']
        self.likes = post_dict['source']['likes']
        self.coordinates = None
        if 'location' in post_dict:
            self.coordinates = extract_coordinates(post_dict['location'])
        self.country = None
        self.city = None
        if 'place' in post_dict:
            place_dict = post_dict['place']
            # Try to extract coordinates if they weren't extracted on the previous step
            if self.coordinates is None:
                self.coordinates = extract_coordinates(place_dict['location'])
        self.created = post_dict['created']
        self.photo = None
        if 'photo' in post_dict:
            self.photo = post_dict['photo']
        self.hashtags = post_dict['hashtags']
        self.owner = post_dict['owner']

    def get_year(self) -> int:
        return self.created.year