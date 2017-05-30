#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import unittest
import os
import json
from typing import List
import logging

from .context import algo
from algo import Post
from algo import Runner
from algo.compute_tools import TripHyposesis

from .utils import read_posts_dicts

WORKING_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(WORKING_DIR, 'data')
RESULT_DIR = os.path.join(WORKING_DIR, 'results')

SAMPLE_POSTS_SASHA = os.path.join(DATA_DIR, 'posts_sasha.json')
RESULT_TRIPS_SASHA = os.path.join(RESULT_DIR, 'trips_sasha.txt')

SAMPLE_POSTS_SKANANYKHIN = os.path.join(DATA_DIR, 'posts_skananykhin.json')
RESULT_TRIPS_SKANANYKHIN = os.path.join(RESULT_DIR, 'trips_skananykhin.txt')

SAMPLE_POSTS_MASHAKA = os.path.join(DATA_DIR, 'posts_mashaka.json')
RESULT_TRIPS_MASHAKA = os.path.join(RESULT_DIR, 'trips_mashaka.txt')


class RunnerTestSuite(unittest.TestCase):
    """ Tests for Runner class """
    def load_posts(self, filename: str) -> List[Post]:
        post_dicts = read_posts_dicts(filename)
        posts = []
        for post_dict in post_dicts:
            posts.append(Post(post_dict))
        posts.sort(key=lambda x: x.created)
        return posts

    def write_trips(self, filename, trips):
        with open(filename, 'w', encoding='utf8') as f:
            f.write('Trips amount: ' + str(len(trips)) + '\n')
            f.write('Geo processing time: ' + str(self.algo_runner.geo_processing_time) + '\n')
            f.write('Algo Processing time: ' + str(self.algo_runner.processing_time - self.algo_runner.geo_processing_time) + '\n')
            f.write('Total Processing time: ' + str(self.algo_runner.processing_time) + '\n')
            f.write('===================' + '\n')
            for i, trip in enumerate(trips):
                f.write('Trip ' + str(i) + '\n')
                f.write('\t' + 'start: ' + str(trip.start) + '\n')
                f.write('\t' + 'end: ' + str(trip.end) + '\n')
                f.write('\t' + 'country: ' + trip.country + '\n')
                for city in trip.cities:
                    f.write('\t' + city.name)
                f.write('\n')
                f.write('\t' + 'posts: ' + str(len(trip.posts)) + '\n')

    def setUp(self):
        self.algo_runner = Runner()

    def test_sasha_posts_internal(self):
        posts = self.load_posts(SAMPLE_POSTS_SASHA)
        trips = self.algo_runner.compute_internal(posts)
        self.write_trips(RESULT_TRIPS_SASHA, trips)
        self.assertEqual(len(trips), 5)
        self.assertEqual(trips[0].country, 'GR')
        self.assertEqual(trips[1].country, 'US')
        self.assertEqual(trips[2].country, 'CH')
        self.assertEqual(trips[3].country, 'RU')
        self.assertEqual(trips[4].country, 'FI')

    def test_sasha_posts(self):
        post_dicts = read_posts_dicts(SAMPLE_POSTS_SASHA)
        trip_dicts = self.algo_runner.compute(post_dicts)
        self.assertEqual(len(trip_dicts), 5)

    def test_skananykhin_posts_internal(self):
        posts = self.load_posts(SAMPLE_POSTS_SKANANYKHIN)
        trips = self.algo_runner.compute_internal(posts)
        self.write_trips(RESULT_TRIPS_SKANANYKHIN, trips)
        self.assertEqual(len(trips), 1)
        self.assertEqual(trips[0].country, 'RU')

    def test_mashaka_posts_internal(self):
        posts = self.load_posts(SAMPLE_POSTS_MASHAKA)
        trips = self.algo_runner.compute_internal(posts)
        self.write_trips(RESULT_TRIPS_MASHAKA, trips)
        self.assertEqual(len(trips), 4)
        self.assertEqual(trips[0].country, 'TR')
        self.assertEqual(trips[1].country, 'RU')
        self.assertEqual(trips[2].country, 'FR')
        self.assertEqual(trips[3].country, 'FI')
