import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class DataProcessor:
    def __init__(self):
        self.soil_optimal_ranges = {
            'ph': (6.0, 7.0),
            'organic_matter': (2.5, 5.0),
            'nitrogen': (20, 50),
            'phosphorus': (15, 40),
            'potassium': (100, 250),
            'calcium': (1000, 2500),
            'magnesium': (75, 200)
        }
        
        self.crop_soil_preferences = {
            'Wheat': {
                'ph': (6.0, 7.0),
                'nitrogen': (25, 45),
                'phosphorus': (20, 40),
                'potassium': (120, 200)
            },
            'Corn': {
                'ph': (6.0, 6.8),
                'nitrogen': (30, 60),
                'phosphorus': (25, 45),
                'potassium': (150, 250)
            },
            'Rice': {
                'ph': (5.5, 6.5),
                'nitrogen': (20, 40),
                'phosphorus': (15, 30),
                'potassium': (100, 180)
            },
            'Soybeans': {
                'ph': (6.0, 7.0),
                'nitrogen': (15, 30),  # Lower due to nitrogen fixation
                'phosphorus': (20, 35),
                'potassium': (120, 220)
            }
        }
    
    def analyze_soil_health(self, soil_data):
        """
        Analyze soil health based on test results
        
        Args:
            soil_data (dict): Soil test results
            
        Returns:
            dict: Comprehensive soil health analysis
        """
        
        analysis = {
            'overall_score': 0,
            'rating': '',
            'parameter_scores': {},
            'deficiencies': [],
            'excesses': [],
            'recommendations': {
                'immediate': [],
                'short_term': [],
                'long_term': []
            }
        }
        
        total_score = 0
        parameter_count = 0
        
        # Analyze each soil parameter
        for parameter, value in soil_data.items():
            if parameter in self.soil_optimal_ranges:
                min_optimal, max_optimal = self.soil_optimal_ranges[parameter]
                
                # Calculate parameter score (0-100)
                if min_optimal <= value <= max_optimal:
                    param_score = 100
                elif value < min_optimal:
                    # Below optimal range
                    deficit = min_optimal - value
                    param_score = max(0, 100 - (deficit / min_optimal * 100))
                    analysis['deficiencies'].append({
                        'parameter': parameter,
                        'current': value,
                        'optimal_min': min_optimal,
                        'severity': 'High' if param_score < 50 else 'Medium'
                    })
                else:
                    # Above optimal range
                    excess = value - max_optimal
                    param_score = max(0, 100 - (excess / max_optimal * 100))
                    analysis['excesses'].append({
                        'parameter': parameter,
                        'current': value,
                        'optimal_max': max_optimal,
                        'severity': 'High' if param_score < 50 else 'Medium'
                    })
                
                analysis['parameter_scores'][parameter] = param_score
                total_score += param_score
                parameter_count += 1
        
        # Calculate overall score
        if parameter_count > 0:
            analysis['overall_score'] = round(total_score / parameter_count)
        
        # Determine rating
        if analysis['overall_score'] >= 85:
            analysis['rating'] = 'Excellent'
        elif analysis['overall_score'] >= 75:
            analysis['rating'] = 'Good'
        elif analysis['overall_score'] >= 60:
            analysis['rating'] = 'Fair'
        elif analysis['overall_score'] >= 40:
            analysis['rating'] = 'Poor'
        else:
            analysis['rating'] = 'Very Poor'
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_soil_recommendations(analysis, soil_data)
        
        return analysis
    
    def _generate_soil_recommendations(self, analysis, soil_data):
        """Generate soil improvement recommendations"""
        
        recommendations = {
            'immediate': [],
            'short_term': [],
            'long_term': []
        }
        
        # pH recommendations
        ph = soil_data.get('ph', 7.0)
        if ph < 6.0:
            recommendations['immediate'].append(f'Apply lime to raise pH from {ph} to 6.0-7.0 range')
            recommendations['short_term'].append('Retest pH after 3-4 months to monitor lime effectiveness')
        elif ph > 8.0:
            recommendations['immediate'].append(f'Apply sulfur or organic matter to lower pH from {ph}')
            recommendations['short_term'].append('Consider using acidifying fertilizers')
        
        # Organic matter recommendations
        om = soil_data.get('organic_matter', 3.0)
        if om < 2.5:
            recommendations['immediate'].append('Add compost or well-rotted manure to increase organic matter')
            recommendations['long_term'].append('Implement cover cropping to build long-term organic matter')
        elif om > 6.0:
            recommendations['short_term'].append('Monitor drainage as high organic matter can retain excess water')
        
        # Nutrient recommendations
        nutrients = ['nitrogen', 'phosphorus', 'potassium']
        for nutrient in nutrients:
            value = soil_data.get(nutrient, 0)
            min_optimal, max_optimal = self.soil_optimal_ranges.get(nutrient, (0, 100))
            
            if value < min_optimal:
                deficiency_level = ((min_optimal - value) / min_optimal) * 100
                if deficiency_level > 50:
                    recommendations['immediate'].append(f'Apply {nutrient} fertilizer - severe deficiency detected')
                else:
                    recommendations['short_term'].append(f'Increase {nutrient} levels through targeted fertilization')
            elif value > max_optimal * 1.5:
                recommendations['immediate'].append(f'Reduce {nutrient} applications - excess levels detected')
        
        # Calcium and Magnesium
        calcium = soil_data.get('calcium', 1200)
        magnesium = soil_data.get('magnesium', 120)
        
        if calcium < 1000:
            recommendations['short_term'].append('Apply gypsum or lime to increase calcium levels')
        
        if magnesium < 75:
            recommendations['short_term'].append('Apply Epsom salt or dolomitic lime for magnesium')
        
        # Ca:Mg ratio check
        if calcium > 0 and magnesium > 0:
            ca_mg_ratio = calcium / magnesium
            if ca_mg_ratio < 3:
                recommendations['short_term'].append('Calcium to magnesium ratio is low - consider calcium applications')
            elif ca_mg_ratio > 10:
                recommendations['short_term'].append('Calcium to magnesium ratio is high - consider magnesium applications')
        
        # General recommendations based on overall score
        if analysis['overall_score'] < 60:
            recommendations['immediate'].append('Conduct comprehensive soil remediation program')
            recommendations['long_term'].append('Implement regular soil testing schedule (every 2-3 years)')
        
        recommendations['long_term'].extend([
            'Maintain crop rotation to preserve soil health',
            'Consider precision agriculture techniques for optimal nutrient management',
            'Implement sustainable farming practices to build long-term soil fertility'
        ])
        
        return recommendations
    
    def analyze_crop_suitability(self, soil_data, crop_type):
        """
        Analyze how suitable the soil is for a specific crop
        
        Args:
            soil_data (dict): Soil test results
            crop_type (str): Type of crop to analyze
            
        Returns:
            dict: Crop suitability analysis
        """
        
        if crop_type not in self.crop_soil_preferences:
            return {'error': f'Crop type {crop_type} not supported'}
        
        crop_preferences = self.crop_soil_preferences[crop_type]
        
        suitability = {
            'crop': crop_type,
            'overall_suitability': 0,
            'parameter_suitability': {},
            'limiting_factors': [],
            'recommendations': []
        }
        
        total_score = 0
        parameter_count = 0
        
        for parameter, (min_pref, max_pref) in crop_preferences.items():
            if parameter in soil_data:
                value = soil_data[parameter]
                
                # Calculate suitability score for this parameter
                if min_pref <= value <= max_pref:
                    param_score = 100
                elif value < min_pref:
                    param_score = max(0, 100 - ((min_pref - value) / min_pref * 100))
                else:
                    param_score = max(0, 100 - ((value - max_pref) / max_pref * 100))
                
                suitability['parameter_suitability'][parameter] = {
                    'score': param_score,
                    'current': value,
                    'optimal_range': (min_pref, max_pref),
                    'status': 'Optimal' if param_score == 100 else 'Suboptimal' if param_score > 70 else 'Poor'
                }
                
                if param_score < 70:
                    suitability['limiting_factors'].append({
                        'parameter': parameter,
                        'current': value,
                        'needed_range': (min_pref, max_pref),
                        'score': param_score
                    })
                
                total_score += param_score
                parameter_count += 1
        
        if parameter_count > 0:
            suitability['overall_suitability'] = round(total_score / parameter_count)
        
        # Generate crop-specific recommendations
        suitability['recommendations'] = self._generate_crop_specific_recommendations(
            suitability, crop_type
        )
        
        return suitability
    
    def _generate_crop_specific_recommendations(self, suitability, crop_type):
        """Generate crop-specific soil management recommendations"""
        
        recommendations = []
        
        overall_score = suitability['overall_suitability']
        limiting_factors = suitability['limiting_factors']
        
        if overall_score >= 85:
            recommendations.append(f'Soil conditions are excellent for {crop_type} production')
            recommendations.append('Maintain current soil management practices')
        elif overall_score >= 70:
            recommendations.append(f'Soil conditions are good for {crop_type} with minor adjustments needed')
        else:
            recommendations.append(f'Soil requires significant improvements for optimal {crop_type} production')
        
        # Address limiting factors
        for factor in limiting_factors:
            parameter = factor['parameter']
            current = factor['current']
            needed_min, needed_max = factor['needed_range']
            
            if parameter == 'ph':
                if current < needed_min:
                    recommendations.append(f'Apply lime to raise pH to {needed_min}-{needed_max} range for {crop_type}')
                else:
                    recommendations.append(f'Apply sulfur to lower pH to {needed_min}-{needed_max} range for {crop_type}')
            
            elif parameter == 'nitrogen':
                if current < needed_min:
                    recommendations.append(f'Apply nitrogen fertilizer to reach {needed_min}-{needed_max} ppm for {crop_type}')
                else:
                    recommendations.append(f'Reduce nitrogen applications - current levels exceed {crop_type} requirements')
            
            elif parameter == 'phosphorus':
                if current < needed_min:
                    recommendations.append(f'Apply phosphorus fertilizer to reach {needed_min}-{needed_max} ppm for {crop_type}')
                else:
                    recommendations.append(f'Reduce phosphorus applications for {crop_type}')
            
            elif parameter == 'potassium':
                if current < needed_min:
                    recommendations.append(f'Apply potassium fertilizer to reach {needed_min}-{needed_max} ppm for {crop_type}')
                else:
                    recommendations.append(f'Reduce potassium applications for {crop_type}')
        
        # Crop-specific advice
        if crop_type == 'Rice':
            recommendations.append('Ensure proper water management for paddy conditions')
            recommendations.append('Monitor for anaerobic soil conditions')
        elif crop_type == 'Soybeans':
            recommendations.append('Consider inoculation with Rhizobia bacteria for nitrogen fixation')
            recommendations.append('Monitor calcium levels for pod development')
        elif crop_type == 'Corn':
            recommendations.append('Ensure adequate drainage for corn production')
            recommendations.append('Plan for high nitrogen requirements during vegetative growth')
        elif crop_type == 'Wheat':
            recommendations.append('Monitor sulfur levels for protein development')
            recommendations.append('Ensure good soil structure for root development')
        
        return recommendations
    
    def generate_fertilizer_plan(self, soil_data, crop_type, target_yield):
        """
        Generate a detailed fertilizer application plan
        
        Args:
            soil_data (dict): Current soil test results
            crop_type (str): Type of crop
            target_yield (float): Target yield in tons per hectare
            
        Returns:
            dict: Detailed fertilizer application plan
        """
        
        if crop_type not in self.crop_soil_preferences:
            return {'error': f'Crop type {crop_type} not supported'}
        
        # Base nutrient requirements per ton of yield
        nutrient_requirements = {
            'Wheat': {'N': 25, 'P2O5': 12, 'K2O': 20},
            'Corn': {'N': 22, 'P2O5': 10, 'K2O': 18},
            'Rice': {'N': 20, 'P2O5': 8, 'K2O': 15},
            'Soybeans': {'N': 5, 'P2O5': 8, 'K2O': 12}  # Lower N due to fixation
        }
        
        if crop_type not in nutrient_requirements:
            crop_type = 'Wheat'  # Default
        
        crop_needs = nutrient_requirements[crop_type]
        
        # Calculate total nutrient needs
        total_n_needed = crop_needs['N'] * target_yield
        total_p_needed = crop_needs['P2O5'] * target_yield
        total_k_needed = crop_needs['K2O'] * target_yield
        
        # Calculate what's available in soil
        soil_n = soil_data.get('nitrogen', 25)
        soil_p = soil_data.get('phosphorus', 20) * 2.29  # Convert P to P2O5
        soil_k = soil_data.get('potassium', 150) * 1.2   # Convert K to K2O
        
        # Calculate fertilizer needs
        n_fertilizer_needed = max(0, total_n_needed - (soil_n * 0.5))  # 50% N availability
        p_fertilizer_needed = max(0, total_p_needed - (soil_p * 0.3))  # 30% P availability
        k_fertilizer_needed = max(0, total_k_needed - (soil_k * 0.8))  # 80% K availability
        
        plan = {
            'crop_type': crop_type,
            'target_yield': target_yield,
            'total_nutrients_needed': {
                'nitrogen': total_n_needed,
                'phosphorus': total_p_needed,
                'potassium': total_k_needed
            },
            'soil_available': {
                'nitrogen': soil_n,
                'phosphorus': soil_p,
                'potassium': soil_k
            },
            'fertilizer_needed': {
                'nitrogen': round(n_fertilizer_needed, 1),
                'phosphorus': round(p_fertilizer_needed, 1),
                'potassium': round(k_fertilizer_needed, 1)
            },
            'application_schedule': self._create_application_schedule(
                crop_type, n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed
            ),
            'estimated_cost': self._estimate_fertilizer_cost(
                n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed
            )
        }
        
        return plan
    
    def _create_application_schedule(self, crop_type, n_needed, p_needed, k_needed):
        """Create fertilizer application schedule by growth stage"""
        
        schedule = {
            'pre_plant': {'N': 0, 'P2O5': 0, 'K2O': 0, 'timing': 'Before planting or at planting'},
            'early_growth': {'N': 0, 'P2O5': 0, 'K2O': 0, 'timing': '2-4 weeks after emergence'},
            'mid_growth': {'N': 0, 'P2O5': 0, 'K2O': 0, 'timing': '6-8 weeks after emergence'},
            'late_growth': {'N': 0, 'P2O5': 0, 'K2O': 0, 'timing': 'Before reproductive stage'}
        }
        
        # Distribution patterns by crop type
        if crop_type == 'Wheat':
            schedule['pre_plant']['N'] = n_needed * 0.3
            schedule['pre_plant']['P2O5'] = p_needed * 1.0  # All P at planting
            schedule['pre_plant']['K2O'] = k_needed * 0.5
            
            schedule['early_growth']['N'] = n_needed * 0.4
            schedule['early_growth']['K2O'] = k_needed * 0.3
            
            schedule['mid_growth']['N'] = n_needed * 0.3
            schedule['mid_growth']['K2O'] = k_needed * 0.2
        
        elif crop_type == 'Corn':
            schedule['pre_plant']['N'] = n_needed * 0.2
            schedule['pre_plant']['P2O5'] = p_needed * 1.0
            schedule['pre_plant']['K2O'] = k_needed * 0.4
            
            schedule['early_growth']['N'] = n_needed * 0.3
            schedule['early_growth']['K2O'] = k_needed * 0.3
            
            schedule['mid_growth']['N'] = n_needed * 0.5  # Side-dress application
            schedule['mid_growth']['K2O'] = k_needed * 0.3
        
        elif crop_type == 'Rice':
            schedule['pre_plant']['N'] = n_needed * 0.4
            schedule['pre_plant']['P2O5'] = p_needed * 1.0
            schedule['pre_plant']['K2O'] = k_needed * 0.5
            
            schedule['early_growth']['N'] = n_needed * 0.3
            schedule['mid_growth']['N'] = n_needed * 0.3
            schedule['mid_growth']['K2O'] = k_needed * 0.5
        
        elif crop_type == 'Soybeans':
            schedule['pre_plant']['N'] = n_needed * 0.5  # Lower N needs
            schedule['pre_plant']['P2O5'] = p_needed * 1.0
            schedule['pre_plant']['K2O'] = k_needed * 0.6
            
            schedule['early_growth']['N'] = n_needed * 0.3
            schedule['early_growth']['K2O'] = k_needed * 0.2
            
            schedule['mid_growth']['N'] = n_needed * 0.2
            schedule['mid_growth']['K2O'] = k_needed * 0.2
        
        # Round all values
        for stage in schedule.values():
            for nutrient in ['N', 'P2O5', 'K2O']:
                stage[nutrient] = round(stage[nutrient], 1)
        
        return schedule
    
    def _estimate_fertilizer_cost(self, n_needed, p_needed, k_needed):
        """Estimate fertilizer costs based on current market prices"""
        
        # Approximate prices per kg (USD) - these would be updated from market data
        prices = {
            'nitrogen': 1.20,    # Urea
            'phosphorus': 1.50,  # DAP
            'potassium': 0.80    # MOP
        }
        
        n_cost = n_needed * prices['nitrogen']
        p_cost = p_needed * prices['phosphorus']
        k_cost = k_needed * prices['potassium']
        
        return {
            'nitrogen_cost': round(n_cost, 2),
            'phosphorus_cost': round(p_cost, 2),
            'potassium_cost': round(k_cost, 2),
            'total_cost': round(n_cost + p_cost + k_cost, 2),
            'cost_per_hectare': round(n_cost + p_cost + k_cost, 2),
            'currency': 'USD'
        }
