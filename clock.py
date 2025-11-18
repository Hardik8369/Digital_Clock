import tkinter as tk
from datetime import datetime
import requests

# Function to get the current location's city using a geolocation API
def get_current_city():
    try:
        response = requests.get("https://ipinfo.io", timeout=5)
        data = response.json()
        return data.get('city', "Unknown Location")
    except Exception:
        return "Unknown Location"

# Function to get the temperature based on the city
def fetch_temperature(city):
    try:
        api_key = "e12d502fdbc0a174e68aefac471bddcb"  # Replace with your API key
        if city in (None, "", "Unknown Location"):
            return "N/A"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        resp = requests.get(url, timeout=6)
        data = resp.json()
        if resp.status_code == 200 and 'main' in data:
            temp = data['main'].get('temp')
            return f"{temp}°C" if temp is not None else "N/A"
        else:
            return "N/A"
    except Exception:
        return "Error"

# Update the clock every second
def update_clock():
    now = datetime.now()
    time_label.config(text=now.strftime("%H:%M:%S"))
    date_label.config(text=f"Date: {now.strftime('%d-%m-%Y')}")
    day_label.config(text=f"Day: {now.strftime('%A')}")
    year_label.config(text=f"Year: {now.year}")

    # schedule next time update after 1000 ms (1 second)
    root.after(1000, update_clock)

# Update temperature less frequently (every 10 minutes)
def update_temperature():
    temperature = fetch_temperature(current_city)
    temp_label.config(text=f"Temperature in {current_city}: {temperature}")
    # schedule next temperature update after 10 minutes (600000 ms)
    root.after(600_000, update_temperature)

# Show welcome splash screen, then build main UI using the same root
def show_welcome_then_start():
    splash = tk.Toplevel(root)
    splash.geometry("600x400")
    splash.configure(bg="#2b2d42")
    splash.title("Welcome Screen")

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

    # After 3 seconds destroy splash and show main UI (single root)
    def close_splash_and_show():
        splash.destroy()
        build_main_ui()
        root.deiconify()  # show main window (it was withdrawn)

    splash.after(3000, close_splash_and_show)

# Build the main clock UI on the single root
def build_main_ui():
    root.title("Digital Clock with Current Location Temperature")
    root.geometry("500x450")
    root.configure(bg="#2b2d42")
    root.resizable(False, False)

    frame = tk.Frame(root, bg="#3a3b58", bd=10, relief="ridge")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    title_label = tk.Label(frame, text="Digital Clock", font=("Helvetica", 24, "bold"), fg="#8d99ae", bg="#3a3b58")
    title_label.pack(pady=(10, 5))

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

    footer_label = tk.Label(root, text="Designed by Hardikgowda", font=("Helvetica", 12), fg="#edf2f4", bg="#2b2d42")
    footer_label.pack(side="bottom", pady=10)

    # Start the periodic updates
    update_clock()
    update_temperature()

# --- Main program flow ---
root = tk.Tk()
root.withdraw()  # hide initial root while splash shows

current_city = get_current_city()

# show splash and then the main UI on the same root
show_welcome_then_start()

# single mainloop call only
root.mainloop()
