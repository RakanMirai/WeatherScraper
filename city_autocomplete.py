"""
City Autocomplete Module
Provides city suggestions with country information using OpenStreetMap Nominatim API
"""

import requests
from typing import List, Dict
import time


class CityAutocomplete:
    """Handles city search and autocomplete functionality"""
    
    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            'User-Agent': 'WeatherApp/1.0'
        }
        self.cache = {}
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Nominatim requires 1 request per second
    
    def search_cities(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
        """
        Search for cities matching the query
        
        Args:
            query: City name to search for
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries with city information
        """
        if not query or len(query) < 2:
            return []
        
        # Check cache first
        cache_key = f"{query.lower()}_{limit}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Rate limiting - wait if needed
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        try:
            params = {
                'q': query,
                'format': 'json',
                'limit': limit,
                'featuretype': 'city',
                'addressdetails': 1
            }
            
            response = requests.get(
                self.nominatim_url,
                params=params,
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            
            self.last_request_time = time.time()
            
            results = response.json()
            cities = []
            
            for result in results:
                address = result.get('address', {})
                
                # Extract city name (try different fields)
                city_name = (
                    address.get('city') or 
                    address.get('town') or 
                    address.get('village') or
                    address.get('municipality') or
                    result.get('name', '')
                )
                
                # Extract country
                country = address.get('country', 'Unknown')
                country_code = address.get('country_code', '').upper()
                
                # Extract state/region if available
                state = address.get('state', '')
                
                if city_name and country:
                    # Create display name
                    if state and country == 'United States':
                        display_name = f"{city_name}, {state}, {country_code}"
                        search_value = f"{city_name},{state},{country}"
                    else:
                        display_name = f"{city_name}, {country}"
                        search_value = f"{city_name},{country}"
                    
                    cities.append({
                        'display': display_name,
                        'value': search_value,
                        'city': city_name,
                        'country': country,
                        'country_code': country_code,
                        'state': state
                    })
            
            # Remove duplicates based on display name
            seen = set()
            unique_cities = []
            for city in cities:
                if city['display'] not in seen:
                    seen.add(city['display'])
                    unique_cities.append(city)
            
            # Cache the results
            self.cache[cache_key] = unique_cities
            
            return unique_cities
            
        except Exception as e:
            print(f"Error searching cities: {e}")
            return []
    
    def get_top_cities(self) -> List[Dict[str, str]]:
        """
        Get a list of popular cities for quick access
        
        Returns:
            List of popular cities with their countries
        """
        popular_cities = [
            {'display': 'London, United Kingdom', 'value': 'London,UK', 'city': 'London', 'country': 'United Kingdom'},
            {'display': 'New York, United States', 'value': 'New York,USA', 'city': 'New York', 'country': 'United States'},
            {'display': 'Tokyo, Japan', 'value': 'Tokyo,Japan', 'city': 'Tokyo', 'country': 'Japan'},
            {'display': 'Paris, France', 'value': 'Paris,France', 'city': 'Paris', 'country': 'France'},
            {'display': 'Dubai, United Arab Emirates', 'value': 'Dubai,UAE', 'city': 'Dubai', 'country': 'UAE'},
            {'display': 'Riyadh, Saudi Arabia', 'value': 'Riyadh,Saudi Arabia', 'city': 'Riyadh', 'country': 'Saudi Arabia'},
            {'display': 'Singapore, Singapore', 'value': 'Singapore,Singapore', 'city': 'Singapore', 'country': 'Singapore'},
            {'display': 'Sydney, Australia', 'value': 'Sydney,Australia', 'city': 'Sydney', 'country': 'Australia'},
            {'display': 'Berlin, Germany', 'value': 'Berlin,Germany', 'city': 'Berlin', 'country': 'Germany'},
            {'display': 'Toronto, Canada', 'value': 'Toronto,Canada', 'city': 'Toronto', 'country': 'Canada'},
        ]
        return popular_cities
