#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import datetime
from typing import List

from .post import Post


class TripHyposesis:
    """
    Represent a continuous consequence of posts in timeline 
    """
    def __init__(self, post: Post):
        self.posts = [post]
        self.country = post.country
        self.city = post.city
    
    def add_post(self, post: Post):
        self.posts.append(post)
        
    def add_posts(self, other_posts: List[Post]):
        self.posts.extend(other_posts)

    def add_posts_in_begin(self, other_posts: List[Post]):
        self.posts = other_posts + self.posts

    def get_start(self) -> datetime:
        return self.posts[0].created

    def get_end(self) -> datetime:
        return self.posts[-1].created

    def get_duration_in_days(self) -> int:
        timedelta = self.posts[-1].created - self.posts[0].created
        return timedelta.days