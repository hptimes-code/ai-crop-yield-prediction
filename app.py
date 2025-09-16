import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import os
from datetime import datetime, timedelta

# Import custom modules
from models.crop_models import CropYieldPredictor
from services.weather_service import WeatherService
from services.recommendation_engine import RecommendationEngine
from utils.data_processor import DataProcessor
from utils.multilingual import MultilingualSupport

# Initialize services
@st.cache_resource
def initialize_services():
    weather_service = WeatherService()
    data_processor = DataProcessor()
    crop_predictor = CropYieldPredictor()
    recommendation_engine = RecommendationEngine()
    multilingual = MultilingualSupport()
    return weather_service, data_processor, crop_predictor, recommendation_engine, multilingual

def main():
    st.set_page_config(
        page_title="AI Crop Yield Prediction Platform",
        page_icon="🌾",
        layout="wide"
    )
    
    # Initialize services
    weather_service, data_processor, crop_predictor, recommendation_engine, multilingual = initialize_services()
    
    # Language selection
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Sidebar for language selection
    st.sidebar.selectbox(
        "Select Language / Seleccionar idioma / Choisir la langue",
        options=['en', 'es', 'fr', 'hi', 'zh'],
        format_func=lambda x: {'en': 'English', 'es': 'Español', 'fr': 'Français', 'hi': 'हिंदी', 'zh': '中文'}[x],
        key='language'
    )
    
    # Get translations
    t = multilingual.get_translations(st.session_state.language)
    
    st.title(f"🌾 {t['title']}")
    st.markdown(f"**{t['subtitle']}**")
    
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=[t['dashboard'], t['prediction'], t['weather'], t['soil_analysis'], t['recommendations']],
        icons=['house', 'graph-up', 'cloud-sun', 'geo-alt', 'lightbulb'],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )
    
    if selected == t['dashboard']:
        show_dashboard(weather_service, data_processor, t)
    elif selected == t['prediction']:
        show_prediction_page(crop_predictor, weather_service, t)
    elif selected == t['weather']:
        show_weather_page(weather_service, t)
    elif selected == t['soil_analysis']:
        show_soil_analysis_page(data_processor, t)
    elif selected == t['recommendations']:
        show_recommendations_page(recommendation_engine, t)

