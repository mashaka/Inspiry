#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import unittest
import os
import json

from .context import algo
from algo.geoutils import update_geodata, get_geo_distance
from algo import Post

WORKING_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(WORKING_DIR, 'data')
SAMPLE_POSTS = os.path.join(DATA_DIR, 'posts_sasha_small.json')

from .utils import read_posts_dicts

"""
Real values for posts_sasha_small.json:
2016-02-01 11:46:09 RU Адлер
2016-02-04 10:35:32 RU Адлер
2016-02-04 15:21:28 RU Адлер
2016-03-21 17:34:38 RU Долгопрудный
2016-03-21 17:57:12 RU Долгопрудный
2016-03-21 17:57:43 RU Долгопрудный
2016-03-27 00:06:15 RU Moscow
2016-11-06 12:41:40 RU None
2016-11-12 20:10:52 None None
2016-11-18 19:00:13 RU Moscow
2016-11-27 00:07:31 FI None
2016-11-27 08:54:14 None None
2016-11-28 13:02:22 FI Helsinki
"""

class GeoUtilsTestSuite(unittest.TestCase):
    """ Tests for geo utils functions in algo package """

    def setUp(self):
        post_dicts = read_posts_dicts(SAMPLE_POSTS)
        self.posts = []
        for post_dict in post_dicts:
            self.posts.append(Post(post_dict))
        self.posts.sort(key=lambda x: x.created)

    def test_update_geodata(self):
        update_geodata(self.posts)
        self.assertEqual(self.posts[0].city.name, 'Sochi')
        self.assertEqual(self.posts[1].city.name, 'Sochi')
        self.assertEqual(self.posts[2].city.name, 'Sochi')
        self.assertEqual(self.posts[3].city.name, 'Dolgoprudny')
        self.assertEqual(self.posts[4].city.name, 'Dolgoprudny')
        self.assertEqual(self.posts[5].city.name, 'Dolgoprudny')
        self.assertEqual(self.posts[6].city.name, 'Moscow')
        self.assertEqual(self.posts[7].city.name, 'Moscow')
        self.assertEqual(self.posts[8].city, None)
        self.assertEqual(self.posts[9].city.name, 'Moscow')
        # Oulu is a result of bad geo polygon (should be Helsinki instead)
        self.assertEqual(self.posts[10].city.name, 'Oulu')
        self.assertEqual(self.posts[11].city, None)
        self.assertEqual(self.posts[12].city.name, 'Helsinki')

    def test_get_geo_distance(self):
        update_geodata(self.posts)
        sochi = self.posts[0].city
        moscow = self.posts[6].city
        distance = get_geo_distance(sochi, moscow)
        self.assertTrue(1350 < distance < 1400)
        dolgoprudny = self.posts[3].city
        distance = get_geo_distance(dolgoprudny, moscow)
        self.assertTrue(distance < 50)
  