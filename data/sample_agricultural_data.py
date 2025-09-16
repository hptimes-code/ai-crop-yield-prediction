import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_agricultural_data():
    """
    Generate comprehensive agricultural training data for crop yield prediction models
    
    Returns:
        pandas.DataFrame: Training dataset with soil, weather, and yield data
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Number of samples per crop
    samples_per_crop = 1000
    crops = ['Wheat', 'Corn', 'Rice', 'Soybeans']
    
    all_data = []
    
    for crop in crops:
        crop_data = _generate_crop_data(crop, samples_per_crop)
        all_data.extend(crop_data)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Add some realistic correlations and adjustments
    df = _apply_realistic_correlations(df)
    
    return df

def _generate_crop_data(crop_type, num_samples):
    """Generate data for a specific crop type"""
    
    # Crop-specific parameter ranges based on agricultural research
    crop_parameters = {
        'Wheat': {
            'ph_range': (5.8, 7.2),
            'organic_matter_range': (1.5, 6.0),
            'nitrogen_range': (15, 60),
            'phosphorus_range': (10, 45),
            'potassium_range': (80, 250),
            'temperature_range': (12, 28),
            'rainfall_range': (400, 1200),
            'humidity_range': (45, 75),
            'base_yield': 4.5,
            'yield_variance': 2.0
        },
        'Corn': {
            'ph_range': (5.5, 7.0),
            'organic_matter_range': (2.0, 6.5),
            'nitrogen_range': (25, 80),
            'phosphorus_range': (15, 50),
            'potassium_range': (100, 300),
            'temperature_range': (18, 32),
            'rainfall_range': (600, 1500),
            'humidity_range': (55, 85),
            'base_yield': 7.5,
            'yield_variance': 3.0
        },
        'Rice': {
            'ph_range': (5.0, 6.8),
            'organic_matter_range': (2.5, 7.0),
            'nitrogen_range': (20, 50),
            'phosphorus_range': (8, 35),
            'potassium_range': (90, 220),
            'temperature_range': (22, 38),
            'rainfall_range': (800, 2500),
            'humidity_range': (65, 95),
            'base_yield': 5.8,
            'yield_variance': 2.5
        },
        'Soybeans': {
            'ph_range': (5.8, 7.2),
            'organic_matter_range': (2.0, 5.5),
            'nitrogen_range': (10, 35),  # Lower due to nitrogen fixation
            'phosphorus_range': (12, 40),
            'potassium_range': (90, 280),
            'temperature_range': (16, 30),
            'rainfall_range': (500, 1300),
            'humidity_range': (50, 80),
            'base_yield': 3.2,
            'yield_variance': 1.5
        }
    }
    
    params = crop_parameters[crop_type]
    data = []
    
    for i in range(num_samples):
        # Generate soil parameters
        ph = np.random.uniform(*params['ph_range'])
        organic_matter = np.random.gamma(2, 1.5) + params['organic_matter_range'][0]
        organic_matter = min(organic_matter, params['organic_matter_range'][1])
        
        nitrogen = np.random.gamma(3, params['nitrogen_range'][1]/6)
        nitrogen = np.clip(nitrogen, *params['nitrogen_range'])
        
        phosphorus = np.random.gamma(2.5, params['phosphorus_range'][1]/5)
        phosphorus = np.clip(phosphorus, *params['phosphorus_range'])
        
        potassium = np.random.gamma(4, params['potassium_range'][1]/8)
        potassium = np.clip(potassium, *params['potassium_range'])
        
        # Generate weather parameters
        temperature = np.random.normal(
            (params['temperature_range'][0] + params['temperature_range'][1]) / 2,
            (params['temperature_range'][1] - params['temperature_range'][0]) / 6
        )
        temperature = np.clip(temperature, *params['temperature_range'])
        
        rainfall = np.random.gamma(2, params['rainfall_range'][1]/4)
        rainfall = np.clip(rainfall, *params['rainfall_range'])
        
        humidity = np.random.normal(
            (params['humidity_range'][0] + params['humidity_range'][1]) / 2,
            (params['humidity_range'][1] - params['humidity_range'][0]) / 6
        )
        humidity = np.clip(humidity, *params['humidity_range'])
        
        # Calculate yield based on parameters with realistic relationships
        yield_tons_per_ha = _calculate_realistic_yield(
            crop_type, ph, organic_matter, nitrogen, phosphorus, potassium,
            temperature, rainfall, humidity, params
        )
        
        # Add some random variation
        yield_tons_per_ha += np.random.normal(0, params['yield_variance'] * 0.2)
        yield_tons_per_ha = max(0.5, yield_tons_per_ha)  # Minimum realistic yield
        
        data.append({
            'crop_type': crop_type,
            'ph_level': round(ph, 2),
            'organic_matter': round(organic_matter, 2),
            'nitrogen': round(nitrogen, 1),
            'phosphorus': round(phosphorus, 1),
            'potassium': round(potassium, 1),
            'temperature': round(temperature, 1),
            'rainfall': round(rainfall, 0),
            'humidity': round(humidity, 1),
            'yield_tons_per_ha': round(yield_tons_per_ha, 2)
        })
    
    return data

def _calculate_realistic_yield(crop_type, ph, organic_matter, nitrogen, phosphorus, 
                              potassium, temperature, rainfall, humidity, params):
    """Calculate realistic yield based on agricultural science principles"""
    
    base_yield = params['base_yield']
    
    # pH effect on yield (each crop has optimal pH range)
    optimal_ph = {
        'Wheat': 6.5,
        'Corn': 6.2,
        'Rice': 5.8,
        'Soybeans': 6.8
    }
    
    ph_optimal = optimal_ph[crop_type]
    ph_effect = 1.0 - (abs(ph - ph_optimal) * 0.15)  # 15% yield loss per pH unit deviation
    ph_effect = max(0.3, ph_effect)  # Minimum 30% of base yield
    
    # Organic matter effect (generally positive)
    om_effect = 0.8 + (organic_matter / 10.0)  # Base 80% + bonus from OM
    om_effect = min(1.3, om_effect)  # Cap at 130%
    
    # Nutrient effects (Liebig's law - limited by most deficient nutrient)
    optimal_nutrients = {
        'Wheat': {'N': 35, 'P': 25, 'K': 150},
        'Corn': {'N': 50, 'P': 30, 'K': 180},
        'Rice': {'N': 30, 'P': 20, 'K': 130},
        'Soybeans': {'N': 20, 'P': 25, 'K': 160}  # Lower N due to fixation
    }
    
    crop_nutrients = optimal_nutrients[crop_type]
    
    n_effect = min(1.0, nitrogen / crop_nutrients['N'])
    p_effect = min(1.0, phosphorus / crop_nutrients['P'])
    k_effect = min(1.0, potassium / crop_nutrients['K'])
    
    # Limiting nutrient effect (Liebig's law)
    nutrient_effect = min(n_effect, p_effect, k_effect)
    nutrient_effect = max(0.2, nutrient_effect)  # Minimum 20%
    
    # Temperature effect (each crop has optimal range)
    optimal_temp = {
        'Wheat': 20,
        'Corn': 25,
        'Rice': 30,
        'Soybeans': 23
    }
    
    temp_optimal = optimal_temp[crop_type]
    temp_deviation = abs(temperature - temp_optimal)
    temp_effect = 1.0 - (temp_deviation * 0.03)  # 3% loss per degree deviation
    temp_effect = max(0.4, temp_effect)  # Minimum 40%
    
    # Rainfall effect (crop-specific water needs)
    optimal_rainfall = {
        'Wheat': 600,
        'Corn': 900,
        'Rice': 1500,
        'Soybeans': 750
    }
    
    rain_optimal = optimal_rainfall[crop_type]
    if rainfall < rain_optimal:
        rain_effect = rainfall / rain_optimal
    else:
        # Excess rainfall can also reduce yield
        excess = rainfall - rain_optimal
        rain_effect = 1.0 - (excess / rain_optimal * 0.3)
    
    rain_effect = max(0.3, min(1.2, rain_effect))
    
    # Humidity effect (moderate impact)
    optimal_humidity = {
        'Wheat': 60,
        'Corn': 70,
        'Rice': 80,
        'Soybeans': 65
    }
    
    hum_optimal = optimal_humidity[crop_type]
    hum_deviation = abs(humidity - hum_optimal)
    hum_effect = 1.0 - (hum_deviation * 0.01)  # 1% loss per % deviation
    hum_effect = max(0.7, hum_effect)  # Minimum 70%
    
    # Calculate final yield
    final_yield = (base_yield * ph_effect * om_effect * nutrient_effect * 
                   temp_effect * rain_effect * hum_effect)
    
    # Add some interaction effects
    # High temperature + low humidity = stress
    if temperature > temp_optimal + 5 and humidity < hum_optimal - 10:
        final_yield *= 0.85  # 15% stress penalty
    
    # Good conditions synergy
    if (ph_effect > 0.9 and nutrient_effect > 0.8 and temp_effect > 0.9 and 
        rain_effect > 0.9):
        final_yield *= 1.1  # 10% synergy bonus
    
    return final_yield

def _apply_realistic_correlations(df):
    """Apply realistic correlations between parameters"""
    
    # Add some realistic correlations
    for crop in df['crop_type'].unique():
        crop_mask = df['crop_type'] == crop
        crop_data = df[crop_mask].copy()
        
        # Higher organic matter often correlates with higher nitrogen
        high_om_mask = crop_data['organic_matter'] > crop_data['organic_matter'].median()
        df.loc[crop_mask & high_om_mask, 'nitrogen'] *= np.random.uniform(1.05, 1.2, sum(crop_mask & high_om_mask))
        
        # Temperature and humidity often inversely related
        high_temp_mask = crop_data['temperature'] > crop_data['temperature'].median()
        df.loc[crop_mask & high_temp_mask, 'humidity'] *= np.random.uniform(0.85, 0.95, sum(crop_mask & high_temp_mask))
        
        # Regions with high rainfall often have different soil characteristics
        high_rain_mask = crop_data['rainfall'] > crop_data['rainfall'].median()
        df.loc[crop_mask & high_rain_mask, 'potassium'] *= np.random.uniform(0.9, 1.1, sum(crop_mask & high_rain_mask))
    
    # Ensure all values are within reasonable bounds after adjustments
    df['ph_level'] = np.clip(df['ph_level'], 4.0, 9.0)
    df['organic_matter'] = np.clip(df['organic_matter'], 0.5, 10.0)
    df['nitrogen'] = np.clip(df['nitrogen'], 5, 100)
    df['phosphorus'] = np.clip(df['phosphorus'], 5, 100)
    df['potassium'] = np.clip(df['potassium'], 50, 500)
    df['temperature'] = np.clip(df['temperature'], 5, 45)
    df['rainfall'] = np.clip(df['rainfall'], 200, 3000)
    df['humidity'] = np.clip(df['humidity'], 20, 100)
    df['yield_tons_per_ha'] = np.clip(df['yield_tons_per_ha'], 0.5, 15.0)
    
    return df

def get_historical_yield_data():
    """
    Generate historical yield trend data for visualization
    
    Returns:
        pandas.DataFrame: Historical yield data by year and crop
    """
    
    years = range(2015, 2025)
    crops = ['Wheat', 'Corn', 'Rice', 'Soybeans']
    
    # Base yields (global averages in tons/hectare)
    base_yields = {
        'Wheat': 3.4,
        'Corn': 5.9,
        'Rice': 4.6,
        'Soybeans': 2.8
    }
    
    # Trends (annual change rate)
    trends = {
        'Wheat': 0.02,   # 2% annual improvement
        'Corn': 0.015,   # 1.5% annual improvement
        'Rice': 0.01,    # 1% annual improvement
        'Soybeans': 0.025 # 2.5% annual improvement
    }
    
    historical_data = []
    
    for crop in crops:
        base_yield = base_yields[crop]
        trend = trends[crop]
        
        for i, year in enumerate(years):
            # Calculate yield with trend and some random variation
            year_yield = base_yield * (1 + trend) ** i
            year_yield += np.random.normal(0, base_yield * 0.1)  # 10% random variation
            year_yield = max(year_yield * 0.5, year_yield)  # Minimum threshold
            
            historical_data.append({
                'year': year,
                'crop': crop,
                'yield_tons_per_ha': round(year_yield, 2),
                'area_harvested_million_ha': np.random.uniform(50, 200),  # Mock area data
                'production_million_tons': round(year_yield * np.random.uniform(50, 200), 1)
            })
    
    return pd.DataFrame(historical_data)

def get_regional_yield_data():
    """
    Generate regional yield comparison data
    
    Returns:
        pandas.DataFrame: Regional yield data
    """
    
    regions = [
        'North America', 'Europe', 'Asia', 'South America', 
        'Africa', 'Oceania'
    ]
    
    crops = ['Wheat', 'Corn', 'Rice', 'Soybeans']
    
    # Regional yield factors (relative to global average)
    regional_factors = {
        'North America': {'Wheat': 1.2, 'Corn': 1.4, 'Rice': 1.1, 'Soybeans': 1.3},
        'Europe': {'Wheat': 1.3, 'Corn': 1.0, 'Rice': 1.2, 'Soybeans': 1.1},
        'Asia': {'Wheat': 0.9, 'Corn': 0.8, 'Rice': 1.0, 'Soybeans': 0.9},
        'South America': {'Wheat': 1.0, 'Corn': 1.1, 'Rice': 0.9, 'Soybeans': 1.2},
        'Africa': {'Wheat': 0.7, 'Corn': 0.6, 'Rice': 0.8, 'Soybeans': 0.7},
        'Oceania': {'Wheat': 1.1, 'Corn': 1.2, 'Rice': 1.3, 'Soybeans': 1.0}
    }
    
    base_yields = {
        'Wheat': 3.4,
        'Corn': 5.9,
        'Rice': 4.6,
        'Soybeans': 2.8
    }
    
    regional_data = []
    
    for region in regions:
        for crop in crops:
            base_yield = base_yields[crop]
            factor = regional_factors[region][crop]
            regional_yield = base_yield * factor
            
            # Add some variation
            regional_yield += np.random.normal(0, regional_yield * 0.05)
            regional_yield = max(0.5, regional_yield)
            
            regional_data.append({
                'region': region,
                'crop': crop,
                'avg_yield_tons_per_ha': round(regional_yield, 2),
                'climate_suitability': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor']),
                'technology_adoption': np.random.uniform(0.3, 0.9)
            })
    
    return pd.DataFrame(regional_data)

# For testing purposes
if __name__ == "__main__":
    # Generate and display sample data
    df = get_agricultural_data()
    print("Sample Agricultural Data:")
    print(df.head(10))
    print(f"\nDataset shape: {df.shape}")
    print(f"\nCrops included: {df['crop_type'].unique()}")
    print(f"\nYield statistics by crop:")
    print(df.groupby('crop_type')['yield_tons_per_ha'].describe())
    
    # Generate historical data
    historical_df = get_historical_yield_data()
    print(f"\nHistorical data shape: {historical_df.shape}")
    
    # Generate regional data
    regional_df = get_regional_yield_data()
    print(f"\nRegional data shape: {regional_df.shape}")
