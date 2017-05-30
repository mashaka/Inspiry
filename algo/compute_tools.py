#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import datetime
from typing import List
import operator
import logging
import os

from .post import Post
from .trip_hypothesis import TripHyposesis
from .geoutils import get_geo_distance
from .utils import make_module_name

module_logger = logging.getLogger(make_module_name(os.path.abspath(__file__)))


def find_countries_change(posts) -> List[TripHyposesis]:
    """
    Find intervals with the same country 
    """
    trip_hypotheses = [TripHyposesis(posts[0])]
    countries = [trip_hypotheses[0].country]
    for post in posts[1:]:
        if post.country != trip_hypotheses[-1].country:
            countries.append(post.country)
            trip_hypotheses.append(TripHyposesis(post))
        else:
            trip_hypotheses[-1].add_post(post)
    module_logger.info('Find country sequence: {}'.format(countries))
    return trip_hypotheses


def calc_hypotheses_gap(h_1: TripHyposesis, h_2: TripHyposesis):
    """
    Calc gap in days between TripHypothesis object
    """
    time_delta = h_2.get_start() - h_1.get_end()
    return time_delta.days


def unite_close_by_time_hypotheses(
        trip_hypotheses: List[TripHyposesis],
        max_days_gap_in_trip
    ) -> List[TripHyposesis]:
    """
    Unite hypothesis with same country that have between them small amout of days
    without geotags
    """
    if len(trip_hypotheses) < 3:
        return trip_hypotheses
    new_trips = [trip_hypotheses[0]]
    i = 2
    last_added = 0
    while i < len(trip_hypotheses):
        if new_trips[-1].country != None and trip_hypotheses[i-1].country == None and \
                new_trips[-1].country == trip_hypotheses[i].country and \
                calc_hypotheses_gap(new_trips[-1], trip_hypotheses[i]) <= max_days_gap_in_trip:
            for post in trip_hypotheses[i-1].posts:
                post.country = new_trips[-1].country
                new_trips[-1].add_post(post)
            new_trips[-1].add_posts(trip_hypotheses[i].posts)
            last_added = i
            i += 2
        else:
            new_trips.append(trip_hypotheses[i-1])
            last_added = i-1
            i += 1
    while last_added != len(trip_hypotheses) - 1:
        last_added += 1
        new_trips.append(trip_hypotheses[last_added])
    countries = [trip.country for trip in new_trips]
    module_logger.info('New country sequence: {}'.format(countries))
    return new_trips


def split_trip_by_cities(
        trip: TripHyposesis
    ) -> List[TripHyposesis]:
    """
    Split trip inside one country
    """
    # Split by city
    new_trips = [TripHyposesis(trip.posts[0])]
    if len(trip.posts) == 1:
        return new_trips
    for post in trip.posts[1:]:
        if (new_trips[-1].city is None and post.city is None) or \
                (new_trips[-1].city is not None and post.city is not None and \
                new_trips[-1].city.name == post.city.name):
            new_trips[-1].add_post(post)
        else:
            new_trips.append(TripHyposesis(post))
    # Unite posts without geotags with the closest in timeline city
    # (assume that on edges of the interval inside one country we have posts with 
    # information about city, because of a construction process)
    if len(new_trips) < 3:
        return new_trips
    new_trips_without_gaps = []
    for i, city_trip in enumerate(new_trips):
        if city_trip.city is None:
            for p, post in enumerate(city_trip.posts):
                if calc_hypotheses_gap(new_trips[i-1], city_trip) > \
                        calc_hypotheses_gap(city_trip, new_trips[i+1]):
                    j = p
                    while j < len(city_trip.posts):
                        city_trip.posts[j].city = new_trips[i+1].city
                        j += 1
                    new_trips[i+1].add_posts_in_begin(city_trip.posts[p:])
                    break
                else:
                    post.city = new_trips[i-1].city
                    new_trips_without_gaps[-1].add_post(post)
        else:
            new_trips_without_gaps.append(city_trip)
    return new_trips_without_gaps
    

