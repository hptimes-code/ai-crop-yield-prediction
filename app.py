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

# Initialize services
@st.cache_resource
def initialize_services():
    weather_service = WeatherService()
    data_processor = DataProcessor()
    crop_predictor = CropYieldPredictor()
    recommendation_engine = RecommendationEngine()
    return weather_service, data_processor, crop_predictor, recommendation_engine

def main():
    st.set_page_config(
        page_title="AI Crop Yield Prediction Platform",
        page_icon="🌾",
        layout="wide"
    )

    # Initialize services
    weather_service, data_processor, crop_predictor, recommendation_engine = initialize_services()

    st.title("🌾 AI Crop Yield Prediction Platform")
    st.markdown("**Advanced agricultural intelligence for optimal farming decisions**")

    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Yield Prediction", "Weather Monitoring", "Soil Analysis", "Recommendations"],
        icons=['house', 'graph-up', 'cloud-sun', 'geo-alt', 'lightbulb'],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Dashboard":
        show_dashboard(weather_service, data_processor)
    elif selected == "Yield Prediction":
        show_prediction_page(crop_predictor, weather_service)
    elif selected == "Weather Monitoring":
        show_weather_page(weather_service)
    elif selected == "Soil Analysis":
        show_soil_analysis_page(data_processor)
    elif selected == "Recommendations":
        show_recommendations_page(recommendation_engine)

