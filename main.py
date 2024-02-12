# main.py
from forecast import hourly_temperature
import sys

def check_temperature_above_threshold(latitude, longitude, threshold=30, duration=3):
    """
    Checks if the temperature is above a given threshold for more than a specified duration
    and prints the time periods when this condition is met.
    
    Parameters:
    - latitude (float): Latitude of the location.
    - longitude (float): Longitude of the location.
    - threshold (int): Temperature threshold to check against.
    - duration (int): Duration (in hours) for which the temperature should be above the threshold.
    
    Returns:
    - None
    """
    try:
        # Fetch hourly temperature data
        hourly_temp_df = hourly_temperature(latitude, longitude)
        
        # Initialize variables to track periods of high temperature
        consecutive_hours_above_threshold = 0
        start_time = None
        periods_above_threshold = []

        # Iterate over the DataFrame rows
        for index, row in hourly_temp_df.iterrows():
            if row['temperature_2m'] > threshold:
                consecutive_hours_above_threshold += 1
                if start_time is None:
                    start_time = row['date']
                
                if consecutive_hours_above_threshold >= duration:
                    # If the current period meets the duration condition, record the end time
                    end_time = row['date']
                    periods_above_threshold.append((start_time, end_time))
            else:
                # Reset counters when the temperature drops below the threshold
                consecutive_hours_above_threshold = 0
                start_time = None
        
        # Print the periods when the temperature was above the threshold
        if periods_above_threshold:
            print(f"Periods when the temperature was above {threshold} degrees for more than {duration} consecutive hours:")
            for start, end in periods_above_threshold:
                print(f"From {start} to {end}")
        else:
            print(f"The temperature does not stay above {threshold} degrees for more than {duration} consecutive hours.")

    except ValueError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