def find_city_change(trip_hypotheses: List[TripHyposesis]) -> List[TripHyposesis]:
    """
    Find change of cities
    """
    new_trips = []
    for trip in trip_hypotheses:
        if trip.country == None:
            new_trips.append(trip)
        else:
            new_trips.extend(split_trip_by_cities(trip))
    return new_trips


def find_local_cities(
        trip_hypotheses: List[TripHyposesis],
        min_local_city_counter,
        max_local_cities_amount,
        max_satelite_towns_distance
    ) -> List[str]:
    """
    Calculate locations stats and find local cities
    """
    local_cities = []
    cities_counter = dict()
    cities_dict = dict()
    for trip in trip_hypotheses:
        if trip.city is None:
            continue
        if trip.city.name in cities_counter:
            cities_counter[trip.city.name] += 1
        else:
            cities_dict[trip.city.name] = trip.city
            cities_counter[trip.city.name] = 1
    cities_sorted = sorted(cities_counter.items(), key=operator.itemgetter(1), reverse=True)
    if cities_sorted[0][1] > 1:
        local_cities.append(cities_sorted[0][0])
    for city in cities_sorted[1:max_local_cities_amount]:
        if city[1] >= min_local_city_counter:
            local_cities.append(city[0])
    # Add satelite towns for local cities
    additional_local_cities = []
    for city in cities_dict:
        if city not in local_cities:
            for local_city in local_cities:
                if get_geo_distance(cities_dict[city], cities_dict[local_city]) \
                        < max_satelite_towns_distance:
                    additional_local_cities.append(city)
                    break
    local_cities.extend(additional_local_cities) 
    return local_cities


def exclude_local_hypothesis(
        trip_hypotheses: List[TripHyposesis],
        local_cities: List[str]
    ) -> List[TripHyposesis]:
    """
    Exclude local cities and hypotheses without location
    """
    new_trips = []
    for trip in trip_hypotheses:
        if trip.country is not None and trip.city.name not in local_cities:
            new_trips.append(trip)
    return new_trips


def exclude_long_trips(
        trip_hypotheses: List[TripHyposesis],
        max_trip_length
    ) -> List[TripHyposesis]:
    """
    Exclude or split very long trips
    """
    new_trips = []
    for trip in trip_hypotheses:
        if trip.get_duration_in_days() <= max_trip_length:
            new_trips.append(trip)
    return new_trips


def unite_small_city_trips(
        trip_hypotheses: List[TripHyposesis], 
        min_posts_in_trip_amount: int,
        max_days_gap_in_trip: int,
        max_cities_distance_in_trip: int
    ) -> List[TripHyposesis]:
    """
    Unite small city trips in one big country trip
    """
    new_trips = [trip_hypotheses[0]]
    if len(trip_hypotheses) == 1:
        return new_trips
    for trip in trip_hypotheses[1:]:
        if trip.country == new_trips[-1].country:
            days_gap = calc_hypotheses_gap(new_trips[-1], trip)
            geo_distance = get_geo_distance(new_trips[-1].posts[-1].city, trip.posts[0].city)
            if days_gap <= max_days_gap_in_trip and (len(trip.posts) <= min_posts_in_trip_amount or \
                    len(new_trips[-1].posts) <= min_posts_in_trip_amount): # and \
                    # geo_distance < max_cities_distance_in_trip:
                module_logger.info('Unite {} with {}'.format(
                        new_trips[-1].posts[-1].city.name, 
                        trip.posts[-1].city.name
                    )
                )
                new_trips[-1].add_posts(trip.posts)
                continue
            else:
                module_logger.info('Not unite {}, distance {}, days gap {}'.format(
                        trip.posts[-1].city.name, 
                        geo_distance,
                        days_gap
                    )
                )
        new_trips.append(trip)
    return new_trips

