from cgitb import text
import requests
import json
import tkinter as tk
from tkinter import ttk

def get_standings():
    url = "https://v3.football.api-sports.io/standings?league=39&season=2023"
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": "dfae65a3595cb0ac72363e9209e886bf"  # Replace with your API key
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "response" in data and data["response"]:
            return data["response"][0]["league"]["standings"][0]  # Extracting the standings list
    return []

# How the GUI updates the standings
def update_standings():
     for row in table.get_children():
        table.delete(row)  # Clear the table before updating

     standings = get_standings()
     if standings:
         for team_data in standings:
             position = team_data["rank"]
             team_name = team_data["team"]["name"]
             played = team_data["all"]["played"]
             wins = team_data["all"]["win"]
             draws = team_data["all"]["draw"]
             losses = team_data["all"]["lose"]
             points= team_data["points"]

             table.insert("", "end", values=(position, team_name, played, wins, draws, losses, points))
         #else:
             #table.insert("", "end", values=("No data available", "", "", "", "", "", ""))

# Creating the window
root = tk.Tk()
root.title("Premier League Table")
root.geometry("700x400")

# Table (Treeview) for displaying standings
columns = ("Position", "Team", "Played", "W", "D", "L", "Points")
table = ttk.Treeview(root, columns=columns, show="headings")

# Set column headers
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=100)

table.pack(expand=True, fill="both", padx=10, pady=10)

refresh_button = tk.Button(root, text="Refresh the standings", command=update_standings)
refresh_button.pack(pady=10)

update_standings()

root.mainloop()
