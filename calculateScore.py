import json
from datetime import datetime
def calculate_score(player):
    return player.gold + len(player.animals) * 10 + len(player.food) * 5
def save_score(player_name, score):
    data = {"name": player_name, "score": score, "time": datetime.now().isoformat()}
    try:
        with open("scores.json", "r", encoding="utf-8") as f:
            scores = json.load(f)
    except:
        scores = []

    scores.append(data)

    with open("scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)
