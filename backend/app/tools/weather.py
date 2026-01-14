"""
Weather Tool
Get current weather information for any city using OpenWeatherMap API

Features:
- Current weather conditions
- Temperature (Celsius and Fahrenheit)
- Humidity, wind speed, pressure
- Weather description
- Caching to reduce API calls
"""

import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherTool:
    """
    Weather tool using OpenWeatherMap API.
    
    Free tier: 1000 calls/day, 60 calls/minute
    """
    
    def __init__(self):
        """Initialize with API key"""
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        # Cache weather data (5 minutes cache)
        self._cache = {}
        self._cache_duration = 300  # seconds
        
        logger.info("WeatherTool initialized")
    
    def get_weather(self, city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current weather for a city.
        
        Args:
            city: City name (e.g., "Lagos", "London")
            country_code: Optional 2-letter country code (e.g., "NG", "GB")
            
        Returns:
            Dict with weather data
        """
        try:
            # Build location query
            location = city
            if country_code:
                location = f"{city},{country_code}"
            
            logger.info(f"Getting weather for: {location}")
            
            # Check cache
            cached_data = self._get_from_cache(location)
            if cached_data:
                logger.info("Using cached weather data")
                return cached_data
            
            # If no API key, return mock data
            if not self.api_key or self.api_key == "your_openweather_api_key_here":
                logger.warning("Using mock weather data (no API key)")
                return self._get_mock_weather(city, country_code)
            
            # Call OpenWeatherMap API
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'  # Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response
            weather_data = {
                'success': True,
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp'], 1),
                'temperature_fahrenheit': round(data['main']['temp'] * 9/5 + 32, 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'description': data['weather'][0]['description'].capitalize(),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': round(data['wind']['speed'], 1),
                'clouds': data['clouds']['all'],
                'timestamp': datetime.now().isoformat(),
                'explanation': self._format_weather_explanation(data)
            }
            
            # Cache the result
            self._add_to_cache(location, weather_data)
            
            return weather_data
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.error(f"City not found: {location}")
                return {
                    'success': False,
                    'error': f'City "{city}" not found',
                    'explanation': f'Could not find weather data for {city}'
                }
            else:
                logger.error(f"API error: {str(e)}")
                return {
                    'success': False,
                    'error': str(e),
                    'explanation': 'Weather API error'
                }
                
        except Exception as e:
            logger.error(f"Error getting weather: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': 'Could not fetch weather data'
            }
    
    def _format_weather_explanation(self, data: Dict) -> str:
        """
        Format weather data into human-readable explanation.
        
        Args:
            data: Raw API response data
            
        Returns:
            Formatted weather description
        """
        city = data['name']
        country = data['sys']['country']
        temp_c = round(data['main']['temp'], 1)
        temp_f = round(temp_c * 9/5 + 32, 1)
        description = data['weather'][0]['description']
        feels_like = round(data['main']['feels_like'], 1)
        humidity = data['main']['humidity']
        wind_speed = round(data['wind']['speed'], 1)
        
        return (
            f"Current weather in {city}, {country}: "
            f"{description} with temperature of {temp_c}°C ({temp_f}°F). "
            f"Feels like {feels_like}°C. "
            f"Humidity: {humidity}%, Wind speed: {wind_speed} m/s."
        )
    
    def _get_from_cache(self, location: str) -> Optional[Dict]:
        """Get cached weather data if still valid"""
        if location in self._cache:
            cached_item = self._cache[location]
            age = (datetime.now() - cached_item['cached_at']).seconds
            
            if age < self._cache_duration:
                return cached_item['data']
            else:
                # Remove stale cache
                del self._cache[location]
        
        return None
    
    def _add_to_cache(self, location: str, data: Dict):
        """Add weather data to cache"""
        self._cache[location] = {
            'data': data,
            'cached_at': datetime.now()
        }
    
    def _get_mock_weather(self, city: str, country_code: Optional[str]) -> Dict[str, Any]:
        """
        Return mock weather data for testing without API key.
        """
        # Mock data for common cities
        mock_data = {
            'lagos': {'temp': 28, 'desc': 'Partly cloudy', 'humidity': 75, 'wind': 3.5},
            'london': {'temp': 12, 'desc': 'Rainy', 'humidity': 80, 'wind': 5.0},
            'new york': {'temp': 18, 'desc': 'Clear sky', 'humidity': 60, 'wind': 4.2},
            'tokyo': {'temp': 20, 'desc': 'Cloudy', 'humidity': 65, 'wind': 3.0},
        }
        
        city_lower = city.lower()
        weather = mock_data.get(city_lower, mock_data['lagos'])
        
        temp_c = weather['temp']
        temp_f = round(temp_c * 9/5 + 32, 1)
        
        return {
            'success': True,
            'city': city.title(),
            'country': country_code or 'XX',
            'temperature': temp_c,
            'temperature_fahrenheit': temp_f,
            'feels_like': temp_c - 1,
            'description': weather['desc'],
            'humidity': weather['humidity'],
            'pressure': 1013,
            'wind_speed': weather['wind'],
            'clouds': 50,
            'timestamp': datetime.now().isoformat(),
            'explanation': (
                f"Current weather in {city}: {weather['desc']} "
                f"with temperature of {temp_c}°C ({temp_f}°F). "
                f"Humidity: {weather['humidity']}%, Wind speed: {weather['wind']} m/s. "
                f"[MOCK DATA - No API key configured]"
            )
        }


# LangChain Tool wrapper
def get_weather_tool_for_langchain():
    """
    Create LangChain-compatible weather tool.
    """
    weather_tool = WeatherTool()
    
    def weather_wrapper(city: str) -> str:
        """
        Get current weather for a city.
        
        Args:
            city: City name, optionally with country code (e.g., "Lagos, NG")
            
        Returns:
            Weather information as string
        """
        # Parse city and country code
        parts = city.split(',')
        city_name = parts[0].strip()
        country_code = parts[1].strip() if len(parts) > 1 else None
        
        result = weather_tool.get_weather(city_name, country_code)
        
        if result['success']:
            return result['explanation']
        else:
            return f"Error: {result.get('error', 'Could not fetch weather')}"
    
    return weather_wrapper


# Example usage and testing
if __name__ == "__main__":
    weather = WeatherTool()
    
    print("🧪 Testing Weather Tool\n")
    
    # Test 1: Lagos
    print("1️⃣ Lagos, Nigeria:")
    result = weather.get_weather("Lagos", "NG")
    print(f"   {result['explanation']}\n")
    
    # Test 2: London
    print("2️⃣ London, UK:")
    result = weather.get_weather("London", "GB")
    print(f"   {result['explanation']}\n")
    
    # Test 3: New York
    print("3️⃣ New York, USA:")
    result = weather.get_weather("New York", "US")
    print(f"   {result['explanation']}\n")
    
    # Test 4: Invalid city
    print("4️⃣ Invalid city:")
    result = weather.get_weather("InvalidCityName12345")
    print(f"   {result.get('explanation', result.get('error'))}\n")
    
    print("✅ All tests completed!")