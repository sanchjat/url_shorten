# -*- coding: utf-8 -*-

import pytest
from short_url import utils 

class TestBase62(object):
    def test_base62_decode(self):
        assert utils.base62_decode("ge") == 1006
        
    def test_base62_encode(self):
        assert utils.base62_encode(1000) == "g8"
