import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

class RecommendationEngine:
    def __init__(self):
        self.crop_data = {
            'Wheat': {
                'growth_stages': ['Seedling', 'Vegetative', 'Flowering', 'Maturity'],
                'growing_season': {'start': 'October', 'end': 'June'},
                'water_needs': 'Medium',
                'fertilizer_schedule': {
                    'Seedling': ['Phosphorus-rich starter', 'Light nitrogen'],
                    'Vegetative': ['High nitrogen', 'Potassium'],
                    'Flowering': ['Balanced NPK', 'Micronutrients'],
                    'Maturity': ['Minimal fertilizer', 'Potassium boost']
                },
                'common_pests': ['Aphids', 'Wheat rust', 'Armyworms'],
                'optimal_conditions': {
                    'temperature': (15, 25),
                    'humidity': (50, 70),
                    'soil_ph': (6.0, 7.0)
                }
            },
            'Corn': {
                'growth_stages': ['Seedling', 'Vegetative', 'Flowering', 'Maturity'],
                'growing_season': {'start': 'April', 'end': 'October'},
                'water_needs': 'High',
                'fertilizer_schedule': {
                    'Seedling': ['Starter fertilizer', 'Phosphorus'],
                    'Vegetative': ['Heavy nitrogen', 'Side-dress application'],
                    'Flowering': ['Balanced fertilizer', 'Zinc supplement'],
                    'Maturity': ['Minimal nitrogen', 'Potassium']
                },
                'common_pests': ['Corn borer', 'Rootworm', 'Fall armyworm'],
                'optimal_conditions': {
                    'temperature': (20, 30),
                    'humidity': (60, 80),
                    'soil_ph': (6.0, 6.8)
                }
            },
            'Rice': {
                'growth_stages': ['Seedling', 'Vegetative', 'Flowering', 'Maturity'],
                'growing_season': {'start': 'May', 'end': 'October'},
                'water_needs': 'Very High',
                'fertilizer_schedule': {
                    'Seedling': ['Nitrogen-phosphorus', 'Transplanting fertilizer'],
                    'Vegetative': ['Split nitrogen application', 'Potassium'],
                    'Flowering': ['Panicle initiation fertilizer', 'Micronutrients'],
                    'Maturity': ['Final potassium', 'Harvest preparation']
                },
                'common_pests': ['Rice blast', 'Brown planthopper', 'Stem borer'],
                'optimal_conditions': {
                    'temperature': (25, 35),
                    'humidity': (70, 90),
                    'soil_ph': (5.5, 6.5)
                }
            },
            'Soybeans': {
                'growth_stages': ['Seedling', 'Vegetative', 'Flowering', 'Maturity'],
                'growing_season': {'start': 'May', 'end': 'September'},
                'water_needs': 'Medium-High',
                'fertilizer_schedule': {
                    'Seedling': ['Starter phosphorus', 'Inoculant'],
                    'Vegetative': ['Light nitrogen', 'Potassium'],
                    'Flowering': ['Calcium', 'Boron supplement'],
                    'Maturity': ['Final potassium', 'Harvest timing']
                },
                'common_pests': ['Soybean aphid', 'Bean leaf beetle', 'White mold'],
                'optimal_conditions': {
                    'temperature': (20, 28),
                    'humidity': (55, 75),
                    'soil_ph': (6.0, 7.0)
                }
            }
        }
    
    def generate_recommendations(self, farm_data):
        """
        Generate comprehensive recommendations based on farm data
        
        Args:
            farm_data (dict): Current farm status including crop, stage, location, etc.
            
        Returns:
            dict: Categorized recommendations
        """
        
        crop_type = farm_data.get('crop_type', 'Wheat')
        growth_stage = farm_data.get('growth_stage', 'Vegetative')
        current_date = farm_data.get('current_date', datetime.now())
        region = farm_data.get('region', 'Unknown')
        
        if crop_type not in self.crop_data:
            crop_type = 'Wheat'  # Default fallback
        
        crop_info = self.crop_data[crop_type]
        
        recommendations = {}
        
        # Irrigation recommendations
        recommendations['irrigation'] = self._generate_irrigation_recommendations(
            crop_type, growth_stage, current_date, region
        )
        
        # Fertilization recommendations
        recommendations['fertilization'] = self._generate_fertilization_recommendations(
            crop_type, growth_stage, current_date
        )
        
        # Pest control recommendations
        recommendations['pest_control'] = self._generate_pest_control_recommendations(
            crop_type, growth_stage, current_date
        )
        
        # Harvesting recommendations
        recommendations['harvesting'] = self._generate_harvesting_recommendations(
            crop_type, growth_stage, current_date
        )
        
        return recommendations
    
    def _generate_irrigation_recommendations(self, crop_type, growth_stage, current_date, region):
        """Generate irrigation-specific recommendations"""
        
        crop_info = self.crop_data[crop_type]
        water_needs = crop_info['water_needs']
        
        # Base recommendations by growth stage
        stage_recommendations = {
            'Seedling': {
                'action': 'Light, frequent watering to maintain soil moisture',
                'timing': 'Daily light irrigation or every 2-3 days',
                'priority': 'High',
                'reason': 'Critical establishment phase requiring consistent moisture'
            },
            'Vegetative': {
                'action': 'Deep, less frequent watering to encourage root development',
                'timing': 'Every 3-5 days depending on soil type and weather',
                'priority': 'Medium',
                'reason': 'Building strong root system and vegetative growth'
            },
            'Flowering': {
                'action': 'Consistent moisture critical for flower and fruit development',
                'timing': 'Monitor soil moisture daily, irrigate as needed',
                'priority': 'High',
                'reason': 'Water stress during flowering significantly impacts yield'
            },
            'Maturity': {
                'action': 'Reduce irrigation to prevent quality issues and prepare for harvest',
                'timing': 'Minimal irrigation, only if severe drought conditions',
                'priority': 'Low',
                'reason': 'Excess moisture can delay harvest and reduce grain quality'
            }
        }
        
        base_rec = stage_recommendations.get(growth_stage, stage_recommendations['Vegetative'])
        
        # Adjust based on crop water needs
        if water_needs == 'Very High':
            base_rec['action'] += ' - This crop requires abundant water'
            if base_rec['priority'] == 'Low':
                base_rec['priority'] = 'Medium'
        elif water_needs == 'Low':
            base_rec['action'] += ' - This crop is drought tolerant'
            if base_rec['priority'] == 'High':
                base_rec['priority'] = 'Medium'
        
        # Add seasonal adjustments
        month = current_date.month
        if month in [6, 7, 8]:  # Summer months
            base_rec['details'] = [
                'Increase irrigation frequency during hot summer months',
                'Consider early morning irrigation to reduce evaporation',
                'Monitor for signs of heat stress',
                'Mulch around plants to retain soil moisture'
            ]
        elif month in [12, 1, 2]:  # Winter months
            base_rec['details'] = [
                'Reduce irrigation frequency in cooler weather',
                'Avoid overwatering in low evaporation conditions',
                'Check drainage to prevent waterlogging',
                'Monitor soil temperature before irrigating'
            ]
        else:
            base_rec['details'] = [
                'Monitor weather forecasts before scheduling irrigation',
                'Check soil moisture at 6-inch depth before watering',
                'Adjust timing based on recent rainfall',
                'Maintain consistent moisture levels'
            ]
        
        return base_rec
    
    def _generate_fertilization_recommendations(self, crop_type, growth_stage, current_date):
        """Generate fertilization recommendations"""
        
        crop_info = self.crop_data[crop_type]
        fertilizer_schedule = crop_info['fertilizer_schedule']
        
        stage_fertilizers = fertilizer_schedule.get(growth_stage, ['Balanced NPK'])
        
        # Base recommendation structure
        recommendation = {
            'action': f'Apply {", ".join(stage_fertilizers)} suitable for {growth_stage.lower()} stage',
            'timing': self._get_fertilizer_timing(growth_stage),
            'priority': self._get_fertilizer_priority(growth_stage),
            'reason': f'{growth_stage} stage requires specific nutrients for optimal development'
        }
        
        # Add detailed instructions
        details = []
        
        if growth_stage == 'Seedling':
            details.extend([
                'Use starter fertilizer with higher phosphorus content',
                'Apply at planting or within first 2 weeks',
                'Avoid high nitrogen that can burn young plants',
                'Consider soil test results for precise application rates'
            ])
        elif growth_stage == 'Vegetative':
            details.extend([
                'Apply nitrogen-rich fertilizer to promote leaf and stem growth',
                'Side-dress application recommended for row crops',
                'Split application to reduce nutrient loss',
                'Monitor plants for nitrogen deficiency signs (yellowing leaves)'
            ])
        elif growth_stage == 'Flowering':
            details.extend([
                'Switch to balanced NPK fertilizer',
                'Add micronutrients (zinc, boron, iron) if deficient',
                'Avoid excessive nitrogen that can delay flowering',
                'Apply before peak flowering for maximum benefit'
            ])
        elif growth_stage == 'Maturity':
            details.extend([
                'Reduce or eliminate nitrogen application',
                'Final potassium application to improve grain quality',
                'Avoid fertilizer that delays harvest maturity',
                'Focus on harvest preparation rather than growth'
            ])
        
        recommendation['details'] = details
        
        return recommendation
    
    def _generate_pest_control_recommendations(self, crop_type, growth_stage, current_date):
        """Generate pest control recommendations"""
        
        crop_info = self.crop_data[crop_type]
        common_pests = crop_info['common_pests']
        
        # Seasonal pest pressure
        month = current_date.month
        seasonal_risk = 'Medium'
        
        if month in [5, 6, 7, 8, 9]:  # Growing season
            seasonal_risk = 'High'
        elif month in [3, 4, 10]:  # Transition periods
            seasonal_risk = 'Medium'
        else:
            seasonal_risk = 'Low'
        
        recommendation = {
            'action': f'Monitor for {", ".join(common_pests[:2])} and other common pests',
            'timing': 'Weekly scouting recommended during growing season',
            'priority': seasonal_risk,
            'reason': f'Seasonal pest pressure is {seasonal_risk.lower()} for this time of year'
        }
        
        # Stage-specific recommendations
        details = []
        
        if growth_stage == 'Seedling':
            details.extend([
                'Focus on soil-dwelling pests and cutworms',
                'Use physical barriers or targeted treatments',
                'Monitor for damping-off diseases',
                'Inspect plants every 2-3 days for early detection'
            ])
        elif growth_stage == 'Vegetative':
            details.extend([
                'Scout for leaf-feeding insects and caterpillars',
                'Check undersides of leaves for eggs and larvae',
                'Monitor growth points for damage',
                'Implement beneficial insect habitat if using IPM'
            ])
        elif growth_stage == 'Flowering':
            details.extend([
                'Watch for pollinators before applying any treatments',
                'Focus on flower and developing fruit protection',
                'Monitor for disease symptoms in humid conditions',
                'Avoid spraying during peak pollinator activity'
            ])
        elif growth_stage == 'Maturity':
            details.extend([
                'Inspect for storage pest prevention',
                'Monitor grain moisture to prevent mold',
                'Scout for late-season pests that affect quality',
                'Prepare for post-harvest pest management'
            ])
        
        # Add crop-specific pest details
        details.append(f'Common pests for {crop_type}: {", ".join(common_pests)}')
        
        recommendation['details'] = details
        
        return recommendation
    
    def _generate_harvesting_recommendations(self, crop_type, growth_stage, current_date):
        """Generate harvesting recommendations"""
        
        if growth_stage != 'Maturity':
            return {
                'action': f'Continue monitoring crop development - not ready for harvest',
                'timing': f'Harvesting typically begins when crop reaches maturity stage',
                'priority': 'Low',
                'reason': f'Crop is currently in {growth_stage.lower()} stage',
                'details': [
                    'Monitor crop development daily',
                    'Look for signs of maturity (grain color, moisture content)',
                    'Prepare harvesting equipment and storage facilities',
                    'Plan harvest logistics and labor requirements'
                ]
            }
        
        # Maturity stage recommendations
        crop_info = self.crop_data[crop_type]
        
        recommendation = {
            'action': 'Crop is approaching harvest readiness - begin harvest preparations',
            'timing': 'Monitor daily for optimal harvest window',
            'priority': 'High',
            'reason': 'Proper timing is critical for maximizing yield and quality'
        }
        
        details = []
        
        if crop_type == 'Wheat':
            details.extend([
                'Check grain moisture content (target: 12-14% for storage)',
                'Test grain hardness and protein content',
                'Monitor weather forecasts for dry harvest conditions',
                'Prepare combine harvester and grain storage facilities'
            ])
        elif crop_type == 'Corn':
            details.extend([
                'Monitor grain moisture (target: 15-20% for field drying)',
                'Check for black layer formation at kernel base',
                'Assess stalk strength to prevent lodging',
                'Prepare for grain drying if moisture is high'
            ])
        elif crop_type == 'Rice':
            details.extend([
                'Check grain filling and color change',
                'Monitor panicle moisture content',
                'Plan for proper field drying before threshing',
                'Prepare threshing and winnowing equipment'
            ])
        elif crop_type == 'Soybeans':
            details.extend([
                'Check pod color and rattle test',
                'Monitor grain moisture (target: 13-15% for storage)',
                'Assess plant maturity uniformity across field',
                'Prepare combine settings for soybean harvest'
            ])
        
        # Add general harvest details
        details.extend([
            'Schedule harvest during optimal weather windows',
            'Coordinate labor and equipment availability',
            'Prepare post-harvest handling and storage systems',
            'Plan for immediate post-harvest field operations'
        ])
        
        recommendation['details'] = details
        
        return recommendation
    
    def _get_fertilizer_timing(self, growth_stage):
        """Get fertilizer application timing"""
        timing_map = {
            'Seedling': 'At planting or within 2 weeks of emergence',
            'Vegetative': 'Every 3-4 weeks during active growth',
            'Flowering': 'At flower initiation and early flowering',
            'Maturity': 'Final application before grain filling'
        }
        return timing_map.get(growth_stage, 'As needed based on soil tests')
    
    def _get_fertilizer_priority(self, growth_stage):
        """Get fertilizer priority level"""
        priority_map = {
            'Seedling': 'High',
            'Vegetative': 'High',
            'Flowering': 'Medium',
            'Maturity': 'Low'
        }
        return priority_map.get(growth_stage, 'Medium')
    
    def generate_weekly_schedule(self, crop_type, growth_stage):
        """Generate a weekly task schedule"""
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        schedule = {day: [] for day in days}
        
        # Base tasks by growth stage
        stage_tasks = {
            'Seedling': [
                'Check soil moisture and irrigate if needed',
                'Scout for emerging pests and diseases',
                'Monitor germination rates',
                'Check for weed emergence',
                'Record growth measurements'
            ],
            'Vegetative': [
                'Deep watering if needed',
                'Side-dress fertilizer application',
                'Comprehensive pest scouting',
                'Weed control activities',
                'Canopy management',
                'Soil cultivation if needed'
            ],
            'Flowering': [
                'Monitor soil moisture daily',
                'Check for flower damage or disease',
                'Pollinator-friendly pest management',
                'Nutrient deficiency assessment',
                'Weather monitoring for harvest planning'
            ],
            'Maturity': [
                'Daily maturity assessment',
                'Grain moisture testing',
                'Harvest equipment preparation',
                'Weather forecast monitoring',
                'Storage facility preparation',
                'Harvest scheduling'
            ]
        }
        
        tasks = stage_tasks.get(growth_stage, stage_tasks['Vegetative'])
        
        # Distribute tasks across the week
        for i, task in enumerate(tasks):
            day_index = i % len(days)
            schedule[days[day_index]].append(task)
        
        # Add crop-specific tasks
        if crop_type == 'Rice' and growth_stage in ['Seedling', 'Vegetative']:
            schedule['Monday'].append('Check water level in paddy fields')
            schedule['Friday'].append('Monitor water quality and algae growth')
        
        return schedule
