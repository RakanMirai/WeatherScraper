"""
Data Storage Module
Manages historical weather data and search history
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict


class DataStorage:
    """Handles storage and retrieval of weather data and search history"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, "weather_history.json")
        self.search_file = os.path.join(data_dir, "search_history.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        if not os.path.exists(self.history_file):
            self._write_json(self.history_file, {})
        if not os.path.exists(self.search_file):
            self._write_json(self.search_file, [])
    
    def save_weather_data(self, city: str, weather_data: dict):
        """
        Save weather data for a city
        
        Args:
            city: City name
            weather_data: Weather data dictionary
        """
        history = self._read_json(self.history_file)
        
        city_key = city.lower()
        if city_key not in history:
            history[city_key] = []
        
        # Add timestamp if not present
        if 'timestamp' not in weather_data:
            weather_data['timestamp'] = datetime.now().isoformat()
        
        history[city_key].append(weather_data)
        
        # Clean old data (keep only current week)
        history[city_key] = self._filter_current_week(history[city_key])
        
        self._write_json(self.history_file, history)
    
    def get_weather_history(self, city: str) -> List[dict]:
        """
        Get weather history for a city (current week only)
        
        Args:
            city: City name
            
        Returns:
            List of weather data dictionaries
        """
        history = self._read_json(self.history_file)
        city_key = city.lower()
        
        if city_key not in history:
            return []
        
        # Filter to current week only
        return self._filter_current_week(history[city_key])
    
    def add_search(self, city: str):
        """
        Add a city to search history
        
        Args:
            city: City name
        """
        searches = self._read_json(self.search_file)
        
        search_entry = {
            'city': city,
            'timestamp': datetime.now().isoformat()
        }
        
        # Remove duplicate if exists
        searches = [s for s in searches if s['city'].lower() != city.lower()]
        
        # Add to beginning
        searches.insert(0, search_entry)
        
        # Keep only last 20 searches
        searches = searches[:20]
        
        self._write_json(self.search_file, searches)
    
    def get_search_history(self) -> List[str]:
        """
        Get list of recently searched cities
        
        Returns:
            List of city names
        """
        searches = self._read_json(self.search_file)
        return [s['city'] for s in searches]
    
    def clear_old_data(self):
        """Clear weather data from previous weeks"""
        history = self._read_json(self.history_file)
        
        for city in history:
            history[city] = self._filter_current_week(history[city])
        
        self._write_json(self.history_file, history)
    
    def _filter_current_week(self, data_list: List[dict]) -> List[dict]:
        """
        Filter data to only include entries from current week
        Week starts on Monday
        
        Args:
            data_list: List of weather data dictionaries
            
        Returns:
            Filtered list
        """
        now = datetime.now()
        
        # Get Monday of current week
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        filtered = []
        for entry in data_list:
            try:
                timestamp = datetime.fromisoformat(entry['timestamp'])
                if timestamp >= start_of_week:
                    filtered.append(entry)
            except (KeyError, ValueError):
                # Skip entries with invalid timestamps
                continue
        
        return filtered
    
    def _read_json(self, filepath: str) -> dict | list:
        """Read JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if 'history' in filepath else []
    
    def _write_json(self, filepath: str, data: dict | list):
        """Write JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
