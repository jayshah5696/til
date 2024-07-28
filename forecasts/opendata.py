import requests
import pandas as pd

def get_forecast(longitude, latitude):
    # Define the API endpoint
    url = f"https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json"
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract the time series data
        time_series = data['timeSeries']
        
        # Prepare a list to hold the parsed data
        forecast_data = []
        
        # Loop through each time point in the time series
        for entry in time_series:
            valid_time = entry['validTime']
            parameters = {param['name']: param['values'][0] for param in entry['parameters']}
            parameters['validTime'] = valid_time
            forecast_data.append(parameters)
        
        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(forecast_data)
        
        return df
    else:
        return f"Error: {response.status_code} - {response.text}"
def main():
    # Example usage
    longitude = 16
    latitude = 58
    forecast_df = get_forecast(longitude, latitude)
    print(forecast_df.head())

if __name__ == "__main__":
    main()