import requests
import pandas as pd
import time 

url = "https://api.github.com/orgs/ORG/copilot/billing/seats"

# Initialize variables
page = 1
per_page = 100
all_data = []

try:
    while True:
        # Define the query parameters for the current page
        params = {
            'page': page,
            'per_page': per_page
        }

        # Make the API request with query parameters
        response = requests.get(url, params=params)

        # Check the response status code
        if response.status_code == 200:
            # Parse and append the 'seats' data from the response
            data = response.json()
            if not data:
                break
            all_data.extend(data['seats'])
            # Increment the page number for the next request
            page += 1
        elif response.status_code == 403:
            # Handle rate limiting, sleep and retry if needed
            reset_time = int(response.headers.get('X-RateLimit-Reset', 60))
            sleep_time = max(reset_time - int(time.time()), 1)
            time.sleep(sleep_time)
        else:
            # Handle other HTTP errors
            response.raise_for_status()

except requests.exceptions.RequestException as e:
    print(f"Request Exception: {e}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Create a DataFrame from the collected data
df = pd.DataFrame(all_data)

# Now you can work with the DataFrame 'df' for further analysis
print(df)
