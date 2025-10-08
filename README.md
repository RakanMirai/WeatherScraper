# 🌤️ Weather Forecast Application

A beautiful weather application built with Streamlit and web scraping capabilities. Get real-time weather data, tomorrow's forecast, and track weather history for the current week!

## ✨ Features

- **🌍 Real-Time Weather**: Scrapes live weather data from wttr.in with OpenWeatherMap fallback
- **🔍 Smart Autocomplete**: Type a city name and get intelligent suggestions with country info (e.g., Birmingham, UK vs Birmingham, USA)
- **📅 Tomorrow's Forecast**: Detailed hourly forecast with temperature and rain probability
- **📊 Past Week's Weather**: Real historical weather data via OpenWeatherMap API (optional - requires API key)
- **🔄 Smart Fallback**: Automatically switches to OpenWeatherMap if wttr.in fails
- **⭐ Popular Cities**: Quick access buttons for major world cities
- **🕐 Search History**: Recently searched cities for quick access
- **🎨 Beautiful UI**: Modern gradient design with interactive charts
- **📈 Data Visualization**: Temperature trends and rain probability charts using Plotly

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Web Scraping**: Requests + BeautifulSoup4
- **APIs**: OpenWeatherMap API (optional, for fallback and historical data)
- **Data Visualization**: Plotly
- **Data Processing**: Pandas
- **Data Sources**: 
  - wttr.in (primary - free, no API key)
  - OpenWeatherMap (fallback and historical)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd WeatherScraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Setup OpenWeatherMap API**:
   ```bash
   # Copy the example env file
   copy .env.example .env
   
   # Edit .env and add your API key
   OPENWEATHERMAP_API_KEY=your_key_here
   ```
   
   **Note**: The app works without an API key! See [SETUP.md](SETUP.md) for details.

## 🚀 Usage

Run the application:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

**Without API Key**: Works perfectly! Shows current weather and tomorrow's forecast.  
**With API Key**: Adds fallback support and historical weather data (requires paid subscription for full historical data).

## 📱 How to Use

1. **Smart Search**: Start typing a city name in the sidebar - autocomplete suggestions will appear
2. **Select City**: Choose from the dropdown suggestions (shows city, country/state)
3. **Quick Access**: Use popular city buttons or recent search history for instant results
4. **View Weather**: See current conditions, tomorrow's forecast, and weekly history
5. **Disambiguate**: For cities with same names (e.g., Birmingham), select the correct country from suggestions

## 📂 Project Structure

```
WeatherScraper/
├── app.py                 # Main Streamlit application
├── weather_scraper.py     # Web scraping module
├── city_autocomplete.py   # City search and autocomplete
├── data_storage.py        # Data management and history
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── data/                 # Generated data directory
    ├── weather_history.json
    └── search_history.json
```

## 🎯 Key Components

### Weather Scraper (`weather_scraper.py`)
- Scrapes real-time weather data from wttr.in
- Provides current conditions and forecasts
- Includes emoji mapping for weather conditions

### City Autocomplete (`city_autocomplete.py`)
- Uses OpenStreetMap Nominatim API for city search
- Provides intelligent suggestions with country/state info
- Handles ambiguous city names (e.g., Birmingham, UK vs USA)
- Includes popular cities list for quick access
- Implements rate limiting and caching

### Data Storage (`data_storage.py`)
- Manages weather history (current week only)
- Tracks search history
- Automatically cleans old data at week start

### Streamlit App (`app.py`)
- Beautiful gradient UI with glass morphism effects
- Smart searchbox with autocomplete functionality
- Interactive Plotly charts
- Responsive layout with metrics cards
- Real-time data updates

## 🌟 Features in Detail

### Current Weather Display
- Large temperature display with emoji
- Feels-like temperature
- Humidity, wind speed, pressure, visibility
- UV index and precipitation data
- Last update timestamp

### Tomorrow's Forecast
- Min/max/average temperatures
- Hourly temperature chart (temperature vs feels-like)
- Rain probability bar chart
- Sunrise/sunset times
- Moon phase information

### Historical Weather Data
- **Real historical weather data** from OpenWeatherMap API
- Shows past 7 days of weather with daily temperature trends
- Weekly statistics (avg, max, min temps, humidity)
- Automatically fetched when you search for a city
- **Requires**: OpenWeatherMap API key (free tier has limitations)
- **Note**: Full historical data requires paid OpenWeatherMap subscription

### Search History
- Last 20 searched cities
- One-click quick search
- No duplicates in history

## 🔧 Configuration

The application uses default settings but can be customized:

- **Data Directory**: Modify `data_dir` in `DataStorage` initialization
- **History Limit**: Change the number `20` in `data_storage.py` for search history
- **Week Start**: Currently set to Monday, modify `_filter_current_week()` to change

## 📝 Notes

- **Primary data source**: wttr.in (free, no API key required)
- **Fallback**: OpenWeatherMap API (optional, for reliability)
- **Historical data**: Requires OpenWeatherMap API key
- **Free tier limitations**: Current weather and forecast work fine; historical data requires paid subscription
- **Search history**: Persists across sessions (stored locally in JSON)
- **.env file**: Not tracked in git (add your API key safely)

## 🐛 Troubleshooting

**Issue**: "Failed to fetch weather data"
- Check your internet connection
- Verify the city name is correct
- If wttr.in is down, add an OpenWeatherMap API key for fallback

**Issue**: "No historical data available"
- You need an OpenWeatherMap API key (see [SETUP.md](SETUP.md))
- Free tier has limitations - full historical requires paid subscription
- The app will show a helpful message if API key is missing

**Issue**: Charts not displaying
- Ensure plotly is installed correctly (`pip install -r requirements.txt`)
- Try refreshing the browser
- Check browser console for JavaScript errors

## 🚀 Future Enhancements

- Multiple city comparison
- Weather alerts and warnings
- Export data to CSV
- Dark/light theme toggle
- Celsius/Fahrenheit conversion
- Weather radar maps

## 📄 License

This project is open source and available for personal and educational use.

## 🙏 Acknowledgments

- Weather data provided by [wttr.in](https://wttr.in)
- Built with [Streamlit](https://streamlit.io)
- Charts powered by [Plotly](https://plotly.com)

---

**Made with ❤️ using Streamlit**