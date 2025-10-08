# Setup Guide

## 🔑 Getting Your OpenWeatherMap API Key

The app uses OpenWeatherMap API for:
- **Fallback** when wttr.in is unavailable
- **Historical weather data** (past week's weather)

### Steps to Get API Key:

1. **Sign up** at [OpenWeatherMap](https://openweathermap.org/api)
2. **Choose a plan**:
   - **Free Tier**: Good for basic usage (60 calls/minute, current weather, 5-day forecast)
   - **Paid Tier**: Required for full historical weather data
3. **Get your API key** from your account dashboard
4. **Create `.env` file** in the project root:

```bash
# Copy the example file
copy .env.example .env
```

5. **Edit `.env` file** and add your key:

```env
OPENWEATHERMAP_API_KEY=your_actual_api_key_here
```

## ⚙️ Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the app**:
```bash
streamlit run app.py
```

## 📝 Notes

### Historical Weather Data Limitations

- **Free Tier**: The app will show a message that historical data is not available
- **Paid Tier** ($40+/month): Full access to historical weather data
- **Alternative**: The app still shows current weather and tomorrow's forecast without any subscription!

### Data Sources

The app intelligently uses multiple sources:

1. **wttr.in** (primary): Free, no API key needed
   - Current weather ✅
   - Tomorrow's forecast ✅
   - Historical data ❌

2. **OpenWeatherMap** (fallback/historical):
   - Current weather ✅ (fallback if wttr.in fails)
   - Tomorrow's forecast ✅
   - Historical data ✅ (requires paid subscription)

## 🆓 Using Without API Key

You can use the app WITHOUT an OpenWeatherMap API key! It will:
- ✅ Show current weather (from wttr.in)
- ✅ Show tomorrow's forecast (from wttr.in)
- ⚠️ Skip historical weather section (shows info message)

The API key is only needed for:
- Fallback when wttr.in is down
- Historical weather data (requires paid subscription anyway)
