#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

from typing import List

from .compute_tools import TripHyposesis

NOT_FOUND = -1

class Trip:
    def __init__(self, trip_hyposesis: TripHyposesis):
        self.posts = trip_hyposesis.posts
        self.country = trip_hyposesis.country
        city_names = []
        self.cities = []
        for post in self.posts:
            # Store city in post.City class format
            if post.city.name not in city_names:
                self.cities.append(post.city)
                city_names.append(post.city.name)
        self.start = self.posts[0].created
        self.end = self.posts[-1].created
        self.name = self.generate_name()
        self.avatar = self.select_avatar()
        self.hashtags = self.generate_hashtags()
        self.owner = [self.posts[0].owner]

    def generate_name(self) -> str:
        return self.country + ', ' + str(self.posts[0].get_year())

    def select_avatar(self) -> List[dict]:
        max_likes = NOT_FOUND
        avatar = None
        for post in self.posts:
            if post.likes > max_likes and post.photo is not None:
                max_likes = post.likes
                avatar = post.photo
        return avatar

    def generate_hashtags(self) -> List[str]:
        hashtags = set()
        for post in self.posts:
            hashtags |= set(post.hashtags)
        return list(hashtags)


    def serialize(self) -> dict:
        trip_dict = dict()
        trip_dict['name'] = self.name
        trip_dict['visible'] = True
        trip_dict['hashtags'] = self.hashtags
        trip_dict['owners'] = self.owner
        trip_dict['comments'] = []
        trip_dict['cities'] = [city.serialize() for city in self.cities]
        trip_dict['avatar'] = self.avatar
        trip_dict['start'] = self.start
        trip_dict['end'] = self.end
        trip_dict['countries'] = [self.country]
        trip_dict['posts'] = self.get_posts_ids()
        return trip_dict

    def get_posts_ids(self) -> List[str]:
        post_ids = [post.id for post in self.posts]
        return post_ids
