from PIL import Image, ImageTk
import requests
import json
import tkinter as tk
from tkinter import ttk

# Function to get standings data
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
            return data["response"][0]["league"]["standings"][0]  # Extracting standings list
    return []

# Download & Resize Logos
def load_team_logo(team_name):
    try:
        image_path = f"TeamLogos/{team_name}.png"  # Ensure file names match exactly
        image = Image.open(image_path)
        image = image.resize((30, 30), Image.LANCZOS)  # Resize logo for display
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading logo for {team_name}: {e}")
        return None  # Return None if the image is missing

# Dictionary to store images to prevent garbage collection
logo_images = {}

# Function to update the table with new standings
def update_standings():
    for row in table.get_children():
        table.delete(row)  # Clear previous standings

    standings = get_standings()
    logo_dict.clear()  # Clear logo dictionary on each update
    
    if standings:
        for index, team_data in enumerate(standings):
            position = team_data["rank"]
            team_name = team_data["team"]["name"]
            played = team_data["all"]["played"]
            wins = team_data["all"]["win"]
            draws = team_data["all"]["draw"]
            losses = team_data["all"]["lose"]
            points = team_data["points"]

            # Load logo
            logo = load_team_logo(team_name)
            if logo:
                logo_images[team_name] = logo  # Store the logo in dictionary to prevent garbage collection

            # Assign row colors based on position
            row_tag = "normal"
            if position == 1:
                row_tag = "champion"  # First place (champion)
            elif position >= len(standings) - 2:
                row_tag = "relegation"  # Bottom 3 teams (relegation)

            # Insert the data into the table with the appropriate tag and corrected column
            table.insert("", "end", values=(position, logo, team_name, played, wins, draws, losses, points), tags=(row_tag,))

            # Insert the logo into the second column after inserting the row
            table.item(table.get_children()[-1], image=logo)  # Assign the logo image to the row

    else:
        table.insert("", "end", values=("No data available", "", "", "", "", "", ""))

# Create the main window
root = tk.Tk()
root.title("Premier League Standings")
root.geometry("900x550")

# Dictionary to store team logos
logo_dict = {}

# Title label
title_label = tk.Label(root, text=" Premier League Standings ", font=("Arial", 16, "bold"), fg="darkblue")
title_label.pack(pady=10)

# Table (Treeview) for displaying standings
columns = ("Position", "Logo", "Team", "Played", "W", "D", "L", "Points")
table = ttk.Treeview(root, columns=columns, show="headings")

# Apply color styling to rows
table.tag_configure("champion", background="lightgreen", font=("Arial", 10, "bold"))  # Green for champion
table.tag_configure("relegation", background="red", foreground="white", font=("Arial", 10, "bold"))  # Red for relegated
table.tag_configure("normal", background="white", font=("Arial", 10))  # Default styling

# To give enough space for logos, you can modify the Treeview widget to make sure there’s enough room
table.column("Logo", anchor="center", width=80)  # Ensure enough width for the logo column
table.heading("Logo", text="Logo")
table.configure(height=50)  # Set row height to be larger (adjust as needed)

# Set column headers
table.heading("Position", text="Position")
table.column("Position", anchor="center", width=80)
table.heading("Logo", text="Logo")
table.column("Logo", anchor="center", width=80)  # Adjusted width for the logo column
table.heading("Team", text="Team")
table.column("Team", anchor="center", width=180)
table.heading("Played", text="Played")
table.column("Played", anchor="center", width=80)
table.heading("W", text="W")
table.column("W", anchor="center", width=50)
table.heading("D", text="D")
table.column("D", anchor="center", width=50)
table.heading("L", text="L")
table.column("L", anchor="center", width=50)
table.heading("Points", text="Points")
table.column("Points", anchor="center", width=80)

table.pack(expand=True, fill="both", padx=10, pady=10)

# Refresh button to update the standings
refresh_button = tk.Button(root, text="Refresh the standings", command=update_standings)
refresh_button.pack(pady=10)

# Initial table population
update_standings()

# Run the GUI
root.mainloop()
