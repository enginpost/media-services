#!/usr/bin/env python3
"""
Interview helper for streaming recommender.
Reads search_options.json and prints structured options for UI presentation.
"""
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).parent.parent / "config"
OPTIONS_FILE = BASE / "search_options.json"

def load_options():
    if not OPTIONS_FILE.exists():
        print(json.dumps({"error": "options file missing"}))
        sys.exit(1)
    data = json.loads(OPTIONS_FILE.read_text())
    # Format for presentation
    genres = [g["name"] for g in data.get("genres", [])]
    decades = [d["label"] for d in data.get("decades", [])]
    moods = data.get("moods", [])
    return {
        "genres": genres,
        "decades": decades,
        "moods": moods
    }

if __name__ == "__main__":
    opts = load_options()
    print(json.dumps(opts, indent=2))
