import json
from pathlib import Path
from collections import defaultdict

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "suggestions_log.json"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_suggestion(query: str, suggestions: list):
    data = defaultdict(lambda: defaultdict(int))

    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            data.update(json.load(f))

    for suggestion in suggestions:
        data[query][suggestion] += 1

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
