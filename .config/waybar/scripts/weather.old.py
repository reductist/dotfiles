#!/usr/bin/env python

import argparse
import json
from datetime import datetime
from sys import exit as sysexit
from typing import Any

import requests

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument(
    "--zip",
    help="zip code",
    type=str,
    default="0",
    required=False,
)
args = parser.parse_args()

if not args.zip:
    args.zip = "0"

WEATHER_CODES = {
    "113": {
        "day": "<span color=\"#f6c177\">  </span>",
        "night": "<span color=\"#ebbcba\">  </span>",
    },
    "116": {
        "day": "<span color=\"#ea9a97\">  </span>",
        "night": "<span color=\"#ebbcba\">  </span>",
    },
    "119": {
        "day": "<span color=\"#908caa\">  </span>",
		"night": "<span color=\"#908caa\">  </span>",
	},
    "122": {
        "day": "<span color=\"#908caa\">  </span>",
		"night": "",
	},
    "143": {
        "day": "<span color=\"#908caa\"> 敖 </span>",
		"night": "<span color=\"#908caa\"> 敖 </span>",
	},
    "176": {
        "day": "<span color=\"#8EB6F5\">  </span>",
		"night": "",
	},
    "179": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "182": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "185": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "200": {
		"day": "<span color=\"#8EB6F5\"> ⛈ </span>",
		"night": "",
	},
    "227": {
		"day": "<span color=\"#8EB6F5\">🌨 </span>",
		"night": "",
	},
    "230": {
		"day": "<span color=\"#bcd3f8\"> ❄️ </span>",
		"night": "",
	},
    "248": {
		"day": "<span color=\"#908caa\"> 敖 </span>",
		"night": "",
	},
    "260": {
		"day": "<span color=\"#908caa\"> 敖 </span>",
		"night": "",
	},
    "263": {
		"day": "<span color=\"#ea9a97\"> 敖 </span>",
		"night": "",
	},
    "266": {
		"day": "<span color=\"#ea9a97\"> 🌦 </span>",
		"night": "",
	},
    "281": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "284": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "293": {
		"day": "<span color=\"#ea9a97\">  </span>",
		"night": "",
	},
    "296": {
		"day": "<span color=\"#ea9a97\">  </span>",
		"night": "",
	},
    "299": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "302": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "305": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "308": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "311": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "314": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "317": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "320": {
		"day": "<span color=\"#8EB6F5\"> 🌨</span>",
		"night": "",
	},
    "323": {
		"day": "<span color=\"#8EB6F5\"> 🌨</span>",
		"night": "",
	},
    "326": {
		"day": "<span color=\"#8EB6F5\"> 🌨</span>",
		"night": "",
	},
    "329": {
		"day": "<span color=\"#bcd3f8\"> ❄️ </span>",
		"night": "",
	},
    "332": {
		"day": "<span color=\"#bcd3f8\"> ❄️ </span>",
		"night": "",
	},
    "335": {
		"day": "<span color=\"#bcd3f8\"> ❄️ </span>",
		"night": "",
	},
    "338": {
		"day": "<span color=\"#bcd3f8\"> ❄️ </span>",
		"night": "",
	},
    "350": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "353": {
		"day": "<span color=\"#ea9a97\">  </span>",
		"night": "",
	},
    "356": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "359": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "362": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "365": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "368": {
		"day": "<span color=\"#8EB6F5\">🌨 </span>",
		"night": "",
	},
    "371": {
		"day": "<span color=\"#bcd3f8\"> ❄️ </span>",
		"night": "",
	},
    "374": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "377": {
		"day": "<span color=\"#8EB6F5\">🌧</span>",
		"night": "",
	},
    "386": {
		"day": "<span color=\"#8EB6F5\"> ⛈ </span>",
		"night": "",
	},
    "389": {
		"day": "<span color=\"#eb6f92\"> 朗 </span>",
		"night": "",
	},
    "392": {
		"day": "<span color=\"#eb6f92\"> ﭼ </span>",
		"night": "",
	},
    "395": {
		"day": "<span color=\"#bcd3f8\"> ❄️ </span>",
		"night": "",
    },
}

