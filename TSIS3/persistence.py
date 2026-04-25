import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings_path = os.path.join(BASE_DIR, "settings.json")
leaderboard_path = os.path.join(BASE_DIR, "leaderboard.json")


def load_leaderboard():
    if not os.path.exists(leaderboard_path):
        return []

    with open(leaderboard_path, "r") as f:
        return json.load(f)


def save_score(name, score, distance):
    data = load_leaderboard()

    data.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(leaderboard_path, "w") as f:
        json.dump(data, f, indent=4)

def load_settings():
    path = os.path.join(BASE_DIR, "settings.json")
    if not os.path.exists(path):
        return {"sound": True, "color": "blue", "difficulty": "normal"}

    with open(path, "r") as f:
        return json.load(f)


def save_settings(settings):
    path = os.path.join(BASE_DIR, "settings.json")
    with open(path, "w") as f:
        json.dump(settings, f, indent=4)