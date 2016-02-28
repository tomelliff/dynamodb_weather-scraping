import logging

from bs4 import BeautifulSoup
import dateutil.parser as dparser
import requests

logging.getLogger().setLevel(logging.INFO)

def get_forecast_for_postcode(postcode):
  BBC_WEATHER_URL = 'http://www.bbc.co.uk/weather/'

  r = requests.get(BBC_WEATHER_URL + postcode.lower())

  logging.debug("Status code: {}".format(r.status_code))

  if r.status_code != requests.codes.ok:
    logging.error("Request for {0} returned status code {1}".format(r.url, r.status_code))
    r.raise_for_status()

  data = r.text

  soup = BeautifulSoup(data, 'html.parser')

  return soup

def get_forecast_date(soup):
  for caption in soup.find_all('caption'):
    logging.debug(caption.string)
    if "Weather forecast details for" in caption.string:
      date_string = caption.string.split('\n', 1)[0]

  logging.info(date_string)

  date = dparser.parse(date_string, fuzzy=True).date()

  logging.info(date)

  return date

def get_forecast(soup):
  forecast = []

  for hour in soup.find_all('span', { "class" : "hour" }):
    logging.debug(hour.string)
    hour_dict = { 'hour': hour.string }
    logging.debug(hour_dict)
    forecast.append(hour_dict)

  return forecast

def main():
  soup = get_forecast_for_postcode('NN1')

  forecast_date = get_forecast_date(soup)

  forecast = get_forecast(soup)

  logging.info(forecast)

if __name__ == '__main__':
  main()
