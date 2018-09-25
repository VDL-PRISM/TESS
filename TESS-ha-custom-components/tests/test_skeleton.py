#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tess_ha_custom_components.skeleton import fib

__author__ = "Kyeong T. Min"
__copyright__ = "Kyeong T. Min"
__license__ = "none"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
