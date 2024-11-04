import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# AccuWeather API Key
API_KEY = "<Get API Key from https://developer.accuweather.com/>"

# Function to download and display the weather icons
def download_and_display_icon(icon_number):
    icon_url = f"https://developer.accuweather.com/sites/default/files/{icon_number:02d}-s.png"
    response = requests.get(icon_url)
    image_data = BytesIO(response.content)
    image = Image.open(image_data)
    return ImageTk.PhotoImage(image)

# Function to fetch city key based on city name
def get_city_key(city_name):
    search_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city_name}&details=true"
    response = requests.get(search_url)
    if response.status_code == 200 and response.json():
        return response.json()[0]["Key"]
    else:
        return None

# Function to fetch weather data based on city key
def get_weather_data(city_key):
    weather_url = f'''https://dataservice.accuweather.com/forecasts/v1/daily/5day/{city_key}?apikey={API_KEY}'''
    response = requests.get(weather_url)
    if response.status_code == 200:
        return response.json()["DailyForecasts"]
    else:
        return None

# Function to create a rounded rectangle for cards
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Function to display the weather data
def display_weather(city_name):
    # Clear previous content
    for widget in frame.winfo_children():
        widget.destroy()

    city_key = get_city_key(city_name)
    if city_key:
        weather_data = get_weather_data(city_key)
        if weather_data:
            for i, forecast in enumerate(weather_data):
                date = forecast["Date"].split("T")[0]
                min_temp = forecast["Temperature"]["Minimum"]["Value"]
                max_temp = forecast["Temperature"]["Maximum"]["Value"]
                day_icon_number = forecast["Day"]["Icon"]
                night_icon_number = forecast["Night"]["Icon"]

                day_icon_img = download_and_display_icon(day_icon_number)
                night_icon_img = download_and_display_icon(night_icon_number)

                # Create a card for each day's weather
                card_frame = tk.Frame(frame, bg="#ffffff", bd=0, relief="solid")
                card_frame.grid(row=0, column=i, padx=20, pady=10)
                
                # Display elements inside the card
                tk.Label(card_frame, text=f"{date}", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)
                tk.Label(card_frame, text=f"{min_temp}°F - {max_temp}°F", font=("Helvetica", 12), bg="#ffffff", fg="#34495e").pack()
                tk.Label(card_frame, image=day_icon_img, bg="#ffffff").pack(pady=10)
                tk.Label(card_frame, image=night_icon_img, bg="#ffffff").pack(pady=10)
                
                # Maintain references to avoid garbage collection
                card_frame.day_icon = day_icon_img
                card_frame.night_icon = night_icon_img
        else:
            error_label.config(text="Error fetching weather data.")
    else:
        error_label.config(text="City not found. Please try again.")

# Function to handle the city search
def search_city():
    city_name = city_entry.get().strip()
    if city_name:
        display_weather(city_name)
    else:
        error_label.config(text="Please enter a city name.")

# Create the main window
root = tk.Tk()
root.title("5-Day Weather Forecast")

# Set the window size and background color
root.geometry("900x400")
root.configure(bg="#ecf0f1")

# Create a frame to hold the input field and button
input_frame = tk.Frame(root, bg="#2c3e50", padx=10, 
                     pady=10, relief="flat", bd=5)
input_frame.grid(row=0, column=0, pady=20, padx=20)

# Create input field for city name
city_label = tk.Label(input_frame, text="Enter City Name:", 
font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1")
city_label.grid(row=0, column=0, padx=10, pady=5)
city_entry = tk.Entry(input_frame, width=25, font=
        ("Helvetica", 14), relief="flat", bd=2)
city_entry.grid(row=0, column=1, padx=10, pady=5)

# Create a search button
search_button = tk.Button(input_frame, text="Search", 
command=search_city, font=("Helvetica", 14), bg="#e74c3c", 
fg="#ffffff", relief="flat", bd=2)
search_button.grid(row=0, column=2, padx=10, pady=5)

# Create a frame to hold the weather data
frame = tk.Frame(root, bg="#ecf0f1", padx=10, pady=10)
frame.grid(row=1, column=0, padx=20, pady=20)

# Create an error label
error_label = tk.Label(root, text="", foreground="red", bg="#ecf0f1", font=("Helvetica", 12))
error_label.grid(row=2, column=0, padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
