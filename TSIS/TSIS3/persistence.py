import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "Normal"
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)

    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value

    save_settings(settings)
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []

    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_score(name, score, distance):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:10]

    save_leaderboard(leaderboard)