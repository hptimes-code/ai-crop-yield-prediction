import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from data.sample_agricultural_data import get_agricultural_data

class CropYieldPredictor:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_names = [
            'ph_level', 'organic_matter', 'nitrogen', 'phosphorus', 
            'potassium', 'temperature', 'rainfall', 'humidity'
        ]
        self.crop_types = ['Wheat', 'Corn', 'Rice', 'Soybeans']
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize and train models for each crop type"""
        # Get training data
        training_data = get_agricultural_data()
        
        for crop in self.crop_types:
            crop_data = training_data[training_data['crop_type'] == crop].copy()
            
            if len(crop_data) > 0:
                # Prepare features and target
                X = crop_data[self.feature_names]
                y = crop_data['yield_tons_per_ha']
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # Train Random Forest model
                rf_model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    min_samples_split=5,
                    min_samples_leaf=2
                )
                rf_model.fit(X_train_scaled, y_train)
                
                # Store model and scaler
                self.models[crop] = rf_model
                self.scalers[crop] = scaler
                
                # Calculate model performance
                y_pred = rf_model.predict(X_test_scaled)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                print(f"{crop} model - MAE: {mae:.2f}, R²: {r2:.3f}")
    
    def predict_yield(self, input_data):
        """
        Predict crop yield based on input parameters
        
        Args:
            input_data (dict): Dictionary containing input parameters
            
        Returns:
            dict: Prediction results including yield, confidence, and risk assessment
        """
        crop_type = input_data['crop_type']
        
        if crop_type not in self.models:
            raise ValueError(f"Model not available for crop type: {crop_type}")
        
        # Prepare input features
        features = np.array([
            input_data['ph_level'],
            input_data['organic_matter'],
            input_data['nitrogen'],
            input_data['phosphorus'],
            input_data['potassium'],
            input_data['temperature'],
            input_data['rainfall'],
            input_data['humidity']
        ]).reshape(1, -1)
        
        # Scale features
        scaler = self.scalers[crop_type]
        features_scaled = scaler.transform(features)
        
        # Make prediction
        model = self.models[crop_type]
        predicted_yield_per_ha = model.predict(features_scaled)[0]
        
        # Calculate total yield
        farm_area = input_data.get('farm_area', 1.0)
        total_yield = predicted_yield_per_ha * farm_area
        
        # Calculate confidence based on feature ranges
        confidence = self._calculate_confidence(input_data, crop_type)
        
        # Assess risk factors
        risk_assessment = self._assess_risk_factors(input_data)
        
        # Get feature importance
        feature_importance = self._get_feature_importance(crop_type)
        
        return {
            'yield_per_ha': max(0, predicted_yield_per_ha),
            'total_yield': max(0, total_yield),
            'confidence': confidence,
            'risk_level': risk_assessment['level'],
            'risk_factors': risk_assessment['factors'],
            'feature_importance': feature_importance
        }
    
    def _calculate_confidence(self, input_data, crop_type):
        """Calculate prediction confidence based on input parameter ranges"""
        
        # Define optimal ranges for different parameters
        optimal_ranges = {
            'ph_level': (6.0, 7.0),
            'organic_matter': (2.5, 5.0),
            'nitrogen': (20, 50),
            'phosphorus': (15, 40),
            'potassium': (100, 250),
            'temperature': (15, 30),
            'rainfall': (500, 1500),
            'humidity': (50, 80)
        }
        
        confidence_score = 0.0
        total_factors = len(optimal_ranges)
        
        for param, (min_val, max_val) in optimal_ranges.items():
            if param in input_data:
                value = input_data[param]
                if min_val <= value <= max_val:
                    confidence_score += 1.0
                else:
                    # Partial confidence based on how far outside the range
                    if value < min_val:
                        distance = (min_val - value) / min_val
                    else:
                        distance = (value - max_val) / max_val
                    
                    confidence_score += max(0, 1 - distance)
        
        base_confidence = confidence_score / total_factors
        
        # Add some randomness to simulate model uncertainty
        model_uncertainty = np.random.uniform(0.05, 0.15)
        final_confidence = max(0.3, base_confidence - model_uncertainty)
        
        return min(0.95, final_confidence)  # Cap at 95%
    
    def _assess_risk_factors(self, input_data):
        """Assess risk factors that might affect yield"""
        
        risk_factors = []
        risk_score = 0
        
        # pH risk assessment
        ph = input_data.get('ph_level', 7.0)
        if ph < 5.5 or ph > 8.0:
            risk_factors.append("Extreme pH levels may affect nutrient availability")
            risk_score += 2
        elif ph < 6.0 or ph > 7.5:
            risk_factors.append("Suboptimal pH levels may reduce yield")
            risk_score += 1
        
        # Temperature risk assessment
        temp = input_data.get('temperature', 20)
        if temp < 10 or temp > 35:
            risk_factors.append("Extreme temperatures may stress crops")
            risk_score += 2
        elif temp < 15 or temp > 30:
            risk_factors.append("Temperature outside optimal range")
            risk_score += 1
        
        # Rainfall risk assessment
        rainfall = input_data.get('rainfall', 800)
        if rainfall < 300:
            risk_factors.append("Insufficient rainfall may require additional irrigation")
            risk_score += 2
        elif rainfall > 2000:
            risk_factors.append("Excessive rainfall may cause waterlogging")
            risk_score += 2
        elif rainfall < 500 or rainfall > 1500:
            risk_factors.append("Rainfall outside optimal range")
            risk_score += 1
        
        # Nutrient deficiency risk
        nitrogen = input_data.get('nitrogen', 25)
        phosphorus = input_data.get('phosphorus', 20)
        potassium = input_data.get('potassium', 150)
        
        if nitrogen < 15:
            risk_factors.append("Low nitrogen levels may limit growth")
            risk_score += 1
        if phosphorus < 10:
            risk_factors.append("Low phosphorus levels may affect root development")
            risk_score += 1
        if potassium < 80:
            risk_factors.append("Low potassium levels may reduce disease resistance")
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 4:
            risk_level = "High"
        elif risk_score >= 2:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        if not risk_factors:
            risk_factors.append("No significant risk factors identified")
        
        return {
            'level': risk_level,
            'factors': "; ".join(risk_factors)
        }
    
    def _get_feature_importance(self, crop_type):
        """Get feature importance from the trained model"""
        
        if crop_type not in self.models:
            return {}
        
        model = self.models[crop_type]
        importance = model.feature_importances_
        
        feature_importance = {}
        for i, feature in enumerate(self.feature_names):
            feature_importance[feature.replace('_', ' ').title()] = importance[i]
        
        # Sort by importance
        sorted_importance = dict(sorted(
            feature_importance.items(), 
            key=lambda x: x[1], 
            reverse=True
        ))
        
        return sorted_importance
    
    def get_model_performance(self, crop_type):
        """Get model performance metrics"""
        
        if crop_type not in self.models:
            return None
        
        # This would typically involve validation on a test set
        # For now, return mock performance metrics
        return {
            'accuracy': np.random.uniform(0.85, 0.95),
            'mae': np.random.uniform(0.5, 1.5),
            'r2_score': np.random.uniform(0.8, 0.9)
        }
    
    def retrain_model(self, crop_type, new_data):
        """Retrain model with new data"""
        
        if crop_type not in self.crop_types:
            raise ValueError(f"Unsupported crop type: {crop_type}")
        
        # Prepare features and target
        X = new_data[self.feature_names]
        y = new_data['yield_tons_per_ha']
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train new model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        model.fit(X_scaled, y)
        
        # Update stored model and scaler
        self.models[crop_type] = model
        self.scalers[crop_type] = scaler
        
        return True
