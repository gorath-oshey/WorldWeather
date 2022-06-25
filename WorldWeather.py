from tkinter import ttk
from ttkthemes import ThemedTk
import requests
from tkinter import messagebox
import time

API_KEY = "69cd5afc0c4327b30e7dc959a9891d81"
API_URL = "http://api.openweathermap.org/data/2.5/weather"


def change_lang(event):
    if lang_select.get() == "EN":
        button["text"] = "What weather?"
    else:
        button["text"] = "Яка погода?"


def print_weather(weather):
    try:
        city = weather["name"]
        country = weather["sys"]["country"]
        temp = weather["main"]["temp"]
        pressure = weather["main"]["pressure"]
        humidity = weather["main"]["humidity"]
        wind = weather["wind"]["speed"]
        desc = weather["weather"][0]["description"]
        sunrise_ts = weather["sys"]["sunrise"]
        sunset_ts = weather["sys"]["sunset"]
        sunrise_struct_time = time.localtime(sunrise_ts)
        sunset_struct_time = time.localtime(sunset_ts)
        sunrise = time.strftime("%H:%M:%S", sunrise_struct_time)
        sunset = time.strftime("%H:%M:%S", sunset_struct_time)
        if params["lang"] == "ua":
            return f"Місто: {city}, {country} \nТемпература: {temp} °C \nАтмосферний тиск: {pressure} гПа \nВологість: {humidity} % \nШвидкість вітру: {wind} м/с \nПогодні умови: {desc} \nСхід сонця: {sunrise} \nЗахід сонця: {sunset}"
        else:
            return f"Location: {city}, {country} \nTemperature: {temp} °C \nPressure: {pressure} Pa \nHumidity: {humidity} % \nWind speed: {wind} m/s \nWeather: {desc} \nSunrise: {sunrise} \nSunset: {sunset}"
    except:
        if params["lang"] == "ua":
            return "Помилка отримання даних..."
        else:
            return "Error with geting information about weather..."


def get_weather(event=""):
    if not entry.get():
        messagebox.showwarning(
            "Warning", "Enter request in such format: city, country_code")
    else:
        global params
        params = {
            "appid": API_KEY,
            "q": entry.get(),
            "units": "metric",
            "lang": "ua"
        }
        if lang_select.get() == "EN":
            params["lang"] = "en"
        else:
            params["lang"] = "ua"
        r = requests.get(API_URL, params=params)
        weather = r.json()
        label["text"] = print_weather(weather)


root = ThemedTk(theme="arc")
root.geometry("500x400+800+300")
root.resizable(False, False)

styles = ttk.Style()
styles.configure("TLabel", padding=5, font="Arial 11")

lang_frame = ttk.Frame(root)
lang_frame.place(relx=0.9, rely=0.12, relwidth=0.1, relheight=0.066, anchor="s")

lang_select = ttk.Combobox(lang_frame, values=["UA", "EN"])
lang_select.pack()
lang_select.current(0)

top_frame = ttk.Frame(root)
top_frame.place(relx=0.5, rely=0.15, relwidth=0.9, relheight=0.1, anchor="n")

entry = ttk.Entry(top_frame)
entry.place(relwidth=0.7, relheight=1)

button = ttk.Button(top_frame, text="Яка погода?", command=get_weather)
button.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = ttk.Frame(root)
lower_frame.place(relx=0.5, rely=0.35, relwidth=0.9, relheight=0.6, anchor="n")

label = ttk.Label(lower_frame, anchor="nw")
label.place(relwidth=1, relheight=1)

entry.bind("<Return>", get_weather)
lang_select.bind("<<ComboboxSelected>>", change_lang)

root.mainloop()
