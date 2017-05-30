#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import unittest
import os
import json

from .context import algo
from algo import Post
from algo.trip_hypothesis import TripHyposesis
from algo.geoutils import update_geodata
from algo.compute_tools import find_countries_change, unite_close_by_time_hypotheses, \
    find_city_change, find_local_cities, exclude_local_hypothesis, exclude_long_trips, \
    unite_small_city_trips

from .utils import read_posts_dicts

WORKING_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(WORKING_DIR, 'data')
SAMPLE_POSTS = os.path.join(DATA_DIR, 'posts_sasha_small.json')


"""
() - for data gathered via geocoder
Real values for posts_sasha_small.json:
2016-02-01 11:46:09 RU Sochi
2016-02-04 10:35:32 RU Sochi
2016-02-04 15:21:28 RU Sochi
2016-03-21 17:34:38 RU Dolgoprudny
2016-03-21 17:57:12 RU Dolgoprudny
2016-03-21 17:57:43 RU Dolgoprudny
2016-03-27 00:06:15 RU Moscow
2016-11-06 12:41:40 RU (Moscow)
2016-11-12 20:10:52 None None
2016-11-18 19:00:13 RU Moscow
2016-11-27 00:07:31 FI (Oulu) 
2016-11-27 08:54:14 (FI) (Oulu)
2016-11-28 13:02:22 FI Helsinki
"""

class ComputeToolsTestSuite(unittest.TestCase):
    """ Tests for functions in compute_tools module """
    def setUp(self):
        post_dicts = read_posts_dicts(SAMPLE_POSTS)
        self.posts = []
        for post_dict in post_dicts:
            self.posts.append(Post(post_dict))
        self.posts.sort(key=lambda x: x.created)
        update_geodata(self.posts)

    def test_minimal_compute_tools(self):
        # test find countries change
        trip_hypotheses = find_countries_change(self.posts)
        self.assertEqual(len(trip_hypotheses), 6)
        self.assertEqual(trip_hypotheses[0].country, 'RU')
        self.assertEqual(trip_hypotheses[1].country, None)
        self.assertEqual(trip_hypotheses[2].country, 'RU')
        self.assertEqual(trip_hypotheses[3].country, 'FI')
        self.assertEqual(trip_hypotheses[4].country, None)
        self.assertEqual(trip_hypotheses[5].country, 'FI')

        # test unite close by time hypotheses(self):
        trip_hypotheses = unite_close_by_time_hypotheses(trip_hypotheses, 2)
        self.assertEqual(len(trip_hypotheses), 4)
        self.assertEqual(trip_hypotheses[0].country, 'RU')
        self.assertEqual(trip_hypotheses[1].country, None)
        self.assertEqual(trip_hypotheses[2].country, 'RU')
        self.assertEqual(trip_hypotheses[3].country, 'FI')

        # test find city change
        trip_hypotheses = find_city_change(trip_hypotheses)
        self.assertEqual(len(trip_hypotheses), 7)
        self.assertEqual(trip_hypotheses[0].city.name, 'Sochi')
        self.assertEqual(trip_hypotheses[1].city.name, 'Dolgoprudny')
        self.assertEqual(trip_hypotheses[2].city.name, 'Moscow')
        self.assertEqual(trip_hypotheses[3].city, None)
        self.assertEqual(trip_hypotheses[4].city.name, 'Moscow')
        # Oulu is a result of bad geo polygon (should be Helsinki instead)
        self.assertEqual(trip_hypotheses[5].city.name, 'Oulu')
        self.assertEqual(trip_hypotheses[6].city.name, 'Helsinki')

        # test find local cities
        local_cities = find_local_cities(trip_hypotheses, 3, 3, 50)
        self.assertEqual(len(local_cities), 2)
        self.assertEqual(local_cities[0], 'Moscow')
        self.assertEqual(local_cities[1], 'Dolgoprudny')

        # tests exclude local hypothesis
        trip_hypotheses = exclude_local_hypothesis(trip_hypotheses, local_cities)
        self.assertEqual(len(trip_hypotheses), 3)
        self.assertEqual(trip_hypotheses[0].city.name, 'Sochi')
        # Oulu is a result of bad geo polygon (should be Helsinki instead)
        self.assertEqual(trip_hypotheses[1].city.name, 'Oulu')
        self.assertEqual(trip_hypotheses[2].city.name, 'Helsinki')

        # Tests exclude very long trips
        trip_hypotheses = exclude_long_trips(trip_hypotheses, 90)
        self.assertEqual(len(trip_hypotheses), 3)

        # Test unite small city trips in one big country trip
        trip_hypotheses = unite_small_city_trips(trip_hypotheses, 3, 2, 600)
        self.assertEqual(len(trip_hypotheses), 2)
        self.assertEqual(trip_hypotheses[0].city.name, 'Sochi')
        # Oulu is a result of bad geo polygon (should be Helsinki instead)
        self.assertEqual(trip_hypotheses[1].city.name, 'Oulu')
