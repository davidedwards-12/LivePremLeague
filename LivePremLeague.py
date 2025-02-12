import requests
import json

# URL to the Football API endpoint that retrieves the standings data for the Premier League (league ID 39) for the 2023 season
url = "https://v3.football.api-sports.io/standings?league=39&season=2023"

# Headers including the API key required to authenticate the request
headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",  # Host for the API
    "x-rapidapi-key": "dfae65a3595cb0ac72363e9209e886bf"  # Your API key for authentication
}

# Sending GET request to the API with the specified URL and headers
response = requests.get(url, headers=headers)

# If the response code is 200, meaning the request was successful
if response.status_code == 200:
    # Parse the JSON data from the API response
    data = response.json()
    
    # Optionally, you can print the full response data to check its structure (commented out)
    # print("Full Response:", data)
    
    # Check if "response" exists and contains data (stands for valid API response)
    if "response" in data and data["response"]:
        # Extract standings data from the response
        standings = data["response"][0]["league"]["standings"][0]  # [0] selects the first (and typically only) list of standings for the season
        
        # Printing a header for the standings
        print("\nPremier League Standings (2023):\n")
        print(f"{'Position':<10}{'Team':<30}{'Played':<10}{'W':<5}{'D':<5}{'L':<5}{'Points'}")

        # Loop through each team's data in the standings list
        for team_data in standings:
            # Extract the relevant data for each team in the standings
            position = team_data["rank"]  # Team's position in the league
            team_name = team_data["team"]["name"]  # Team's name
            played = team_data["all"]["played"]  # Number of games played
            wins = team_data["all"]["win"]  # Number of wins
            draws = team_data["all"]["draw"]  # Number of draws
            losses = team_data["all"]["lose"]  # Number of losses
            points = team_data["points"]  # Points accumulated

            # Print each team's data in a formatted manner
            print(f"{position:<10}{team_name:<30}{played:<10}{wins:<5}{draws:<5}{losses:<5}{points}")
    else:
        # If no standings data is available, notify the user
        print("No standings data available.")
else:
    # If the request failed (non-200 response), print the error status code and message
    print(f"Failed to retrieve data: {response.status_code} - {response.text}")