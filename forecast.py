import requests
import pandas as pd

def hourly_temperature(latitude, longitude):
    """
    Fetches hourly temperature data for a given location from the Open-Meteo API.
    
    Parameters:
    - latitude (float): Latitude of the location.
    - longitude (float): Longitude of the location.
    
    Returns:
    - pd.DataFrame: A dataframe containing the date and hourly temperature (in °C) for the location.
    
    Raises:
    - ValueError: If the API call is unsuccessful, returns no data, or the DataFrame is empty.
    """
    # Open-Meteo API endpoint with specified parameters
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m"
    }
    
    # Send GET request to the Open-Meteo API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract data from response
        data = response.json()
        hourly_data = data.get('hourly', {})
        time = hourly_data.get('time', [])
        temperature_2m = hourly_data.get('temperature_2m', [])
        
        # Ensure there is data to process
        if not time or not temperature_2m:
            raise ValueError("No data found for the specified location and variables.")
        
        # Create a DataFrame
        df = pd.DataFrame({
            'date': pd.to_datetime(time),
            'temperature_2m': temperature_2m
        })
        
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("Failed to create a non-empty DataFrame from the fetched data.")
        
        return df
    else:
        raise ValueError(f"Error fetching data: HTTP {response.status_code}")
