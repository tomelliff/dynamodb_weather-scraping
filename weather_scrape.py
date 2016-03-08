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

  logging.debug(date_string)

  date = dparser.parse(date_string, fuzzy=True).date()

  logging.debug(date)

  return date

def get_forecast(soup):
  forecast = []

  for hour in soup.find_all('span', {'class': 'hour'}):
    logging.debug(hour.string)
    hour_dict = { 'hour': hour.string }
    logging.debug(hour_dict)
    forecast.append(hour_dict)

  i = 0

  for conditions_block in soup.find('tr', {'class': 'weather-type'}).find_all('td'):
    img_element = conditions_block.find('img')
    if img_element:
       conditions = img_element['alt']
       logging.debug(conditions)
       forecast[i]['weather-conditions'] = conditions
    i += 1

  j = 0

  for temperature_block in soup.find('tr', {'class': 'temperature'}).find_all('td'):
    temperature_element = temperature_block.find('span', {'data-unit': 'c'})
    if temperature_element:
      logging.debug(temperature_element)
      temperature_celsius = temperature_element.contents[0]
      forecast[j]['temperature-celsius'] = temperature_celsius
    j += 1

  k = 0

  for wind_block in soup.find('tr', {'class': 'windspeed'}).find_all('td'):
    wind_element = wind_block.find('span', {'class': 'wind'})
    if wind_element:
      logging.debug(wind_element)
      wind_speed_mph = wind_element.find('span', {'data-unit': 'mph'}).contents[0]
      logging.debug(wind_speed_mph)
      wind_direction = wind_element.find('span', {'class': 'description'}).string
      logging.debug(wind_direction)
      wind_dict = {'direction': wind_direction, 'speed-mph': wind_speed_mph}
      logging.debug(wind_dict)
      forecast[k]['wind'] = wind_dict
    k += 1

  return forecast

def main():
  soup = get_forecast_for_postcode('NN1')

  forecast_date = get_forecast_date(soup)

  logging.info("forecast date: {}".format(forecast_date))

  forecast = get_forecast(soup)

  logging.info("forecast: {}".format(forecast))

if __name__ == '__main__':
  main()