def make_url(args: argparse.Namespace) -> str:
    base = "https://wttr.in/"
    match args.zip:
        case zip if args.zip != "0":
            q = f"{zip}?format=j1"
        case _:
            q = "?format=j1"
    return f"{base}{q}"

def format_time(time: str) -> str:
    return time.replace("00", "").zfill(2)


def format_temp(hour: dict[str, Any]) -> str:
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

def format_rain(hour: dict[str, Any]) -> str:
    if (pct := int(hour["chanceofrain"])) > 0:
        return f"({pct}% rain)"
    return ""

def get_skip_conditions(tm: int) -> bool:
    if tm < 6:
        return True
    return False

def get_by_path(root: dict[str, dict | list] | list, items: list[str]) -> str:
    """Access a nested object in root by item sequence."""
    if len(items) == 1 and items[0] in root:
        if isinstance(root, dict) and items[0] in root:
            return f"{root[items[0]]}"
        else:
            return root[0] # type: ignore
    if len(items) == 0 and isinstance(root, str):
        return root
    if len(items) == 0:
        return ""
    _d = {}
    _i = items
    if isinstance(root, dict) and items[0] in root:
        _d = root[items[0]]
        _i = items[1:]
    if isinstance(root, list):
        _d = root[0] # type: ignore
    return get_by_path(_d, _i)

def make_text(weather: dict[str, Any]) -> str:
    dttm = datetime.strptime(
        weather["current_condition"][0]["localObsDateTime"],
        "%Y-%m-%d %I:%M %p",
    )
    tod = "day" if dttm.hour <= 16 else "night"
    code: str = get_by_path(weather, ["current_condition", "weatherCode"])
    sym = WEATHER_CODES[code][tod]
    if sym == "":
        sym = WEATHER_CODES[code]["day"]
    temp = f'{get_by_path(weather, ["current_condition", "FeelsLikeF"])}°'
    return f" {sym.removesuffix('</span>')} {temp}</span>"

def make_tooltip(weather: dict[str, dict | list]) -> str:
    desc = f'{get_by_path(weather, ["current_condition", "weatherDesc", "value"])}'
    feels = f'Feels like: {get_by_path(weather, ["current_condition", "FeelsLikeF"])}°'
    wind = f'Wind: {get_by_path(weather, ["current_condition", "windspeedMiles"])}mph'
    hum = f'Humidity: {get_by_path(weather, ["current_condition", "humidity"])}%'
    len_max = max([len(el) for el in (feels, wind, hum)])
    pads = [
        (len_max - len(el) + 1) * " "
        for el in (feels, wind, hum)
    ]
    padded = [pads[i].join(s.rsplit(" ", 1)) for i,s in enumerate((feels, wind, hum))]
    desc_fmt = f"<b>{desc}</b>"
    feels_fmt, wind_fmt, hum_fmt = padded
    return (
        f"{desc_fmt} \n" +
        f"{feels_fmt} \n" +
        f"{wind_fmt} \n" +
        f"{hum_fmt}\n"
    )

def format_weathercode(hour: dict[str, Any]) -> str:
    code = hour["weatherCode"]
    symbols = WEATHER_CODES[code]
    if int(format_time(hour["time"])) <= 18:
        sym = symbols["day"]
    else:
        sym = symbols["night"]
        if sym == "":
            sym = symbols["day"]
    return sym.removesuffix('</span>')


weather = requests.get(f"{make_url(args)}").json()
data = {}
data["text"] = make_text(weather)

