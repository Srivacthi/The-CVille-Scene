import requests

TOKEN = 'XDNRKCFHR7QZCITXRFSE'
BASE_URL = 'https://www.eventbriteapi.com/v3/events/search/'

def search_events(query, location):
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    params = {
        'q': query,  # Search keyword
        'location.address': location,
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


if __name__ == "__main__":
    data = search_events('technology', 'New York')
    if data:
        for event in data.get('events', []):
            print(f"Event: {event['name']['text']}")
            print(f"Starts: {event['start']['local']}")
            print(f"Ends: {event['end']['local']}")
            print(f"URL: {event['url']}\n")

