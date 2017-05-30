#####
# Author: Maria Sandrikova
# Copyright 2017, Inspiry
#####

import unittest
import os
import json

from .context import algo
from algo import Post

from .utils import read_post_dict

WORKING_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(WORKING_DIR, 'data')
SAMPLE_POST = os.path.join(DATA_DIR, 'post_sample.json')

class PostTestSuite(unittest.TestCase):
    """ Tests for algo.Post class """
    def setUp(self):
        post_dict = read_post_dict(SAMPLE_POST)
        self.post = Post(post_dict)

    def test_init(self):
        self.assertTrue(self.post.id, '584095f91f57bf5ca7f8b54f')

    def test_get_year(self):
        self.assertTrue(self.post.get_year(), 2016)
        