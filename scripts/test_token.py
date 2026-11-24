#!/usr/bin/env python3
"""
Test TMDB v4 read access token.
Reads token from config/tmdb_read_token.txt and makes a simple authenticated request.
"""

import sys
import pathlib
import urllib.request
import urllib.error

BASE = pathlib.Path(__file__).parent.parent / "config"
TOKEN_FILE = BASE / "tmdb_read_token.txt"

def read_token():
    if not TOKEN_FILE.exists():
        print(f"Missing token file: {TOKEN_FILE}", file=sys.stderr)
        sys.exit(1)
    token = TOKEN_FILE.read_text().strip().splitlines()[0].strip()
    if not token or token.startswith("#"):
        print("Token file empty or commented", file=sys.stderr)
        sys.exit(1)
    return token

def main():
    token = read_token()
    url = "https://api.themoviedb.org/3/movie/550"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode()
            print(f"HTTP {resp.status}")
            print(body[:500])
            print("\nToken appears valid")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
