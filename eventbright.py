import requests
import json

# Replace this with your actual Eventbrite API token
API_TOKEN = 'XDNRKCFHR7QZCITXRFSE'

#url = 'https://www.eventbriteapi.com/v3/events/search/'
user_url = 'https://www.eventbriteapi.com/v3/users/me/'
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}
user_response = requests.get(user_url, headers=headers)
print(f"Token Validation Status: {user_response.status_code}")
print(user_response.json())

# params = {
#     'q': 'tech conference',              # Search term
#     'location.address': 'San Francisco',  # Location
#     'sort_by': 'date',                    # Sort by date
#     'expand': 'venue'                     # Expand venue details
# }

# # Debugging: Check the request response
# try:
#     response = requests.get(url, headers=headers, params=params)
#     print(f"Status Code: {response.status_code}")  # Check HTTP status code

#     if response.status_code == 200:
#         data = response.json()

#         # Debug: Print the entire JSON response (for inspection)
#         print(json.dumps(data, indent=4))

#         # Check if 'events' key exists and is not empty
#         if 'events' in data and data['events']:
#             for event in data['events']:
#                 print(f"Event Name: {event['name']['text']}")
#                 print(f"Start Date: {event['start']['local']}")
#                 print(f"End Date: {event['end']['local']}")
#                 print(f"URL: {event['url']}")
#                 print("-" * 50)
#         else:
#             print("No events found. Try changing the search parameters.")
#     else:
#         print(f"Error: Received status code {response.status_code}")
#         print(f"Response Content: {response.text}")

# except Exception as e:
#     print(f"An error occurred: {e}")
