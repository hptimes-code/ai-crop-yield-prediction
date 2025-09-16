class MultilingualSupport:
    def __init__(self):
        self.translations = {
            'en': {
                # Page titles and navigation
                'title': 'AI Crop Yield Prediction Platform',
                'subtitle': 'Data-driven recommendations for optimizing agricultural productivity',
                'dashboard': 'Dashboard',
                'prediction': 'Yield Prediction',
                'weather': 'Weather Data',
                'soil_analysis': 'Soil Analysis',
                'recommendations': 'Recommendations',
                
                # Dashboard content
                'total_crops': 'Supported Crops',
                'regions': 'Coverage',
                'accuracy': 'Model Accuracy',
                'farmers_helped': 'Farmers Served',
                'yield_trends': 'Yield Trends',
                'historical_yield_trends': 'Historical Yield Trends by Crop',
                'regional_performance': 'Regional Performance',
                'avg_yield_by_region': 'Average Yield by Region',
                'crop_distribution': 'Crop Distribution',
                'crop_area_distribution': 'Crop Area Distribution',
                
                # Common terms
                'yield': 'Yield',
                'date': 'Date',
                'region': 'Region',
                'city': 'City',
                'location': 'Location',
                'temperature': 'Temperature',
                'humidity': 'Humidity',
                'pressure': 'Pressure',
                'conditions': 'Conditions',
                'rainfall': 'Rainfall',
                'nutrients': 'Nutrients',
                'levels': 'Levels',
                'factors': 'Factors',
                'importance': 'Importance',
                'value': 'Value',
                'analysis': 'Analysis',
                'assessment': 'Assessment',
                'impact': 'Impact',
                'recommendation': 'Recommendation',
                'priority': 'Priority',
                'action': 'Action',
                'timing': 'Timing',
                'reason': 'Reason',
                
                # Prediction page
                'yield_prediction': 'Crop Yield Prediction',
                'input_parameters': 'Input Parameters',
                'select_crop': 'Select Crop Type',
                'farm_area': 'Farm Area',
                'soil_parameters': 'Soil Parameters',
                'ph_level': 'pH Level',
                'organic_matter': 'Organic Matter',
                'nitrogen': 'Nitrogen',
                'phosphorus': 'Phosphorus',
                'potassium': 'Potassium',
                'weather_data': 'Weather Data',
                'use_current_weather': 'Use Current Weather Data',
                'avg_temperature': 'Average Temperature',
                'annual_rainfall': 'Annual Rainfall',
                'avg_humidity': 'Average Humidity',
                'predict_yield': 'Predict Yield',
                'analyzing': 'Analyzing data',
                'prediction_results': 'Prediction Results',
                'predicted_yield': 'Predicted Yield',
                'total_yield': 'Total Yield',
                'confidence': 'Confidence',
                'risk_assessment': 'Risk Assessment',
                'risk_level': 'Risk Level',
                'factor_importance': 'Factor Importance',
                'factors_affecting_yield': 'Factors Affecting Yield',
                'prediction_error': 'Prediction Error',
                'region_required': 'Please enter a region/city',
                
                # Weather page
                'weather_monitoring': 'Weather Monitoring',
                'enter_location': 'Enter Location',
                'get_weather': 'Get Weather Data',
                'fetching_weather': 'Fetching weather data',
                'weather_data_retrieved': 'Weather data retrieved successfully',
                'current_conditions': 'Current Conditions',
                'agricultural_impact': 'Agricultural Impact',
                'forecast_trend': 'Forecast Trends',
                '7_day_forecast': '7-Day Temperature and Humidity Forecast',
                'weather_data_error': 'Unable to retrieve weather data. Please check the location.',
                'weather_data_unavailable': 'Current weather data unavailable, using default values',
                
                # Soil analysis page
                'soil_test_results': 'Soil Test Results',
                'calcium': 'Calcium',
                'magnesium': 'Magnesium',
                'analyze_soil': 'Analyze Soil Health',
                'analysis_results': 'Analysis Results',
                'soil_health_score': 'Soil Health Score',
                'overall_assessment': 'Overall Assessment',
                'nutrient_levels': 'Nutrient Levels',
                'current_vs_optimal': 'Current vs Optimal Levels',
                
                # Recommendations page
                'smart_recommendations': 'Smart Farming Recommendations',
                'current_farm_status': 'Current Farm Status',
                'current_crop': 'Current Crop',
                'growth_stage': 'Growth Stage',
                'generate_recommendations': 'Generate Recommendations',
                'generating_recommendations': 'Generating recommendations',
                'irrigation': 'irrigation',
                'fertilization': 'fertilization',
                'pest_control': 'pest control',
                'harvesting': 'harvesting',
                'weekly_schedule': 'Weekly Task Schedule',
                'more_details': 'More Details',
                'fill_all_fields': 'Please fill all required fields',
                'no_tasks_scheduled': 'No specific tasks scheduled for this day',
                
                # Help text
                'supported_crops_help': 'Currently supporting 4 major crop types',
                'global_coverage_help': 'Weather data available worldwide',
                'model_accuracy_help': 'Average prediction accuracy across all crops',
                'farmers_count_help': 'Number of farmers using the platform',
                'crop_selection_help': 'Select the crop you want to analyze',
                'region_help': 'Enter your farm location for weather data',
                'farm_area_help': 'Total cultivated area in hectares',
                'ph_help': 'Soil pH affects nutrient availability (6.0-7.0 optimal)',
                'organic_matter_help': 'Percentage of organic matter in soil',
                'nitrogen_help': 'Available nitrogen in parts per million',
                'phosphorus_help': 'Available phosphorus in parts per million',
                'potassium_help': 'Available potassium in parts per million',
                'current_weather_help': 'Use real-time weather data for prediction',
                'yield_per_ha_help': 'Expected yield per hectare',
                'total_yield_help': 'Total expected yield for your farm area',
                'confidence_help': 'Model confidence in prediction accuracy',
                'location_help': 'Enter city name or coordinates',
                'health_score_help': 'Overall soil health rating (0-100)',
                'growth_stage_help': 'Current development stage of your crop'
            },
            
            'es': {
                # Page titles and navigation
                'title': 'Plataforma de Predicción de Rendimiento de Cultivos con IA',
                'subtitle': 'Recomendaciones basadas en datos para optimizar la productividad agrícola',
                'dashboard': 'Panel de Control',
                'prediction': 'Predicción de Rendimiento',
                'weather': 'Datos Meteorológicos',
                'soil_analysis': 'Análisis de Suelo',
                'recommendations': 'Recomendaciones',
                
                # Dashboard content
                'total_crops': 'Cultivos Compatibles',
                'regions': 'Cobertura',
                'accuracy': 'Precisión del Modelo',
                'farmers_helped': 'Agricultores Atendidos',
                'yield_trends': 'Tendencias de Rendimiento',
                'historical_yield_trends': 'Tendencias Históricas de Rendimiento por Cultivo',
                'regional_performance': 'Rendimiento Regional',
                'avg_yield_by_region': 'Rendimiento Promedio por Región',
                'crop_distribution': 'Distribución de Cultivos',
                'crop_area_distribution': 'Distribución del Área de Cultivos',
                
                # Common terms
                'yield': 'Rendimiento',
                'date': 'Fecha',
                'region': 'Región',
                'city': 'Ciudad',
                'location': 'Ubicación',
                'temperature': 'Temperatura',
                'humidity': 'Humedad',
                'pressure': 'Presión',
                'conditions': 'Condiciones',
                'rainfall': 'Precipitación',
                'nutrients': 'Nutrientes',
                'levels': 'Niveles',
                'factors': 'Factores',
                'importance': 'Importancia',
                'value': 'Valor',
                'analysis': 'Análisis',
                'assessment': 'Evaluación',
                'impact': 'Impacto',
                'recommendation': 'Recomendación',
                'priority': 'Prioridad',
                'action': 'Acción',
                'timing': 'Momento',
                'reason': 'Razón',
                
                # Help text
                'supported_crops_help': 'Actualmente compatible con 4 tipos principales de cultivos',
                'global_coverage_help': 'Datos meteorológicos disponibles en todo el mundo',
                'model_accuracy_help': 'Precisión promedio de predicción en todos los cultivos',
                'farmers_count_help': 'Número de agricultores que usan la plataforma'
            },
            
            'fr': {
                # Page titles and navigation
                'title': 'Plateforme de Prédiction de Rendement des Cultures par IA',
                'subtitle': 'Recommandations basées sur les données pour optimiser la productivité agricole',
                'dashboard': 'Tableau de Bord',
                'prediction': 'Prédiction de Rendement',
                'weather': 'Données Météo',
                'soil_analysis': 'Analyse du Sol',
                'recommendations': 'Recommandations',
                
                # Common terms
                'yield': 'Rendement',
                'date': 'Date',
                'region': 'Région',
                'city': 'Ville',
                'location': 'Emplacement',
                'temperature': 'Température',
                'humidity': 'Humidité',
                'pressure': 'Pression',
                'conditions': 'Conditions',
                'rainfall': 'Précipitations',
                'nutrients': 'Nutriments',
                'levels': 'Niveaux',
                'factors': 'Facteurs',
                'importance': 'Importance',
                'value': 'Valeur',
                'analysis': 'Analyse',
                'assessment': 'Évaluation',
                'impact': 'Impact',
                'recommendation': 'Recommandation',
                'priority': 'Priorité',
                'action': 'Action',
                'timing': 'Timing',
                'reason': 'Raison'
            },
            
            'hi': {
                # Page titles and navigation
                'title': 'AI फसल उत्पादन पूर्वानुमान प्लेटफॉर्म',
                'subtitle': 'कृषि उत्पादकता को अनुकूलित करने के लिए डेटा-संचालित सिफारिशें',
                'dashboard': 'डैशबोर्ड',
                'prediction': 'उत्पादन पूर्वानुमान',
                'weather': 'मौसम डेटा',
                'soil_analysis': 'मिट्टी विश्लेषण',
                'recommendations': 'सिफारिशें',
                
                # Common terms
                'yield': 'उत्पादन',
                'date': 'दिनांक',
                'region': 'क्षेत्र',
                'city': 'शहर',
                'location': 'स्थान',
                'temperature': 'तापमान',
                'humidity': 'नमी',
                'pressure': 'दबाव',
                'conditions': 'स्थितियां',
                'rainfall': 'वर्षा',
                'nutrients': 'पोषक तत्व',
                'levels': 'स्तर',
                'factors': 'कारक',
                'importance': 'महत्व',
                'value': 'मान',
                'analysis': 'विश्लेषण',
                'assessment': 'मूल्यांकन',
                'impact': 'प्रभाव',
                'recommendation': 'सिफारिश',
                'priority': 'प्राथमिकता',
                'action': 'कार्य',
                'timing': 'समय',
                'reason': 'कारण'
            },
            
            'zh': {
                # Page titles and navigation
                'title': 'AI作物产量预测平台',
                'subtitle': '基于数据驱动的农业生产力优化建议',
                'dashboard': '仪表板',
                'prediction': '产量预测',
                'weather': '天气数据',
                'soil_analysis': '土壤分析',
                'recommendations': '建议',
                
                # Common terms
                'yield': '产量',
                'date': '日期',
                'region': '地区',
                'city': '城市',
                'location': '位置',
                'temperature': '温度',
                'humidity': '湿度',
                'pressure': '压力',
                'conditions': '条件',
                'rainfall': '降雨量',
                'nutrients': '营养素',
                'levels': '水平',
                'factors': '因素',
                'importance': '重要性',
                'value': '值',
                'analysis': '分析',
                'assessment': '评估',
                'impact': '影响',
                'recommendation': '建议',
                'priority': '优先级',
                'action': '行动',
                'timing': '时间',
                'reason': '原因'
            }
        }
    
    def get_translations(self, language_code):
        """Get translations for specified language"""
        return self.translations.get(language_code, self.translations['en'])
    
    def get_supported_languages(self):
        """Get list of supported language codes"""
        return list(self.translations.keys())
    
    def add_translation(self, language_code, translations):
        """Add translations for a new language"""
        if language_code not in self.translations:
            self.translations[language_code] = {}
        
        self.translations[language_code].update(translations)
    
    def translate(self, key, language_code='en'):
        """Translate a specific key"""
        lang_dict = self.translations.get(language_code, self.translations['en'])
        return lang_dict.get(key, key)  # Return key if translation not found
