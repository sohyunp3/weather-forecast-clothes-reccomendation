import requests
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geopy.geocoders import Nominatim

# Base configuration
BASE_URL = "https://api.weather.gov"

# Database setup
Base = declarative_base()
DATABASE_URL = "sqlite:///./grid_cache.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class GridCache(Base):
    __tablename__ = "grid_cache"
    id = Column(Integer, primary_key=True)
    city = Column(String, index=True, unique=True)
    state = Column(String, index=True)
    latitude = Column(String)
    longitude = Column(String)
    forecast_url = Column(String)

def init_db():
    """
    Initializes the database and creates tables if they don't exist.
    """
    Base.metadata.create_all(bind=engine)

# Geocoding
def get_coordinates_from_location(location_name):
    """
    Converts a city/state name to latitude and longitude using Nominatim API.
    """
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(location_name)
    if location:
        print(f"Coordinates for {location_name}: {location.latitude}, {location.longitude}")
        return location.latitude, location.longitude
    else:
        print(f"Could not find coordinates for {location_name}")
        return None, None

# Fetch Grid Info
def get_grid_info(lat, lon):
    """
    Fetches the grid location info using the /points endpoint.
    """
    endpoint = f"{BASE_URL}/points/{lat},{lon}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        forecast_url = data["properties"]["forecast"]
        print(f"Grid Forecast URL: {forecast_url}")
        return forecast_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching grid information for {lat},{lon}: {e}")
        return None

# Cache Management
def get_grid_info_cached(city, state):
    """
    Fetch grid information from cache or API if not cached.
    """
    db = SessionLocal()
    # Check cache
    cache_entry = db.query(GridCache).filter_by(city=city, state=state).first()
    if cache_entry:
        print(f"Cache hit for {city}, {state}: {cache_entry.forecast_url}")
        return cache_entry.forecast_url

    # If not cached, get coordinates
    lat, lon = get_coordinates_from_location(f"{city}, {state}")
    if lat is None or lon is None:
        return None

    # Call /points API
    forecast_url = get_grid_info(lat, lon)
    if forecast_url:
        # Cache the result
        new_cache = GridCache(
            city=city,
            state=state,
            latitude=str(lat),
            longitude=str(lon),
            forecast_url=forecast_url
        )
        db.add(new_cache)
        db.commit()
        print(f"Cached grid information for {city}, {state}")
        return forecast_url
    return None

# Fetch Forecast
def fetch_forecast(forecast_url):
    """
    Fetches the forecast data from the given grid forecast URL.
    """
    try:
        response = requests.get(forecast_url)
        response.raise_for_status()
        data = response.json()
        print(f"Forecast Data: {data}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None

# Combined Functionality
def fetch_forecast_by_location(city, state):
    """
    Fetch weather forecast by city and state.
    """
    forecast_url = get_grid_info_cached(city, state)
    if not forecast_url:
        print(f"Could not retrieve forecast URL for {city}, {state}")
        return None
    return fetch_forecast(forecast_url)

# # Example Usage
# if __name__ == "__main__":
#     init_db()  # Initialize database

#     # Example user input
#     user_city = input("Enter city: ").strip()
#     user_state = input("Enter state: ").strip()

#     # Fetch forecast
#     forecast_data = fetch_forecast_by_location(user_city, user_state)
#     if forecast_data:
#         print(f"Weather forecast for {user_city}, {user_state}:")
#         for period in forecast_data["properties"]["periods"]:
#             print(f"{period['name']}: {period['shortForecast']}, {period['temperature']}°{period['temperatureUnit']}")
