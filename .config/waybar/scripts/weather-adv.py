#!/usr/bin/env python

import json
from typing import Any
import requests
from datetime import datetime

WEATHER_CODES = {
    "113": "<span color=\"#f6c177\"> </span>",
    "116": "<span color=\"#ea9a97\"> </span>",
    "119": "<span color=\"#908caa\"> </span>",
    "122": "<span color=\"#908caa\"> </span>",
    "143": "<span color=\"#908caa\">敖 </span>",
    "176": "<span color=\"#8EB6F5\"> </span>",
    "179": "<span color=\"#8EB6F5\">🌧 </span>",
    "182": "<span color=\"#8EB6F5\">🌧 </span>",
    "185": "<span color=\"#8EB6F5\">🌧 </span>",
    "200": "<span color=\"#8EB6F5\">⛈ </span>",
    "227": "<span color=\"#8EB6F5\">🌨 </span>",
    "230": "<span color=\"#bcd3f8\">❄️ </span>",
    "248": "<span color=\"#908caa\">敖 </span>",
    "260": "<span color=\"#908caa\">敖 </span>",
    "263": "<span color=\"#ea9a97\">敖 </span>",
    "266": "<span color=\"#ea9a97\">🌦 </span>",
    "281": "<span color=\"#8EB6F5\">🌧 </span>",
    "284": "<span color=\"#8EB6F5\">🌧 </span>",
    "293": "<span color=\"#ea9a97\"> </span>",
    "296": "<span color=\"#ea9a97\"> </span>",
    "299": "<span color=\"#8EB6F5\">🌧 </span>",
    "302": "<span color=\"#8EB6F5\">🌧 </span>",
    "305": "<span color=\"#8EB6F5\">🌧 </span>",
    "308": "<span color=\"#8EB6F5\">🌧 </span>",
    "311": "<span color=\"#8EB6F5\">🌧 </span>",
    "314": "<span color=\"#8EB6F5\">🌧 </span>",
    "317": "<span color=\"#8EB6F5\">🌧 </span>",
    "320": "<span color=\"#8EB6F5\">🌨 </span>",
    "323": "<span color=\"#8EB6F5\">🌨 </span>",
    "326": "<span color=\"#8EB6F5\">🌨 </span>",
    "329": "<span color=\"#bcd3f8\">❄️ </span>",
    "332": "<span color=\"#bcd3f8\">❄️ </span>",
    "335": "<span color=\"#bcd3f8\">❄️ </span>",
    "338": "<span color=\"#bcd3f8\">❄️ </span>",
    "350": "<span color=\"#8EB6F5\">🌧 </span>",
    "353": "<span color=\"#ea9a97\"> </span>",
    "356": "<span color=\"#8EB6F5\">🌧 </span>",
    "359": "<span color=\"#8EB6F5\">🌧 </span>",
    "362": "<span color=\"#8EB6F5\">🌧 </span>",
    "365": "<span color=\"#8EB6F5\">🌧 </span>",
    "368": "<span color=\"#8EB6F5\">🌨 </span>",
    "371": "<span color=\"#bcd3f8\">❄️ </span>",
    "374": "<span color=\"#8EB6F5\">🌧 </span>",
    "377": "<span color=\"#8EB6F5\">🌧 </span>",
    "386": "<span color=\"#8EB6F5\">⛈ </span>",
    "389": "<span color=\"#eb6f92\">朗 </span>",
    "392": "<span color=\"#eb6f92\">ﭼ </span>",
    "395": "<span color=\"#bcd3f8\">❄️ </span>",
}

data = {}
weather = requests.get("https://wttr.in/?format=j1").json()


def format_time(time: str) -> str:
    return time.replace("00", "").zfill(2)


def format_temp(temp: str) -> str:
    return (hour["FeelsLikeF"] + "°").ljust(3)


def format_chances(hour: dict[str, Any]) -> str:
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind",
    }

    conditions: list[str] = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event] + " " + hour[event] + "%")
    return ", ".join(conditions)


def get_skip_conditions(tm: int, idx: int) -> bool:
    if tm < 6:
        return True
    return False

data["text"] = (
    WEATHER_CODES[weather["current_condition"][0]["weatherCode"]]
    + " "
    + weather["current_condition"][0]["FeelsLikeF"]
    + "°"
)

data[
    "tooltip"
] = f"<b>{weather['current_condition'][0]['weatherDesc'][0]['value']} \
{weather['current_condition'][0]['temp_F']}°</b>\n"
data["tooltip"] += f"Feels like: {weather['current_condition'][0]['FeelsLikeF']}°\n"
data["tooltip"] += f"Wind: {weather['current_condition'][0]['windspeedMiles']}mph\n"
data["tooltip"] += f"Humidity: {weather['current_condition'][0]['humidity']}%\n"

pfxcol = "#393552"
for i, day in enumerate(weather["weather"]):
    data["tooltip"] += f"\n<b>"
    if i == 0:
        data["tooltip"] += "Today, "
    if i == 1:
        data["tooltip"] += "Tomorrow, "
    data["tooltip"] += f"{day['date']}</b>\n"
    data["tooltip"] += f"<i><b>{day['maxtempF']}° {day['mintempF']}°</b>  / "
    data[
        "tooltip"
    ] += f"<span color=\"#f6c177cc\">盛 {day['astronomy'][0]['sunrise']}</span>  \
<span color=\"#ea9a97cc\"> {day['astronomy'][0]['sunset']}</span></i>\n"

    for hour in day["hourly"]:
        now = int(format_time(hour["time"]))
        if i == 0 and datetime.now().hour - 2 < now and datetime.now().hour + 2 > now:
            pfxcol = "#9ccfd8"
        if get_skip_conditions(tm=int(format_time(hour["time"])), idx=i):
            continue

        pfx = f"<span color=\"{pfxcol}\"></span>"
        data[
            "tooltip"
        ] += f"<b>{pfx} {format_time(hour['time'])}</b> | \
{WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeF'])} | \
{hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"
        pfxcol = "#393552"


print(json.dumps(data))
