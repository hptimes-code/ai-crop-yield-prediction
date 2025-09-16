import requests
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_weather_data(self, location):
        """
        Get current weather data for a location
        
        Args:
            location (str): City name or coordinates
            
        Returns:
            dict: Weather data or None if error
        """
        try:
            # Current weather endpoint
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    'location': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', 0),
                    'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                    'uv_index': self._estimate_uv_index(data['coord']['lat']),
                    'rainfall_annual': self._estimate_annual_rainfall(location),
                    'timestamp': datetime.now()
                }
            else:
                print(f"Weather API error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Weather service error: {e}")
            # Return mock data for development
            return self._get_mock_weather_data(location)
        except Exception as e:
            print(f"Unexpected error in weather service: {e}")
            return None
    
    def get_forecast_data(self, location, days=7):
        """
        Get weather forecast data
        
        Args:
            location (str): City name or coordinates
            days (int): Number of days to forecast
            
        Returns:
            pandas.DataFrame: Forecast data
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                forecast_data = []
                
                for item in data['list'][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                    forecast_data.append({
                        'date': datetime.fromtimestamp(item['dt']),
                        'temperature': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'description': item['weather'][0]['description'],
                        'wind_speed': item['wind']['speed'],
                        'precipitation': item.get('rain', {}).get('3h', 0)
                    })
                
                return pd.DataFrame(forecast_data)
            else:
                print(f"Forecast API error: {response.status_code}")
                return self._get_mock_forecast_data(location, days)
                
        except Exception as e:
            print(f"Forecast service error: {e}")
            return self._get_mock_forecast_data(location, days)
    
    def _get_mock_weather_data(self, location):
        """Return mock weather data for development/testing"""
        
        # Generate realistic weather data based on location patterns
        base_temp = np.random.uniform(15, 30)
        
        return {
            'location': location.split(',')[0] if ',' in location else location,
            'country': 'Mock',
            'temperature': base_temp,
            'feels_like': base_temp + np.random.uniform(-2, 2),
            'humidity': np.random.uniform(40, 80),
            'pressure': np.random.uniform(1000, 1020),
            'description': np.random.choice(['clear sky', 'few clouds', 'scattered clouds', 'light rain']),
            'wind_speed': np.random.uniform(2, 8),
            'wind_direction': np.random.uniform(0, 360),
            'visibility': np.random.uniform(8, 15),
            'uv_index': np.random.uniform(3, 9),
            'rainfall_annual': np.random.uniform(400, 1200),
            'timestamp': datetime.now()
        }
    
    def _get_mock_forecast_data(self, location, days):
        """Return mock forecast data"""
        
        forecast_data = []
        start_date = datetime.now()
        base_temp = np.random.uniform(15, 30)
        
        for i in range(days * 4):  # 4 forecasts per day
            date = start_date + timedelta(hours=i * 6)
            temp_variation = np.sin(i * 0.1) * 5  # Temperature variation pattern
            
            forecast_data.append({
                'date': date,
                'temperature': base_temp + temp_variation + np.random.uniform(-2, 2),
                'humidity': np.random.uniform(40, 80),
                'description': np.random.choice(['clear sky', 'few clouds', 'light rain']),
                'wind_speed': np.random.uniform(2, 8),
                'precipitation': np.random.uniform(0, 5) if np.random.random() < 0.3 else 0
            })
        
        return pd.DataFrame(forecast_data)
    
    def _estimate_uv_index(self, latitude):
        """Estimate UV index based on latitude"""
        
        # Simple estimation based on latitude
        abs_lat = abs(latitude)
        if abs_lat < 23.5:  # Tropics
            return np.random.uniform(8, 12)
        elif abs_lat < 40:  # Subtropical
            return np.random.uniform(6, 9)
        else:  # Temperate
            return np.random.uniform(3, 7)
    
    def _estimate_annual_rainfall(self, location):
        """Estimate annual rainfall based on location"""
        
        # Very basic estimation - in reality, this would use historical data
        location_lower = location.lower()
        
        if any(region in location_lower for region in ['desert', 'arizona', 'nevada']):
            return np.random.uniform(100, 400)
        elif any(region in location_lower for region in ['tropical', 'florida', 'hawaii']):
            return np.random.uniform(1200, 2500)
        elif any(region in location_lower for region in ['seattle', 'oregon', 'washington']):
            return np.random.uniform(800, 1500)
        else:
            return np.random.uniform(500, 1200)
    
    def assess_agricultural_impact(self, weather_data):
        """
        Assess the impact of current weather conditions on different crops
        
        Args:
            weather_data (dict): Current weather data
            
        Returns:
            dict: Impact assessment for each crop type
        """
        
        temperature = weather_data['temperature']
        humidity = weather_data['humidity']
        description = weather_data['description'].lower()
        
        crops = ['Wheat', 'Corn', 'Rice', 'Soybeans']
        impact_assessment = {}
        
        for crop in crops:
            impact = self._assess_crop_weather_impact(
                crop, temperature, humidity, description
            )
            impact_assessment[crop] = impact
        
        return impact_assessment
    
    def _assess_crop_weather_impact(self, crop, temperature, humidity, description):
        """Assess weather impact for specific crop"""
        
        # Optimal conditions for each crop
        optimal_conditions = {
            'Wheat': {'temp_range': (15, 25), 'humidity_range': (50, 70)},
            'Corn': {'temp_range': (20, 30), 'humidity_range': (60, 80)},
            'Rice': {'temp_range': (25, 35), 'humidity_range': (70, 90)},
            'Soybeans': {'temp_range': (20, 28), 'humidity_range': (55, 75)}
        }
        
        crop_conditions = optimal_conditions.get(crop, {'temp_range': (15, 30), 'humidity_range': (50, 80)})
        
        # Assess temperature impact
        temp_min, temp_max = crop_conditions['temp_range']
        if temp_min <= temperature <= temp_max:
            temp_impact = "Optimal"
        elif temperature < temp_min - 5 or temperature > temp_max + 5:
            temp_impact = "Poor"
        else:
            temp_impact = "Suboptimal"
        
        # Assess humidity impact
        hum_min, hum_max = crop_conditions['humidity_range']
        if hum_min <= humidity <= hum_max:
            hum_impact = "Good"
        else:
            hum_impact = "Suboptimal"
        
        # Overall impact assessment
        if temp_impact == "Optimal" and hum_impact == "Good":
            overall_impact = "Favorable"
        elif temp_impact == "Poor":
            overall_impact = "Unfavorable"
        else:
            overall_impact = "Moderate"
        
        # Generate recommendations
        recommendations = self._generate_weather_recommendations(
            crop, temperature, humidity, description, overall_impact
        )
        
        return {
            'impact': overall_impact,
            'temperature_impact': temp_impact,
            'humidity_impact': hum_impact,
            'recommendation': recommendations
        }
    
    def _generate_weather_recommendations(self, crop, temp, humidity, description, impact):
        """Generate weather-based recommendations"""
        
        recommendations = []
        
        if "rain" in description:
            recommendations.append("Monitor for waterlogging and fungal diseases")
            recommendations.append("Ensure proper drainage in fields")
        
        if temp > 30:
            recommendations.append("Consider additional irrigation during hot weather")
            recommendations.append("Monitor plants for heat stress")
        elif temp < 15:
            recommendations.append("Protect crops from potential frost damage")
            recommendations.append("Consider covering sensitive plants")
        
        if humidity > 80:
            recommendations.append("Increase ventilation to prevent fungal growth")
            recommendations.append("Monitor for pest activity in high humidity")
        elif humidity < 50:
            recommendations.append("Consider supplemental irrigation")
            recommendations.append("Monitor soil moisture levels closely")
        
        if impact == "Unfavorable":
            recommendations.append(f"Consider postponing field activities for {crop}")
            recommendations.append("Implement protective measures immediately")
        
        if not recommendations:
            recommendations.append("Weather conditions are favorable for normal farming activities")
        
        return " | ".join(recommendations[:3])  # Limit to top 3 recommendations
    
    def get_weather_alerts(self, location):
        """Get weather alerts and warnings for the location"""
        
        try:
            # In a real implementation, this would call weather alerts API
            # For now, return mock alerts based on weather conditions
            weather_data = self.get_weather_data(location)
            
            if not weather_data:
                return []
            
            alerts = []
            temp = weather_data['temperature']
            humidity = weather_data['humidity']
            description = weather_data['description']
            
            # Temperature alerts
            if temp > 35:
                alerts.append({
                    'type': 'Heat Warning',
                    'severity': 'High',
                    'message': 'Extreme heat conditions. Take precautions for crops and livestock.',
                    'recommendations': ['Increase irrigation', 'Provide shade for animals', 'Avoid field work during peak hours']
                })
            elif temp < 5:
                alerts.append({
                    'type': 'Frost Alert',
                    'severity': 'High',
                    'message': 'Freezing temperatures expected. Protect sensitive crops.',
                    'recommendations': ['Cover tender plants', 'Use frost protection methods', 'Harvest mature crops']
                })
            
            # Precipitation alerts
            if "heavy rain" in description or "thunderstorm" in description:
                alerts.append({
                    'type': 'Heavy Rain Warning',
                    'severity': 'Medium',
                    'message': 'Heavy rainfall expected. Prepare for potential flooding.',
                    'recommendations': ['Check drainage systems', 'Secure loose equipment', 'Monitor soil erosion']
                })
            
            return alerts
            
        except Exception as e:
            print(f"Error getting weather alerts: {e}")
            return []
