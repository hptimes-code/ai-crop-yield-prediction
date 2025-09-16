# AI Crop Yield Prediction Platform

## Overview

This is an AI-powered agricultural platform built with Streamlit that provides crop yield predictions, weather analysis, soil health assessment, and farming recommendations. The platform uses machine learning models to predict crop yields based on environmental factors and provides actionable insights to help farmers optimize their agricultural productivity. It features multilingual support for global accessibility and integrates real-time weather data to deliver comprehensive agricultural intelligence.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with interactive dashboards
- **Visualization**: Plotly for charts and graphs (Express and Graph Objects)
- **Navigation**: streamlit-option-menu for multi-page navigation
- **UI Components**: Wide layout configuration with sidebar navigation and multilingual interface

### Machine Learning Architecture
- **Model Type**: Ensemble approach using Random Forest and Linear Regression
- **Training Data**: Synthetic agricultural dataset with realistic correlations
- **Features**: 8 key parameters (pH, organic matter, nitrogen, phosphorus, potassium, temperature, rainfall, humidity)
- **Crop Support**: Specialized models for Wheat, Corn, Rice, and Soybeans
- **Preprocessing**: StandardScaler for feature normalization and LabelEncoder for categorical data

### Data Processing Pipeline
- **Soil Analysis**: Comprehensive soil health assessment with crop-specific optimal ranges
- **Weather Integration**: Real-time weather data processing and historical trend analysis
- **Recommendation Engine**: Rule-based system providing fertilizer schedules, pest management, and optimal growing conditions
- **Data Validation**: Robust input validation and error handling throughout the pipeline

### Service Architecture
- **Weather Service**: OpenWeatherMap API integration for current conditions and forecasts
- **Recommendation Engine**: Knowledge-based system with crop-specific growth stage recommendations
- **Data Processor**: Centralized data validation and analysis utilities
- **Multilingual Support**: Translation service supporting English, Spanish, French, Hindi, and Chinese

### Model Training and Deployment
- **Training Strategy**: Per-crop model training with train/test split validation
- **Performance Metrics**: Mean Absolute Error (MAE) and R² score tracking
- **Model Persistence**: Joblib for model serialization and caching
- **Resource Management**: Streamlit cache_resource decorator for service initialization

## External Dependencies

### APIs and Services
- **OpenWeatherMap API**: Real-time weather data and forecasting
- **Environment Variables**: API key management through environment configuration

### Python Libraries
- **Core Framework**: Streamlit for web application development
- **Data Science**: pandas, numpy for data manipulation and analysis
- **Machine Learning**: scikit-learn for model training and preprocessing
- **Visualization**: plotly (express and graph_objects) for interactive charts
- **UI Enhancement**: streamlit-option-menu for navigation components
- **Model Persistence**: joblib for saving and loading trained models
- **HTTP Requests**: requests library for external API communication

### Data Sources
- **Training Data**: Synthetic agricultural dataset generator with realistic crop parameters
- **Weather Data**: Live weather feeds from OpenWeatherMap
- **Crop Knowledge Base**: Built-in agricultural expertise for recommendations

### File System Dependencies
- **Model Storage**: Local file system for persisting trained models
- **Configuration Management**: Environment-based configuration for API keys
- **Data Caching**: Streamlit's caching system for performance optimization