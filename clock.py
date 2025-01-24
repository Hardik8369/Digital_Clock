import tkinter as tk
from time import strftime
from datetime import datetime
import requests

# Function to get the current location's city using a geolocation API
def get_current_city():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        return data['city']
    except Exception as e:
        return "Unknown Location"

# Function to get the temperature based on the city
def get_temperature(city):
    try:
        api_key = "e12d502fdbc0a174e68aefac471bddcb"  # Replace with your API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            return f"{temp}°C"
        else:
            return "N/A"
    except Exception as e:
        return "Error"

# Update the clock
def update_clock():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d-%m-%Y")
    current_day = now.strftime("%A")
    year = now.year
    temperature = get_temperature(current_city)
    
    # Update labels
    time_label.config(text=current_time)
    date_label.config(text=f"Date: {current_date}")
    day_label.config(text=f"Day: {current_day}")
    year_label.config(text=f"Year: {year}")
    temp_label.config(text=f"Temperature in {current_city}: {temperature}")
    
    # Call the update function after 500 ms (0.5 second)
    root.after(500, update_clock)

# Show welcome screen
def show_welcome():
    splash = tk.Toplevel()
    splash.geometry("600x400")
    splash.configure(bg="#2b2d42")
    splash.title("Welcome Screen")
    
    # Add 3D style welcome text
    welcome_label = tk.Label(
        splash,
        text="Hello, Welcome to Digital Clock!",
        font=("Helvetica", 28, "bold"),
        fg="#edf2f4",
        bg="#2b2d42",
        relief="raised",
        bd=5
    )
    welcome_label.pack(expand=True)
    
    # Automatically close the splash screen after 3 seconds
    splash.after(3000, lambda: (splash.destroy(), start_clock()))

# Start the clock after the welcome screen
def start_clock():
    global root
    root = tk.Tk()
    root.title("Digital Clock with Current Location Temperature")
    root.geometry("500x450")
    root.configure(bg="#2b2d42")  # Background color
    root.resizable(False, False)

    # Create a main frame with border
    frame = tk.Frame(root, bg="#3a3b58", bd=10, relief="ridge")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Add a title
    title_label = tk.Label(frame, text="Digital Clock", font=("Helvetica", 24, "bold"), fg="#8d99ae", bg="#3a3b58")
    title_label.pack(pady=(10, 5))

    # Add labels for time, date, day, year, and temperature
    global time_label, date_label, day_label, year_label, temp_label
    time_label = tk.Label(frame, font=("Helvetica", 48, "bold"), fg="#ef233c", bg="#3a3b58")
    time_label.pack(pady=10)

    date_label = tk.Label(frame, font=("Helvetica", 20), fg="#edf2f4", bg="#3a3b58")
    date_label.pack(pady=(5, 2))

    day_label = tk.Label(frame, font=("Helvetica", 20), fg="#edf2f4", bg="#3a3b58")
    day_label.pack(pady=(2, 2))

    year_label = tk.Label(frame, font=("Helvetica", 20), fg="#edf2f4", bg="#3a3b58")
    year_label.pack(pady=(2, 2))

    temp_label = tk.Label(frame, font=("Helvetica", 20), fg="#ffadad", bg="#3a3b58")
    temp_label.pack(pady=(5, 10))

    # Footer with "Designed by Hardikgowda"
    footer_label = tk.Label(root, text="Designed by Hardikgowda", font=("Helvetica", 12), fg="#edf2f4", bg="#2b2d42")
    footer_label.pack(side="bottom", pady=10)

    # Start the clock
    update_clock()

    # Run the application
    root.mainloop()

# Main program flow
current_city = get_current_city()
main_window = tk.Tk()
main_window.withdraw()  # Hide the main window during splash
show_welcome()  # Show the welcome screen
main_window.mainloop()