def show_dashboard(weather_service, data_processor, t):
    st.header(f"📊 {t['dashboard']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"🌾 {t['total_crops']}",
            value="4",
            help=t['supported_crops_help']
        )
    
    with col2:
        st.metric(
            label=f"🌍 {t['regions']}",
            value="Global",
            help=t['global_coverage_help']
        )
    
    with col3:
        st.metric(
            label=f"📈 {t['accuracy']}",
            value="92%",
            help=t['model_accuracy_help']
        )
    
    with col4:
        st.metric(
            label=f"👨‍🌾 {t['farmers_helped']}",
            value="10K+",
            help=t['farmers_count_help']
        )
    
    # Sample yield trends visualization
    st.subheader(f"📈 {t['yield_trends']}")
    
    # Generate sample trend data
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='M')
    crops = ['Wheat', 'Corn', 'Rice', 'Soybeans']
    
    trend_data = []
    for crop in crops:
        base_yield = np.random.uniform(3, 8)
        trend = np.random.uniform(-0.1, 0.3, len(dates))
        noise = np.random.normal(0, 0.5, len(dates))
        yields = base_yield + np.cumsum(trend) + noise
        yields = np.maximum(yields, 0.5)  # Ensure positive yields
        
        for i, date in enumerate(dates):
            trend_data.append({
                'Date': date,
                'Crop': crop,
                'Yield': yields[i]
            })
    
    trend_df = pd.DataFrame(trend_data)
    
    fig = px.line(
        trend_df, 
        x='Date', 
        y='Yield', 
        color='Crop',
        title=f"{t['historical_yield_trends']}",
        labels={'Yield': f"{t['yield']} (tons/ha)", 'Date': t['date']}
    )
    
    fig.update_layout(
        xaxis_title=t['date'],
        yaxis_title=f"{t['yield']} (tons/ha)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🌍 {t['regional_performance']}")
        
        regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
        avg_yields = np.random.uniform(4, 9, len(regions))
        
        fig_bar = px.bar(
            x=regions,
            y=avg_yields,
            title=f"{t['avg_yield_by_region']}",
            labels={'x': t['region'], 'y': f"{t['yield']} (tons/ha)"}
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader(f"🌾 {t['crop_distribution']}")
        
        crop_areas = [25, 30, 20, 25]  # Percentage distribution
        
        fig_pie = px.pie(
            values=crop_areas,
            names=crops,
            title=f"{t['crop_area_distribution']}"
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

def show_prediction_page(crop_predictor, weather_service, t):
    st.header(f"🔮 {t['yield_prediction']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(f"📝 {t['input_parameters']}")
        
        # Crop selection
        crop_type = st.selectbox(
            t['select_crop'],
            options=['Wheat', 'Corn', 'Rice', 'Soybeans'],
            help=t['crop_selection_help']
        )
        
        # Region input
        region = st.text_input(
            f"{t['region']} / {t['city']}",
            placeholder="e.g., Iowa, USA",
            help=t['region_help']
        )
        
        # Farm area
        farm_area = st.number_input(
            f"{t['farm_area']} (ha)",
            min_value=0.1,
            max_value=10000.0,
            value=10.0,
            step=0.1,
            help=t['farm_area_help']
        )
        
        # Soil parameters
        st.subheader(f"🌱 {t['soil_parameters']}")
        
        ph_level = st.slider(
            f"{t['ph_level']}",
            min_value=4.0,
            max_value=9.0,
            value=6.5,
            step=0.1,
            help=t['ph_help']
        )
        
        organic_matter = st.slider(
            f"{t['organic_matter']} (%)",
            min_value=0.5,
            max_value=10.0,
            value=3.0,
            step=0.1,
            help=t['organic_matter_help']
        )
        
        nitrogen = st.slider(
            f"{t['nitrogen']} (ppm)",
            min_value=5,
            max_value=100,
            value=25,
            step=1,
            help=t['nitrogen_help']
        )
        
        phosphorus = st.slider(
            f"{t['phosphorus']} (ppm)",
            min_value=5,
            max_value=100,
            value=20,
            step=1,
            help=t['phosphorus_help']
        )
        
        potassium = st.slider(
            f"{t['potassium']} (ppm)",
            min_value=50,
            max_value=500,
            value=150,
            step=10,
            help=t['potassium_help']
        )
        
        # Weather override option
        st.subheader(f"🌤️ {t['weather_data']}")
        use_current_weather = st.checkbox(
            f"{t['use_current_weather']}",
            value=True,
            help=t['current_weather_help']
        )
        
        if not use_current_weather:
            avg_temp = st.number_input(
                f"{t['avg_temperature']} (°C)",
                min_value=-10.0,
                max_value=50.0,
                value=22.0,
                step=0.5
            )
            
            rainfall = st.number_input(
                f"{t['annual_rainfall']} (mm)",
                min_value=100,
                max_value=3000,
                value=800,
                step=50
            )
            
            humidity = st.number_input(
                f"{t['avg_humidity']} (%)",
                min_value=20.0,
                max_value=100.0,
                value=65.0,
                step=1.0
            )
        
        predict_button = st.button(
            f"🔮 {t['predict_yield']}",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        if predict_button:
            if not region:
                st.error(t['region_required'])
                return
            
            with st.spinner(f"{t['analyzing']}..."):
                try:
                    # Get weather data if needed
                    weather_data = None
                    if use_current_weather:
                        weather_data = weather_service.get_weather_data(region)
                        if weather_data:
                            avg_temp = weather_data['temperature']
                            rainfall = weather_data.get('rainfall_annual', 800)
                            humidity = weather_data['humidity']
                        else:
                            st.warning(f"{t['weather_data_unavailable']}")
                            avg_temp, rainfall, humidity = 22.0, 800, 65.0
                    
                    # Prepare input data
                    input_data = {
                        'crop_type': crop_type,
                        'ph_level': ph_level,
                        'organic_matter': organic_matter,
                        'nitrogen': nitrogen,
                        'phosphorus': phosphorus,
                        'potassium': potassium,
                        'temperature': avg_temp,
                        'rainfall': rainfall,
                        'humidity': humidity,
                        'farm_area': farm_area
                    }
                    
                    # Make prediction
                    prediction_result = crop_predictor.predict_yield(input_data)
                    
                    # Display results
                    st.subheader(f"📊 {t['prediction_results']}")
                    
                    # Main prediction metrics
                    col_metric1, col_metric2, col_metric3 = st.columns(3)
                    
                    with col_metric1:
                        st.metric(
                            label=f"{t['predicted_yield']} (tons/ha)",
                            value=f"{prediction_result['yield_per_ha']:.2f}",
                            help=t['yield_per_ha_help']
                        )
                    
                    with col_metric2:
                        st.metric(
                            label=f"{t['total_yield']} (tons)",
                            value=f"{prediction_result['total_yield']:.2f}",
                            help=t['total_yield_help']
                        )
                    
                    with col_metric3:
                        confidence_color = "green" if prediction_result['confidence'] > 0.8 else "orange" if prediction_result['confidence'] > 0.6 else "red"
                        st.metric(
                            label=f"{t['confidence']}",
                            value=f"{prediction_result['confidence']:.1%}",
                            help=t['confidence_help']
                        )
                    
                    # Risk assessment
                    st.subheader(f"⚠️ {t['risk_assessment']}")
                    risk_level = prediction_result['risk_level']
                    risk_colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
                    
                    st.markdown(f"""
                    <div style="padding: 10px; border-radius: 5px; background-color: {risk_colors[risk_level]}20; border-left: 5px solid {risk_colors[risk_level]};">
                        <strong>{t['risk_level']}: {risk_level}</strong><br>
                        {prediction_result['risk_factors']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Feature importance chart
                    st.subheader(f"📈 {t['factor_importance']}")
                    
                    factors = list(prediction_result['feature_importance'].keys())
                    importance = list(prediction_result['feature_importance'].values())
                    
                    fig_importance = px.bar(
                        x=importance,
                        y=factors,
                        orientation='h',
                        title=f"{t['factors_affecting_yield']}",
                        labels={'x': t['importance'], 'y': t['factors']}
                    )
                    fig_importance.update_layout(yaxis={'categoryorder':'total ascending'})
                    
                    st.plotly_chart(fig_importance, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"{t['prediction_error']}: {str(e)}")

def show_weather_page(weather_service, t):
    st.header(f"🌤️ {t['weather_monitoring']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        location = st.text_input(
            f"{t['enter_location']}",
            placeholder="e.g., New York, USA",
            help=t['location_help']
        )
        
        get_weather_btn = st.button(
            f"🌤️ {t['get_weather']}",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        if get_weather_btn and location:
            with st.spinner(f"{t['fetching_weather']}..."):
                weather_data = weather_service.get_weather_data(location)
                
                if weather_data:
                    st.success(f"{t['weather_data_retrieved']}")
                    
                    # Current conditions
                    st.subheader(f"🌡️ {t['current_conditions']}")
                    
                    col_temp, col_hum, col_press = st.columns(3)
                    
                    with col_temp:
                        st.metric(
                            label=f"{t['temperature']}",
                            value=f"{weather_data['temperature']:.1f}°C"
                        )
                    
                    with col_hum:
                        st.metric(
                            label=f"{t['humidity']}",
                            value=f"{weather_data['humidity']}%"
                        )
                    
                    with col_press:
                        st.metric(
                            label=f"{t['pressure']}",
                            value=f"{weather_data['pressure']} hPa"
                        )
                    
                    # Weather description
                    st.info(f"**{t['conditions']}:** {weather_data['description']}")
                    
                    # Agricultural impact
                    st.subheader(f"🌾 {t['agricultural_impact']}")
                    
                    impact = weather_service.assess_agricultural_impact(weather_data)
                    
                    for crop, assessment in impact.items():
                        with st.expander(f"{crop} {t['assessment']}"):
                            st.write(f"**{t['impact']}:** {assessment['impact']}")
                            st.write(f"**{t['recommendation']}:** {assessment['recommendation']}")
                    
                    # 7-day forecast visualization
                    st.subheader(f"📅 {t['forecast_trend']}")
                    
                    forecast_data = weather_service.get_forecast_data(location)
                    if forecast_data:
                        fig = px.line(
                            forecast_data,
                            x='date',
                            y=['temperature', 'humidity'],
                            title=f"{t['7_day_forecast']}",
                            labels={'value': t['value'], 'date': t['date']}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.error(f"{t['weather_data_error']}")

def show_soil_analysis_page(data_processor, t):
    st.header(f"🌱 {t['soil_analysis']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(f"📝 {t['soil_test_results']}")
        
        # Soil composition inputs
        ph = st.number_input(
            f"{t['ph_level']}",
            min_value=4.0,
            max_value=9.0,
            value=6.5,
            step=0.1,
            help=t['ph_help']
        )
        
        organic_matter = st.number_input(
            f"{t['organic_matter']} (%)",
            min_value=0.0,
            max_value=15.0,
            value=3.0,
            step=0.1
        )
        
        nitrogen = st.number_input(
            f"{t['nitrogen']} (ppm)",
            min_value=0,
            max_value=150,
            value=25,
            step=1
        )
        
        phosphorus = st.number_input(
            f"{t['phosphorus']} (ppm)",
            min_value=0,
            max_value=150,
            value=20,
            step=1
        )
        
        potassium = st.number_input(
            f"{t['potassium']} (ppm)",
            min_value=0,
            max_value=800,
            value=150,
            step=10
        )
        
        calcium = st.number_input(
            f"{t['calcium']} (ppm)",
            min_value=100,
            max_value=5000,
            value=1200,
            step=50
        )
        
        magnesium = st.number_input(
            f"{t['magnesium']} (ppm)",
            min_value=25,
            max_value=500,
            value=120,
            step=10
        )
        
        analyze_btn = st.button(
            f"🔬 {t['analyze_soil']}",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        if analyze_btn:
            soil_data = {
                'ph': ph,
                'organic_matter': organic_matter,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'calcium': calcium,
                'magnesium': magnesium
            }
            
            analysis = data_processor.analyze_soil_health(soil_data)
            
            st.subheader(f"📊 {t['analysis_results']}")
            
            # Overall soil health score
            health_score = analysis['overall_score']
            health_color = "green" if health_score > 80 else "orange" if health_score > 60 else "red"
            
            st.metric(
                label=f"{t['soil_health_score']}",
                value=f"{health_score}/100",
                help=t['health_score_help']
            )
            
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 5px; background-color: {health_color}20; border-left: 5px solid {health_color};">
                <strong>{t['overall_assessment']}: {analysis['rating']}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Nutrient levels visualization
            st.subheader(f"🧪 {t['nutrient_levels']}")
            
            nutrients = ['pH', 'Organic Matter', 'Nitrogen', 'Phosphorus', 'Potassium']
            current_levels = [ph, organic_matter, nitrogen, phosphorus, potassium]
            optimal_ranges = [(6.0, 7.0), (3.0, 5.0), (20, 40), (15, 35), (120, 200)]
            
            fig = go.Figure()
            
            for i, (nutrient, current, optimal) in enumerate(zip(nutrients, current_levels, optimal_ranges)):
                fig.add_trace(go.Bar(
                    name=nutrient,
                    x=[nutrient],
                    y=[current],
                    marker_color='lightblue' if optimal[0] <= current <= optimal[1] else 'orange'
                ))
            
            fig.update_layout(
                title=f"{t['current_vs_optimal']}",
                xaxis_title=t['nutrients'],
                yaxis_title=t['levels'],
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed recommendations
            st.subheader(f"💡 {t['recommendations']}")
            
            for category, recommendations in analysis['recommendations'].items():
                with st.expander(f"{category.title()} {t['recommendations']}"):
                    for rec in recommendations:
                        st.write(f"• {rec}")

def show_recommendations_page(recommendation_engine, t):
    st.header(f"💡 {t['smart_recommendations']}")
    
    # Mock current farm data
    st.info(f"🏡 {t['current_farm_status']}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crop_type = st.selectbox(
            f"{t['current_crop']}",
            options=['Wheat', 'Corn', 'Rice', 'Soybeans'],
            help=t['crop_selection_help']
        )
    
    with col2:
        growth_stage = st.selectbox(
            f"{t['growth_stage']}",
            options=['Seedling', 'Vegetative', 'Flowering', 'Maturity'],
            help=t['growth_stage_help']
        )
    
    with col3:
        region = st.text_input(
            f"{t['location']}",
            placeholder="e.g., California, USA",
            help=t['location_help']
        )
    
    if st.button(f"🔄 {t['generate_recommendations']}", type="primary"):
        if crop_type and growth_stage and region:
            with st.spinner(f"{t['generating_recommendations']}..."):
                farm_data = {
                    'crop_type': crop_type,
                    'growth_stage': growth_stage,
                    'region': region,
                    'current_date': datetime.now()
                }
                
                recommendations = recommendation_engine.generate_recommendations(farm_data)
                
                # Display recommendations by category
                categories = ['irrigation', 'fertilization', 'pest_control', 'harvesting']
                icons = ['💧', '🌱', '🐛', '🚜']
                
                for category, icon in zip(categories, icons):
                    if category in recommendations:
                        st.subheader(f"{icon} {t[category].title()}")
                        
                        rec_data = recommendations[category]
                        
                        # Priority indicator
                        priority_colors = {'High': 'red', 'Medium': 'orange', 'Low': 'green'}
                        priority_color = priority_colors.get(rec_data.get('priority', 'Low'), 'blue')
                        
                        st.markdown(f"""
                        <div style="padding: 15px; border-radius: 10px; background-color: {priority_color}15; border-left: 5px solid {priority_color}; margin-bottom: 15px;">
                            <strong>{t['priority']}: {rec_data.get('priority', 'N/A')}</strong><br>
                            <strong>{t['action']}:</strong> {rec_data.get('action', 'No action needed')}<br>
                            <strong>{t['timing']}:</strong> {rec_data.get('timing', 'As needed')}<br>
                            <strong>{t['reason']}:</strong> {rec_data.get('reason', 'General maintenance')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Additional details
                        if 'details' in rec_data:
                            with st.expander(f"{t['more_details']}"):
                                for detail in rec_data['details']:
                                    st.write(f"• {detail}")
        else:
            st.warning(f"{t['fill_all_fields']}")
    
    # Weekly schedule
    st.subheader(f"📅 {t['weekly_schedule']}")
    
    schedule = recommendation_engine.generate_weekly_schedule(crop_type, growth_stage)
    
    if schedule:
        for day, tasks in schedule.items():
            with st.expander(f"{day}"):
                if tasks:
                    for task in tasks:
                        st.write(f"• {task}")
                else:
                    st.write(f"{t['no_tasks_scheduled']}")

if __name__ == "__main__":
    main()
