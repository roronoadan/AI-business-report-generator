import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_weather_data(city="Algiers", days=30):
    """
    Fetch last 30 days of weather data for any city.
    Using Open-Meteo API — completely free, no key needed.
    """
    # Get coordinates for city
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo = requests.get(geo_url).json()
    
    if not geo.get("results"):
        raise ValueError(f"City '{city}' not found")
    
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    country = geo["results"][0].get("country", "")
    
    # Date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    # Fetch weather data
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,"
        f"precipitation_sum,wind_speed_10m_max"
        f"&start_date={start_date}&end_date={end_date}"
        f"&timezone=auto"
    )
    
    weather = requests.get(weather_url).json()
    daily = weather["daily"]
    
    df = pd.DataFrame({
        "date": pd.to_datetime(daily["time"]),
        "temp_max": daily["temperature_2m_max"],
        "temp_min": daily["temperature_2m_min"],
        "precipitation": daily["precipitation_sum"],
        "wind_speed": daily["wind_speed_10m_max"]
    })
    
    df["temp_avg"] = (df["temp_max"] + df["temp_min"]) / 2
    df["city"] = city
    df["country"] = country
    
    print(f"✅ Fetched {len(df)} days of data for {city}, {country}")
    return df

if __name__ == "__main__":
    df = fetch_weather_data("Algiers", 30)
    print(df.head())
    df.to_csv("data/raw_data.csv", index=False)
    print("✅ Data saved to data/raw_data.csv")