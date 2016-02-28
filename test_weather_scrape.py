import logging
from nose.tools import assert_equal, assert_raises, nottest

import weather_scrape

import requests

logging.getLogger().setLevel(logging.INFO)

@nottest
def test_get_forecast_for_postcode():
  """ TODO: How to check that we get a BS object back? Should the function
      be returning this type of object?"""
  assert_equal(weather_scrape.get_forecast_for_postcode('nn1'), "Hello world!")

def test_get_forecast_for_postcode_bad_status():

  assert_raises(requests.HTTPError, weather_scrape.get_forecast_for_postcode, 'foobar')
