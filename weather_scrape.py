import logging

from bs4 import BeautifulSoup
import requests

logging.getLogger().setLevel(logging.INFO)

def get_forecast_for_postcode(postcode):
  BBC_WEATHER_URL = 'http://www.bbc.co.uk/weather/'

  r = requests.get(BBC_WEATHER_URL + postcode.lower())

  logging.debug("Status code: {}".format(r.status_code))

  data = r.text

  soup = BeautifulSoup(data, 'html.parser')

  return soup

def main():
  soup = get_forecast_for_postcode('NN1')

if __name__ == '__main__':
  main()
