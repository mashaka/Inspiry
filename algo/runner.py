#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

from typing import List
import time
import logging
import os

import numpy as np

from .trip import Trip
from .post import Post
from .compute_tools import TripHyposesis, find_countries_change, unite_close_by_time_hypotheses, \
    find_city_change, find_local_cities, exclude_local_hypothesis, exclude_long_trips, unite_small_city_trips
from .geoutils import update_geodata
from .utils import make_module_name

module_logger = logging.getLogger(make_module_name(os.path.abspath(__file__)))


class Runner:

    def __init__(self,
                max_trip_length=90, 
                max_days_gap_in_trip=3,
                min_local_city_counter=3,
                max_local_cities_amount=3,
                min_posts_in_trip_amount=30,
                max_satelite_towns_distance=50,
                max_cities_distance_in_trip=1200):
        module_logger.info('Init Runner')
        # Max trip duration in days
        self.max_trip_length = max_trip_length
        # Allowed amount of days between two posts with geotag, to include between them
        # data without geotag and unite all in one trip
        self.max_days_gap_in_trip = max_days_gap_in_trip
        # Amount of trips with same city should appear in timelime to define it as local
        self.min_local_city_counter = min_local_city_counter
        # Maximal amount of local cities for one user
        self.max_local_cities_amount = max_local_cities_amount
        # Mininal amount of posts in trip to be idependent
        self.min_posts_in_trip_amount = min_posts_in_trip_amount
        # Maximal distance between local cities and their satelite towns
        self.max_satelite_towns_distance = max_satelite_towns_distance
        # Maximal distance between cities in trip
        self.max_cities_distance_in_trip = max_cities_distance_in_trip

    def compute(self, post_dicts: List[dict]) -> List[dict]:
        """
        Create trips dicts from posts dicts
        """
        # Check that posts array is not empty
        if len(post_dicts) == 0:
            return []
        posts = [Post(post_dict) for post_dict in post_dicts]
        module_logger.info('Receive {} posts'.format(len(posts)))
        trips = self.compute_internal(posts)
        trips_dicts = [trip.serialize() for trip in trips]
        module_logger.info('Ready to return {} trips'.format(len(trips_dicts)))
        return trips_dicts

    def compute_internal(self, posts: List[Post]) -> List[Trip]:
        """
        Create trips from posts
        """
        start_time = time.time()
        # Sorting posts by their date
        posts.sort(key=lambda x: x.created)
        # Update geodata in posts
        start_time_geo = time.time()
        update_geodata(posts)
        self.geo_processing_time = time.time() - start_time_geo
        module_logger.info('Update geodata in posts in {} seconds'.format(self.geo_processing_time))
        # Find change of countries
        trip_hypotheses = find_countries_change(posts)
        module_logger.info('Find {} changes of countries'.format(len(trip_hypotheses)))
        # Unite trip hyposesis with small gap in time
        trip_hypotheses = unite_close_by_time_hypotheses(trip_hypotheses, self.max_days_gap_in_trip)
        module_logger.info(
            'After uniting small time gaps, there are {} trips left'.format(len(trip_hypotheses)))
        # Find change of cities
        trip_hypotheses = find_city_change(trip_hypotheses)
        module_logger.info('{} trips after splitting by city'.format(len(trip_hypotheses)))
        # Calculate locations stats and find local cities and their satelite towns
        local_cities = find_local_cities(
            trip_hypotheses,
            self.min_local_city_counter, 
            self.max_local_cities_amount, 
            self.max_satelite_towns_distance
        )
        module_logger.info('Local cities: {}'.format(local_cities))
        # Exclude local cities and hypotheses without location
        trip_hypotheses = exclude_local_hypothesis(trip_hypotheses, local_cities)
        module_logger.info('{} trips after excluding local cities'.format(len(trip_hypotheses)))
        # Exclude very long trips
        trip_hypotheses = exclude_long_trips(trip_hypotheses, self.max_trip_length)
        module_logger.info('{} trips after excluding long trips'.format(len(trip_hypotheses)))
        # Unite small city trips in one big country trip
        trip_hypotheses = unite_small_city_trips(
            trip_hypotheses, 
            self.min_posts_in_trip_amount,
            self.max_days_gap_in_trip, 
            self.max_cities_distance_in_trip
        )
        module_logger.info('{} trips after uniting small country trips'.format(len(trip_hypotheses)))
        # Wrap results in Trip objects
        trips = [Trip(hypothesis) for hypothesis in trip_hypotheses]
        self.processing_time = time.time() - start_time
        module_logger.info('Main algo worked {} seconds'.format(self.processing_time))
        return trips
