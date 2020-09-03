#!/usr/bin/env python
from collections import OrderedDict

import pytest

import converter


def test_load_default_options():
    context = converter.load_default_options("../cookiecutter.json")
    assert isinstance(context, OrderedDict)


if "__name__" == "__main":
    pytest.main()