# data[
#     "tooltip"
# ] = f"<b>{weather['current_condition'][0]['weatherDesc'][0]['value']} \
# {weather['current_condition'][0]['temp_F']}°</b>\n"
# data["tooltip"] += f"Feels like: {weather['current_condition'][0]['FeelsLikeF']}°\n"
# data["tooltip"] += f"Wind: {weather['current_condition'][0]['windspeedMiles']}mph\n"
# data["tooltip"] += f"Humidity: {weather['current_condition'][0]['humidity']}%\n"

data["tooltip"] = make_tooltip(weather)

def make_header(i, date: str) -> str:
    if i == 0:
        return f"\n<b>Today, {date}</b>\n"
    dttm = datetime.strptime(date, "%Y-%m-%d")
    return f"\n<b>{dttm.strftime('%A')}, {date}</b>\n"

def make_hi_lo(day: dict[str, Any]) -> str:
    return f"<i><b>{day['maxtempF']}° {day['mintempF']}°</b>  / "

def make_sunrise_sunset(day: dict[str, Any]) -> str:
    return (
        f"<span color=\"#f6c177cc\">盛 {day['astronomy'][0]['sunrise']}</span> " +
        f"<span color=\"#ea9a97cc\"> {day['astronomy'][0]['sunset']}</span></i>\n"
    )

def make_daily(i: int, day: dict[str, Any]) -> str:
    hdr = make_header(i, day["date"])
    hilo = make_hi_lo(day)
    sunriseset = make_sunrise_sunset(day)
    return (
        hdr +
        hilo +
        sunriseset
    )

def get_marker_hi(i: int, now: int) -> str:
    pfxcol = "#393552"
    if i == 0 and datetime.now().hour - 2 < now and datetime.now().hour + 2 > now:
        pfxcol = "#9ccfd8"
    return pfxcol

def make_hourly(i: int, hour: dict[str, Any]) -> tuple[bool, str]:
    now = int(format_time(hour["time"]))
    skip = get_skip_conditions(now)
    pfx = f"<span color=\"{get_marker_hi(i, now)}\"></span>"
    retstr = (
        f"<b>{pfx} {format_time(hour['time'])}</b> | " +
        f"{format_weathercode(hour)} {format_temp(hour)}</span> | " +
        f"{hour['weatherDesc'][0]['value']} {format_rain(hour)} \n"
    )
    return (skip, retstr)

def main():
    for i, day in enumerate(weather["weather"]):
        data["tooltip"] += make_daily(i, day)
        for hour in day["hourly"]:
            skip, hrstr = make_hourly(i, hour)
            if skip:
                continue
            data['tooltip'] += hrstr

    print(u"{:<20}".format(json.dumps(data)))

if __name__ == '__main__':
    sysexit(main())

#     data["tooltip"] += f"\n<b>"
#     if i == 0:
#        data["tooltip"] += "Today, "
#     else:
#         data["tooltip"] += datetime.strptime(
#             day["date"],
#             "%Y-%m-%d",
#         ).strftime("%A") + ", "
#     data["tooltip"] += f"{day['date']}</b>\n"
#     data["tooltip"] += f"<i><b>{day['maxtempF']}° {day['mintempF']}°</b>  / "
#     data[
#         "tooltip"
#     ] += f"<span color=\"#f6c177cc\">盛 {day['astronomy'][0]['sunrise']}</span>  \
# <span color=\"#ea9a97cc\"> {day['astronomy'][0]['sunset']}</span></i>\n"
#
#     for hour in day["hourly"]:
#         now = int(format_time(hour["time"]))
#         if i == 0 and datetime.now().hour - 2 < now and datetime.now().hour + 2 > now:
#             pfxcol = "#9ccfd8"
#         if get_skip_conditions(tm=int(format_time(hour["time"]))):
#             continue
#
#         pfx = f"<span color=\"{pfxcol}\"></span>"
#         data["tooltip"] += (
#             f"<b>{pfx} {format_time(hour['time'])}</b> | " +
#             f"{format_weathercode(hour)} {format_temp(hour)}</span> | " +
#             f"{hour['weatherDesc'][0]['value']} {format_rain(hour)} \n"
#         )
