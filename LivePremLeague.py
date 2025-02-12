import requests
import json

# URL to the Football API that is being used
url = "https://v3.football.api-sports.io/standings?league=39&season=2023"
headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "dfae65a3595cb0ac72363e9209e886bf"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Print the full response data to check the structure
    # print("Full Response:", data)
    
    if "response" in data and data["response"]:
        # Extract standings data
        standings = data["response"][0]["league"]["standings"][0]  # [0] for season's first standings list
        
        print("\nPremier League Standings (2023):\n")
        print(f"{'Position':<10}{'Team':<30}{'Played':<10}{'W':<5}{'D':<5}{'L':<5}{'Points'}")

        # Loop through each team in the standings
        for team_data in standings:
            position = team_data["rank"]
            team_name = team_data["team"]["name"]
            played = team_data["all"]["played"]
            wins = team_data["all"]["win"]
            draws = team_data["all"]["draw"]
            losses = team_data["all"]["lose"]
            points = team_data["points"]

            # Print the formatted data
            print(f"{position:<10}{team_name:<30}{played:<10}{wins:<5}{draws:<5}{losses:<5}{points}")
    else:
        print("No standings data available.")
else:
    print(f"Failed to retrieve data: {response.status_code} - {response.text}")

