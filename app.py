"""
Weather App - Streamlit Frontend
A beautiful weather application with web scraping capabilities
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from streamlit_searchbox import st_searchbox
from weather_scraper import WeatherScraper
from data_storage import DataStorage
from city_autocomplete import CityAutocomplete


# Page configuration
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .weather-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 10px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .temp-display {
        font-size: 72px;
        font-weight: bold;
        text-align: center;
        color: #667eea;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .city-name {
        font-size: 36px;
        font-weight: 600;
        color: #764ba2;
        text-align: center;
        margin-bottom: 10px;
    }
    .condition-text {
        font-size: 24px;
        color: #667eea;
        text-align: center;
        font-weight: 500;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    h1, h2, h3 {
        color: white !important;
    }
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)


# Initialize services
@st.cache_resource
def get_services():
    """Initialize scraper, storage, and autocomplete services"""
    return WeatherScraper(), DataStorage(), CityAutocomplete()


def search_cities(searchterm: str):
    """
    Search function for city autocomplete
    
    Args:
        searchterm: User's search input
        
    Returns:
        List of matching cities
    """
    if not searchterm or len(searchterm) < 2:
        return []
    
    # Get autocomplete service
    _, _, autocomplete = get_services()
    
    # Search for cities
    results = autocomplete.search_cities(searchterm, limit=8)
    
    # Return list of tuples (display_name, search_value)
    return [(city['display'], city['value']) for city in results]


def display_current_weather(weather_data: dict, scraper: WeatherScraper):
    """Display current weather in a beautiful card layout"""
    
    emoji = scraper.get_weather_emoji(weather_data['condition'], weather_data.get('weather_code'))
    
    # Main weather display
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Display location with region if available
        location_display = f"{weather_data['city']}, {weather_data['country']}"
        if weather_data.get('region'):
            location_display = f"{weather_data['city']}, {weather_data['region']}, {weather_data['country']}"
        
        st.markdown(f"<div class='city-name'>{location_display}</div>", 
                   unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 80px;'>{emoji}</div>", 
                   unsafe_allow_html=True)
        st.markdown(f"<div class='temp-display'>{weather_data['temperature']}°C</div>", 
                   unsafe_allow_html=True)
        st.markdown(f"<div class='condition-text'>{weather_data['condition']}</div>", 
                   unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; color: white; font-size: 18px; margin-top: 10px;'>Feels like {weather_data['feels_like']}°C</div>", 
                   unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Weather metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 40px;'>💧</div>
            <div style='font-size: 28px; font-weight: bold;'>{weather_data['humidity']}%</div>
            <div style='font-size: 14px; opacity: 0.9;'>Humidity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 40px;'>💨</div>
            <div style='font-size: 28px; font-weight: bold;'>{weather_data['wind_speed']}</div>
            <div style='font-size: 14px; opacity: 0.9;'>km/h {weather_data['wind_direction']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 40px;'>🌡️</div>
            <div style='font-size: 28px; font-weight: bold;'>{weather_data['pressure']}</div>
            <div style='font-size: 14px; opacity: 0.9;'>mb Pressure</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 40px;'>👁️</div>
            <div style='font-size: 28px; font-weight: bold;'>{weather_data['visibility']}</div>
            <div style='font-size: 14px; opacity: 0.9;'>km Visibility</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**☀️ UV Index:** {weather_data['uv_index']}")
    with col2:
        st.markdown(f"**🌧️ Precipitation:** {weather_data['precipitation']} mm")
    with col3:
        st.markdown(f"**🕐 Updated:** {datetime.fromisoformat(weather_data['timestamp']).strftime('%I:%M %p')}")


def display_tomorrow_forecast(forecast_data: dict):
    """Display tomorrow's forecast"""
    st.markdown("## 🌅 Tomorrow's Forecast")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class='weather-card'>
            <h3 style='color: #667eea; text-align: center;'>{forecast_data['date']}</h3>
            <div style='text-align: center; font-size: 48px; font-weight: bold; color: #764ba2;'>
                {forecast_data['max_temp']}°C
            </div>
            <div style='text-align: center; font-size: 24px; color: #667eea;'>
                Min: {forecast_data['min_temp']}°C
            </div>
            <div style='text-align: center; font-size: 18px; color: #666; margin-top: 15px;'>
                {forecast_data['condition']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Astronomy info
        st.markdown(f"""
        <div class='weather-card' style='margin-top: 20px;'>
            <div style='color: #667eea; font-weight: 600; margin-bottom: 10px;'>🌅 Astronomy</div>
            <div style='font-size: 14px;'>
                🌄 Sunrise: {forecast_data['sunrise']}<br>
                🌆 Sunset: {forecast_data['sunset']}<br>
                🌙 Moon Phase: {forecast_data['moon_phase']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Hourly forecast chart
        hourly = forecast_data['hourly_forecast']
        
        # Create hourly temperature chart
        times = [f"{h['time'][:2]}:00" if len(h['time']) == 3 else f"0{h['time'][:1]}:00" 
                for h in hourly]
        temps = [int(h['temp']) for h in hourly]
        feels_like = [int(h['feels_like']) for h in hourly]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=times, y=temps,
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=times, y=feels_like,
            mode='lines',
            name='Feels Like',
            line=dict(color='#764ba2', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Hourly Temperature Forecast",
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            template="plotly_white",
            height=300,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,0.95)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Rain probability chart - only show if there's meaningful rain chance
        rain_chances = [int(h['chance_of_rain']) for h in hourly]
        max_rain_chance = max(rain_chances) if rain_chances else 0
        
        # Only display rain chart if max chance is > 10%
        if max_rain_chance > 10:
            fig2 = go.Figure(go.Bar(
                x=times,
                y=rain_chances,
                marker=dict(color=rain_chances, colorscale='Blues'),
                text=[f"{r}%" for r in rain_chances],
                textposition='outside'
            ))
            
            fig2.update_layout(
                title="Chance of Rain",
                xaxis_title="Time",
                yaxis_title="Probability (%)",
                template="plotly_white",
                height=250,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(255,255,255,0.95)'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        else:
            # Show a nice message instead of empty graph
            st.info(f"☀️ Good news! Low chance of rain tomorrow (max {max_rain_chance}%)")


def display_historical_data(scraper: WeatherScraper, city: str):
    """Display historical weather data for the past week using OpenWeatherMap API"""
    
    st.markdown("## 📈 Past Week's Weather")
    
    # Check if API key is configured
    if not scraper.owm_api_key:
        st.warning("⚠️ OpenWeatherMap API key not configured. Add your API key to `.env` file to see historical weather data.")
        st.info("Get a free API key at: https://openweathermap.org/api")
        return
    
    try:
        with st.spinner("📊 Fetching historical weather data..."):
            # Get historical data from OpenWeatherMap
            historical_data = scraper.get_historical_weather(city, days=7)
        
        if not historical_data:
            st.info("📊 No historical data available. This requires an OpenWeatherMap API key with appropriate access.")
            return
        
        # Prepare data for visualization
        df = pd.DataFrame(historical_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df['day'] = df['date'].dt.strftime('%a %m/%d')
        
        st.caption(f"📅 Showing {len(df)} day(s) of historical weather data")
        
        # Temperature trend chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['temperature'].astype(float),
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#667eea', width=3),
            marker=dict(size=12),
            hovertemplate='<b>%{customdata[0]}</b><br>Temp: %{y}°C<br>%{customdata[1]}<extra></extra>',
            customdata=df[['day', 'condition']].values
        ))
        
        fig.update_layout(
            title=f"Temperature History for {city}",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            template="plotly_white",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,0.95)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Weekly stats summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_temp = df['temperature'].astype(float).mean()
            st.metric("📊 Week Avg", f"{avg_temp:.1f}°C")
        
        with col2:
            max_temp = df['temperature'].astype(float).max()
            st.metric("🔥 Warmest", f"{max_temp:.0f}°C")
        
        with col3:
            min_temp = df['temperature'].astype(float).min()
            st.metric("❄️ Coldest", f"{min_temp:.0f}°C")
        
        with col4:
            avg_humidity = df['humidity'].astype(float).mean()
            st.metric("💧 Avg Humidity", f"{avg_humidity:.0f}%")
            
    except Exception as e:
        st.error(f"❌ Error fetching historical data: {str(e)}")
        st.info("💡 Note: True historical weather data requires a paid OpenWeatherMap subscription. The free tier has limitations.")


def main():
    """Main application"""
    
    # Initialize services
    scraper, storage, autocomplete = get_services()
    
    # Header
    st.markdown("<h1 style='text-align: center; font-size: 48px; margin-bottom: 30px;'>🌤️ Weather Forecast</h1>", 
               unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_city' not in st.session_state:
        st.session_state['current_city'] = None
    
    # Sidebar for search and history
    with st.sidebar:
        st.markdown("## 🔍 Search City")
        
        # Use searchbox with autocomplete
        selected_city = st_searchbox(
            search_cities,
            key="city_searchbox",
            placeholder="Type a city name... (e.g., Birmingham, Riyadh)",
            label="",
            clear_on_submit=True
        )
        
        # When a city is selected from searchbox
        if selected_city:
            st.session_state['current_city'] = selected_city
        
        # Popular cities quick access
        st.markdown("### 🌟 Popular Cities")
        popular = autocomplete.get_top_cities()
        
        cols = st.columns(2)
        for idx, city in enumerate(popular[:6]):
            col_idx = idx % 2
            with cols[col_idx]:
                if st.button(f"📍 {city['city']}", key=f"pop_{idx}", use_container_width=True):
                    st.session_state['current_city'] = city['value']
        
        st.markdown("---")
        
        # Search history
        st.markdown("## 🕐 Recent Searches")
        search_history = storage.get_search_history()
        
        if search_history:
            for past_city in search_history[:10]:
                if st.button(f"📍 {past_city}", key=past_city, use_container_width=True):
                    st.session_state['current_city'] = past_city
        else:
            st.info("No recent searches")
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; font-size: 12px; color: rgba(255,255,255,0.7);'>
            Made with ❤️ using Streamlit<br>
            Data scraped from wttr.in
        </div>
        """, unsafe_allow_html=True)
    
    # Get the city to search for
    city = st.session_state.get('current_city', None)
    
    # Debug info
    if city:
        st.sidebar.markdown(f"**🔍 Searching:** `{city}`")
    
    # Main content area
    if city:
        try:
            with st.spinner(f"🌍 Fetching weather data..."):
                # Get current weather
                weather_data = scraper.get_current_weather(city)
                
                # Check if returned location matches what user expected
                location_str = f"{weather_data['city']}, {weather_data['country']}"
                
                # Save the search value to search history (no longer saving weather data)
                storage.add_search(city)
                
                # Show data source badge
                source = weather_data.get('source', 'wttr.in')
                if source == 'OpenWeatherMap':
                    st.sidebar.info("🔄 Using OpenWeatherMap (fallback)")
                
                # Display current weather
                display_current_weather(weather_data, scraper)
                
                # Show location verification message with source
                st.success(f"✅ Weather data for: **{location_str}** (Source: {source})")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Get and display tomorrow's forecast
                try:
                    forecast_data = scraper.get_tomorrow_forecast(city)
                    display_tomorrow_forecast(forecast_data)
                except Exception as e:
                    st.warning(f"Could not load tomorrow's forecast: {str(e)}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display historical data using OpenWeatherMap API
                display_historical_data(scraper, city)
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Please check the city name and try again. Make sure you have an internet connection.")
    
    else:
        # Welcome screen
        st.markdown("""
        <div style='text-align: center; padding: 50px; color: white;'>
            <div style='font-size: 100px; margin-bottom: 20px;'>🌤️</div>
            <h2>Welcome to Weather Forecast!</h2>
            <p style='font-size: 18px; opacity: 0.9;'>
                Start typing a city name in the sidebar for smart suggestions!<br>
                View current weather, tomorrow's forecast, and this week's history!
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
