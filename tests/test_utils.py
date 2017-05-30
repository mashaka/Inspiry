#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import unittest
import os

from .context import algo
from algo.utils import extract_coordinates, delete_extension


class UtilsTestSuite(unittest.TestCase):
    """ Tests for utils functions in algo package """

    def test_extract_coordinates(self):
        point_coordinated = extract_coordinates({
            "type": "Point",
            "coordinates": [24.93424987, 60.1698687]
        })
        self.assertTupleEqual(point_coordinated, (24.93424987, 60.1698687))
        polygon_coordinated = extract_coordinates({
            "type": "Polygon",
            "coordinates": [
                [
                    [24.78281, 60.021032],
                    [25.2544364, 60.021032],
                    [25.2544364, 60.2979104],
                    [24.78281, 60.2979104],
                    [24.78281, 60.021032]
                ]
            ]
        })
        self.assertTupleEqual(polygon_coordinated, (24.97146056, 60.13178336))

    def test_delete_extension(self):
        self.assertEqual(delete_extension('tests.py'), 'tests')
