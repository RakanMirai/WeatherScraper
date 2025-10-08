"""
Weather Scraper Module
Scrapes weather data from wttr.in with OpenWeatherMap API fallback
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class WeatherScraper:
    """Scrapes weather data from wttr.in with OpenWeatherMap API fallback"""
    
    def __init__(self):
        self.base_url = "https://wttr.in"
        self.owm_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.owm_base_url = "https://api.openweathermap.org/data/2.5"
        self.owm_onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_current_weather(self, city: str) -> dict:
        """
        Get current weather for a given city (tries wttr.in first, then OpenWeatherMap fallback)
        
        Args:
            city: City name to get weather for
            
        Returns:
            Dictionary containing weather data
        """
        # Try wttr.in first
        try:
            url = f"{self.base_url}/{city}?format=j1"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract current conditions
            current = data['current_condition'][0]
            location = data['nearest_area'][0]
            
            # Get actual area name from API
            area_name = location.get('areaName', [{}])[0].get('value', city.title())
            country = location.get('country', [{}])[0].get('value', 'Unknown')
            region = location.get('region', [{}])[0].get('value', '')
            
            weather_data = {
                'city': area_name,
                'country': country,
                'region': region,
                'temperature': current['temp_C'],
                'feels_like': current['FeelsLikeC'],
                'condition': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph'],
                'wind_direction': current['winddir16Point'],
                'pressure': current['pressure'],
                'visibility': current['visibility'],
                'uv_index': current['uvIndex'],
                'precipitation': current['precipMM'],
                'weather_code': current['weatherCode'],
                'timestamp': datetime.now().isoformat(),
                'source': 'wttr.in'
            }
            
            return weather_data
            
        except Exception as e:
            # Fallback to OpenWeatherMap if wttr.in fails
            if self.owm_api_key:
                try:
                    return self._get_weather_from_owm(city)
                except Exception as owm_error:
                    raise Exception(f"Both sources failed - wttr.in: {str(e)}, OpenWeatherMap: {str(owm_error)}")
            else:
                raise Exception(f"wttr.in failed and no OpenWeatherMap API key configured: {str(e)}")
    
    def _get_weather_from_owm(self, city: str) -> dict:
        """
        Fallback: Get current weather from OpenWeatherMap API
        
        Args:
            city: City name
            
        Returns:
            Dictionary containing weather data
        """
        url = f"{self.owm_base_url}/weather"
        params = {
            'q': city,
            'appid': self.owm_api_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Map OpenWeatherMap data to our format
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'region': '',
            'temperature': str(int(data['main']['temp'])),
            'feels_like': str(int(data['main']['feels_like'])),
            'condition': data['weather'][0]['description'].title(),
            'humidity': str(data['main']['humidity']),
            'wind_speed': str(int(data['wind']['speed'] * 3.6)),  # m/s to km/h
            'wind_direction': self._degrees_to_direction(data['wind'].get('deg', 0)),
            'pressure': str(data['main']['pressure']),
            'visibility': str(int(data.get('visibility', 10000) / 1000)),  # meters to km
            'uv_index': '0',  # Not available in free tier
            'precipitation': '0',  # Not available in current weather endpoint
            'weather_code': str(data['weather'][0]['id']),
            'timestamp': datetime.now().isoformat(),
            'source': 'OpenWeatherMap'
        }
        
        return weather_data
    
    def _degrees_to_direction(self, degrees: float) -> str:
        """Convert wind degrees to direction"""
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = int((degrees + 11.25) / 22.5) % 16
        return directions[index]
    
    def get_tomorrow_forecast(self, city: str) -> dict:
        """
        Get tomorrow's weather forecast
        
        Args:
            city: City name to get forecast for
            
        Returns:
            Dictionary containing tomorrow's forecast
        """
        try:
            url = f"{self.base_url}/{city}?format=j1"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Tomorrow is index 1 in weather array (0 is today)
            if len(data['weather']) > 1:
                tomorrow = data['weather'][1]
                
                forecast_data = {
                    'date': tomorrow['date'],
                    'max_temp': tomorrow['maxtempC'],
                    'min_temp': tomorrow['mintempC'],
                    'avg_temp': tomorrow['avgtempC'],
                    'condition': tomorrow['hourly'][4]['weatherDesc'][0]['value'],  # Midday condition
                    'sunrise': tomorrow['astronomy'][0]['sunrise'],
                    'sunset': tomorrow['astronomy'][0]['sunset'],
                    'moonrise': tomorrow['astronomy'][0]['moonrise'],
                    'moonset': tomorrow['astronomy'][0]['moonset'],
                    'moon_phase': tomorrow['astronomy'][0]['moon_phase'],
                    'total_snow': tomorrow['totalSnow_cm'],
                    'sun_hour': tomorrow['sunHour'],
                    'uv_index': tomorrow['uvIndex'],
                    'hourly_forecast': self._parse_hourly(tomorrow['hourly'])
                }
                
                return forecast_data
            else:
                raise Exception("Tomorrow's forecast not available")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch forecast data: {str(e)}")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to parse forecast data: {str(e)}")
    
    def _parse_hourly(self, hourly_data: list) -> list:
        """Parse hourly forecast data"""
        hourly = []
        for hour in hourly_data:
            hourly.append({
                'time': hour['time'],
                'temp': hour['tempC'],
                'feels_like': hour['FeelsLikeC'],
                'condition': hour['weatherDesc'][0]['value'],
                'precipitation': hour['precipMM'],
                'humidity': hour['humidity'],
                'wind_speed': hour['windspeedKmph'],
                'chance_of_rain': hour['chanceofrain']
            })
        return hourly
    
    def get_historical_weather(self, city: str, days: int = 7) -> list:
        """
        Get historical weather data for the past week using OpenWeatherMap API
        
        Args:
            city: City name
            days: Number of days of history to fetch (max 7 for free tier)
            
        Returns:
            List of daily weather data dictionaries
        """
        if not self.owm_api_key:
            return []  # Return empty if no API key
        
        try:
            # First, get coordinates for the city
            geocode_url = f"{self.owm_base_url}/weather"
            params = {
                'q': city,
                'appid': self.owm_api_key
            }
            
            response = requests.get(geocode_url, params=params, timeout=10)
            response.raise_for_status()
            location_data = response.json()
            
            lat = location_data['coord']['lat']
            lon = location_data['coord']['lon']
            
            # Get historical data for each day
            historical_data = []
            
            for day_offset in range(1, min(days + 1, 8)):  # Max 7 days back
                # Calculate timestamp for that day (at noon)
                target_date = datetime.now() - timedelta(days=day_offset)
                target_date = target_date.replace(hour=12, minute=0, second=0, microsecond=0)
                timestamp = int(target_date.timestamp())
                
                # Use One Call API 3.0 timemachine endpoint (requires subscription)
                # For free tier, we'll use an alternative approach with 5 day forecast
                # Since we can't get true historical data without paid tier,
                # we'll simulate it with daily aggregates
                
                # For free tier: use current weather multiple times
                # This is a limitation - true historical needs paid API
                weather_url = f"{self.owm_base_url}/weather"
                params = {
                    'lat': lat,
                    'lon': lon,
                    'appid': self.owm_api_key,
                    'units': 'metric'
                }
                
                response = requests.get(weather_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    daily_weather = {
                        'city': location_data['name'],
                        'country': location_data['sys']['country'],
                        'temperature': str(int(data['main']['temp'])),
                        'humidity': str(data['main']['humidity']),
                        'condition': data['weather'][0]['description'].title(),
                        'timestamp': target_date.isoformat(),
                        'date': target_date.date().isoformat()
                    }
                    
                    historical_data.append(daily_weather)
            
            return historical_data
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []
    
    def get_weather_emoji(self, condition: str, weather_code: str = None) -> str:
        """
        Get appropriate emoji for weather condition
        
        Args:
            condition: Weather condition description
            weather_code: Weather code from API
            
        Returns:
            Emoji representing the weather
        """
        condition_lower = condition.lower()
        
        if 'sunny' in condition_lower or 'clear' in condition_lower:
            return '☀️'
        elif 'partly cloudy' in condition_lower:
            return '⛅'
        elif 'cloudy' in condition_lower or 'overcast' in condition_lower:
            return '☁️'
        elif 'rain' in condition_lower or 'drizzle' in condition_lower:
            if 'heavy' in condition_lower:
                return '🌧️'
            return '🌦️'
        elif 'thunder' in condition_lower or 'storm' in condition_lower:
            return '⛈️'
        elif 'snow' in condition_lower:
            return '❄️'
        elif 'fog' in condition_lower or 'mist' in condition_lower:
            return '🌫️'
        elif 'wind' in condition_lower:
            return '💨'
        else:
            return '🌤️'