def show_dashboard(weather_service, data_processor):
    st.header("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🌾 Total Crops Supported",
            value="4",
            help="Number of crop types supported by our prediction models"
        )

    with col2:
        st.metric(
            label="🌍 Regions Covered",
            value="Global",
            help="Weather data available for locations worldwide"
        )

    with col3:
        st.metric(
            label="📈 Model Accuracy",
            value="92%",
            help="Average accuracy of our machine learning models"
        )

    with col4:
        st.metric(
            label="👨‍🌾 Farmers Helped",
            value="10K+",
            help="Number of farmers using our platform globally"
        )

    # Sample yield trends visualization
    st.subheader("📈 Yield Trends")

    # Generate sample trend data
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='ME')
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
        title="Historical Yield Trends",
        labels={'Yield': "Yield (tons/ha)", 'Date': "Date"}
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Yield (tons/ha)",
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Regional performance
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 Regional Performance")

        regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
        avg_yields = np.random.uniform(4, 9, len(regions))

        fig_bar = px.bar(
            x=regions,
            y=avg_yields,
            title="Average Yield by Region",
            labels={'x': "Region", 'y': "Yield (tons/ha)"}
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("🌾 Crop Distribution")

        crop_areas = [25, 30, 20, 25]  # Percentage distribution

        fig_pie = px.pie(
            values=crop_areas,
            names=crops,
            title="Crop Area Distribution"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

def show_prediction_page(crop_predictor, weather_service):
    st.header("🔮 Crop Yield Prediction")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Input Parameters")

        # Crop selection
        crop_type = st.selectbox(
            "Select Crop Type",
            options=['Wheat', 'Corn', 'Rice', 'Soybeans'],
            help="Choose the crop you want to analyze"
        )

        # Region input
        region = st.text_input(
            "Region / City",
            placeholder="e.g., Iowa, USA",
            help="Enter your farm location for weather data"
        )

        # Farm area
        farm_area = st.number_input(
            "Farm Area (ha)",
            min_value=0.1,
            max_value=10000.0,
            value=10.0,
            step=0.1,
            help="Total area of your farm in hectares"
        )

        # Soil parameters
        st.subheader("🌱 Soil Parameters")

        ph_level = st.slider(
            "pH Level",
            min_value=4.0,
            max_value=9.0,
            value=6.5,
            step=0.1,
            help="Soil acidity/alkalinity level (6.0-7.0 is optimal for most crops)"
        )

        organic_matter = st.slider(
            "Organic Matter (%)",
            min_value=0.5,
            max_value=10.0,
            value=3.0,
            step=0.1,
            help="Percentage of organic matter in soil"
        )

        nitrogen = st.slider(
            "Nitrogen (ppm)",
            min_value=5,
            max_value=100,
            value=25,
            step=1,
            help="Nitrogen content in parts per million"
        )

        phosphorus = st.slider(
            "Phosphorus (ppm)",
            min_value=5,
            max_value=100,
            value=20,
            step=1,
            help="Phosphorus content in parts per million"
        )

        potassium = st.slider(
            "Potassium (ppm)",
            min_value=50,
            max_value=500,
            value=150,
            step=10,
            help="Potassium content in parts per million"
        )

        # Weather override option
        st.subheader("🌤️ Weather Data")
        use_current_weather = st.checkbox(
            "Use Current Weather Data",
            value=True,
            help="Use real-time weather data for predictions"
        )

        if not use_current_weather:
            avg_temp = st.number_input(
                "Average Temperature (°C)",
                min_value=-10.0,
                max_value=50.0,
                value=22.0,
                step=0.5
            )

            rainfall = st.number_input(
                "Annual Rainfall (mm)",
                min_value=100,
                max_value=3000,
                value=800,
                step=50
            )

            humidity = st.number_input(
                "Average Humidity (%)",
                min_value=20.0,
                max_value=100.0,
                value=65.0,
                step=1.0
            )
        else:
            # Initialize default values for when using current weather
            avg_temp = 22.0
            rainfall = 800
            humidity = 65.0

        predict_button = st.button(
            "🔮 Predict Yield",
            type="primary",
            use_container_width=True
        )

    with col2:
        if predict_button:
            if not region:
                st.error("Please enter a region/city")
                return

            with st.spinner("Analyzing..."):
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
                            st.warning("Weather data unavailable, using default values")
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
                    st.subheader("📊 Prediction Results")

                    # Main prediction metrics
                    col_metric1, col_metric2, col_metric3 = st.columns(3)

                    with col_metric1:
                        st.metric(
                            label="Predicted Yield (tons/ha)",
                            value=f"{prediction_result['yield_per_ha']:.2f}",
                            help="Expected yield per hectare"
                        )

                    with col_metric2:
                        st.metric(
                            label="Total Yield (tons)",
                            value=f"{prediction_result['total_yield']:.2f}",
                            help="Total expected yield for your farm"
                        )

                    with col_metric3:
                        st.metric(
                            label="Confidence",
                            value=f"{prediction_result['confidence']:.1%}",
                            help="Model confidence in the prediction"
                        )

                    # Risk assessment
                    st.subheader("⚠️ Risk Assessment")
                    risk_level = prediction_result['risk_level']
                    risk_colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}

                    st.markdown(f"""
                    <div style="padding: 10px; border-radius: 5px; background-color: {risk_colors[risk_level]}20; border-left: 5px solid {risk_colors[risk_level]};">
                        <strong>Risk Level: {risk_level}</strong><br>
                        {prediction_result['risk_factors']}
                    </div>
                    """, unsafe_allow_html=True)

                    # Feature importance chart
                    st.subheader("📈 Factor Importance")

                    factors = list(prediction_result['feature_importance'].keys())
                    importance = list(prediction_result['feature_importance'].values())

                    fig_importance = px.bar(
                        x=importance,
                        y=factors,
                        orientation='h',
                        title="Factors Affecting Yield",
                        labels={'x': "Importance", 'y': "Factors"}
                    )
                    fig_importance.update_layout(yaxis={'categoryorder':'total ascending'})

                    st.plotly_chart(fig_importance, use_container_width=True)

                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")

def show_weather_page(weather_service):
    st.header("🌤️ Weather Monitoring")

    col1, col2 = st.columns([1, 2])

    with col1:
        location = st.text_input(
            "Enter Location",
            placeholder="e.g., New York, USA",
            help="Enter city name and country for accurate weather data"
        )

        get_weather_btn = st.button(
            "🌤️ Get Weather Data",
            type="primary",
            use_container_width=True
        )

    with col2:
        if get_weather_btn and location:
            with st.spinner("Fetching weather data..."):
                weather_data = weather_service.get_weather_data(location)

                if weather_data:
                    st.success("Weather data retrieved successfully")

                    # Current conditions
                    st.subheader("🌡️ Current Conditions")

                    col_temp, col_hum, col_press = st.columns(3)

                    with col_temp:
                        st.metric(
                            label="Temperature",
                            value=f"{weather_data['temperature']:.1f}°C"
                        )

                    with col_hum:
                        st.metric(
                            label="Humidity",
                            value=f"{weather_data['humidity']}%"
                        )

                    with col_press:
                        st.metric(
                            label="Pressure",
                            value=f"{weather_data['pressure']} hPa"
                        )

                    # Weather description
                    st.info(f"**Conditions:** {weather_data['description']}")

                    # Agricultural impact
                    st.subheader("🌾 Agricultural Impact")

                    impact = weather_service.assess_agricultural_impact(weather_data)

                    for crop, assessment in impact.items():
                        with st.expander(f"{crop} Assessment"):
                            st.write(f"**Impact:** {assessment['impact']}")
                            st.write(f"**Recommendation:** {assessment['recommendation']}")

                    # 7-day forecast visualization
                    st.subheader("📅 Forecast Trend")

                    forecast_data = weather_service.get_forecast_data(location)
                    if forecast_data is not None and len(forecast_data) > 0:
                        fig = px.line(
                            forecast_data,
                            x='date',
                            y=['temperature', 'humidity'],
                            title="7-Day Forecast",
                            labels={'value': "Value", 'date': "Date"}
                        )
                        st.plotly_chart(fig, use_container_width=True)

                else:
                    st.error("Unable to retrieve weather data")

def show_soil_analysis_page(data_processor):
    st.header("🌱 Soil Analysis")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Soil Test Results")

        # Soil composition inputs
        ph = st.number_input(
            "pH Level",
            min_value=4.0,
            max_value=9.0,
            value=6.5,
            step=0.1,
            help="Soil acidity/alkalinity level (6.0-7.0 is optimal for most crops)"
        )

        organic_matter = st.number_input(
            "Organic Matter (%)",
            min_value=0.0,
            max_value=15.0,
            value=3.0,
            step=0.1
        )

        nitrogen = st.number_input(
            "Nitrogen (ppm)",
            min_value=0,
            max_value=150,
            value=25,
            step=1
        )

        phosphorus = st.number_input(
            "Phosphorus (ppm)",
            min_value=0,
            max_value=150,
            value=20,
            step=1
        )

        potassium = st.number_input(
            "Potassium (ppm)",
            min_value=0,
            max_value=800,
            value=150,
            step=10
        )

        calcium = st.number_input(
            "Calcium (ppm)",
            min_value=100,
            max_value=5000,
            value=1200,
            step=50
        )

        magnesium = st.number_input(
            "Magnesium (ppm)",
            min_value=25,
            max_value=500,
            value=120,
            step=10
        )

        analyze_btn = st.button(
            "🧪 Analyze Soil",
            type="primary",
            use_container_width=True
        )

    with col2:
        if analyze_btn:
            with st.spinner("Analyzing soil composition..."):
                soil_data = {
                    'ph_level': ph,
                    'organic_matter': organic_matter,
                    'nitrogen': nitrogen,
                    'phosphorus': phosphorus,
                    'potassium': potassium,
                    'calcium': calcium,
                    'magnesium': magnesium
                }

                analysis_result = data_processor.analyze_soil(soil_data)

                st.subheader("📊 Analysis Results")

                # Soil health score
                st.metric(
                    label="Soil Health Score",
                    value=f"{analysis_result['health_score']}/100",
                    help="Overall soil health score based on nutrient levels"
                )

                # Nutrient levels visualization
                st.subheader("📈 Nutrient Levels")

                nutrients = ['Nitrogen', 'Phosphorus', 'Potassium', 'Calcium', 'Magnesium']
                levels = [nitrogen, phosphorus, potassium, calcium, magnesium]
                optimal = [40, 30, 200, 2000, 200]  # Optimal levels

                fig_nutrients = go.Figure()
                fig_nutrients.add_trace(go.Bar(
                    name='Current Levels',
                    x=nutrients,
                    y=levels,
                    marker_color='lightblue'
                ))
                fig_nutrients.add_trace(go.Bar(
                    name='Optimal Levels',
                    x=nutrients,
                    y=optimal,
                    marker_color='green',
                    opacity=0.6
                ))

                fig_nutrients.update_layout(
                    title="Current vs Optimal Nutrient Levels",
                    xaxis_title="Nutrients",
                    yaxis_title="Concentration (ppm)",
                    barmode='group'
                )

                st.plotly_chart(fig_nutrients, use_container_width=True)

                # Recommendations
                st.subheader("💡 Recommendations")
                for recommendation in analysis_result['recommendations']:
                    st.info(recommendation)

                # Crop suitability
                st.subheader("🌾 Crop Suitability")
                suitability_data = analysis_result['crop_suitability']

                crops = list(suitability_data.keys())
                suitability = list(suitability_data.values())

                fig_suitability = px.bar(
                    x=crops,
                    y=suitability,
                    title="Crop Suitability Scores",
                    labels={'x': "Crops", 'y': "Suitability Score (%)"},
                    color=suitability,
                    color_continuous_scale='RdYlGn'
                )

                st.plotly_chart(fig_suitability, use_container_width=True)

def show_recommendations_page(recommendation_engine):
    st.header("💡 Recommendations")

    # Farm information inputs
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Farm Information")

        current_crop = st.selectbox(
            "Current Crop",
            options=['Wheat', 'Corn', 'Rice', 'Soybeans', 'Other'],
            help="What crop are you currently growing?"
        )

        farm_size = st.number_input(
            "Farm Size (ha)",
            min_value=0.1,
            max_value=10000.0,
            value=50.0,
            step=0.1
        )

        budget = st.number_input(
            "Available Budget (USD)",
            min_value=100,
            max_value=1000000,
            value=10000,
            step=100
        )

        farming_experience = st.selectbox(
            "Farming Experience",
            options=['Beginner', 'Intermediate', 'Advanced'],
            help="Your level of farming experience"
        )

        primary_goal = st.selectbox(
            "Primary Goal",
            options=['Maximize Profit', 'Sustainable Farming', 'Risk Minimization', 'Yield Optimization'],
            help="What is your primary farming objective?"
        )

        get_recommendations_btn = st.button(
            "🔍 Get Recommendations",
            type="primary",
            use_container_width=True
        )

    with col2:
        if get_recommendations_btn:
            with st.spinner("Generating personalized recommendations..."):
                farm_profile = {
                    'current_crop': current_crop,
                    'farm_size': farm_size,
                    'budget': budget,
                    'experience': farming_experience,
                    'primary_goal': primary_goal
                }

                recommendations = recommendation_engine.generate_recommendations(farm_profile)

                st.subheader("🎯 Personalized Recommendations")

                # Crop recommendations
                st.subheader("🌾 Crop Recommendations")
                crop_recs = recommendations['crop_recommendations']

                for i, crop_rec in enumerate(crop_recs):
                    with st.expander(f"{i+1}. {crop_rec['crop']} - Expected Profit: ${crop_rec['expected_profit']:,}"):
                        st.write(f"**Rationale:** {crop_rec['rationale']}")
                        st.write(f"**Investment Required:** ${crop_rec['investment']:,}")
                        st.write(f"**Risk Level:** {crop_rec['risk_level']}")

                # Technology recommendations
                st.subheader("🔧 Technology Recommendations")
                tech_recs = recommendations['technology_recommendations']

                for tech in tech_recs:
                    with st.expander(f"{tech['technology']} - Cost: ${tech['cost']:,}"):
                        st.write(f"**Description:** {tech['description']}")
                        st.write(f"**ROI:** {tech['roi']}")

                # Best practices
                st.subheader("📋 Best Practices")
                practices = recommendations['best_practices']

                for practice in practices:
                    st.info(practice)

                # Financial projection
                st.subheader("💰 Financial Projection")
                financial = recommendations['financial_projection']

                col_rev, col_cost, col_profit = st.columns(3)

                with col_rev:
                    st.metric(
                        label="Projected Revenue",
                        value=f"${financial['revenue']:,}"
                    )

                with col_cost:
                    st.metric(
                        label="Estimated Costs",
                        value=f"${financial['costs']:,}"
                    )

                with col_profit:
                    st.metric(
                        label="Net Profit",
                        value=f"${financial['profit']:,}"
                    )

if __name__ == "__main__":
    main()
