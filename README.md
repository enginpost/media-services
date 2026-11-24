# media-services

Streaming recommender code and assets for the `streaming-recommender` Hermes skill.

## Structure

```
media-services/
  config/               # Runtime config, gitignored
    subscriptions.json
    tmdb_read_token.txt
    search_options.json
  templates/            # Template files for config
    subscriptions.json.template
    tmdb_read_token.txt.template
    search_options.json.template
  scripts/              # Helper scripts
  README.md
```

## Setup

Config files are gitignored. Use the templates to bootstrap them:

1. Ensure `config/` exists
2. Copy templates into config:
   ```bash
   cp templates/subscriptions.json.template config/subscriptions.json
   cp templates/tmdb_read_token.txt.template config/tmdb_read_token.txt
   cp templates/search_options.json.template config/search_options.json
   ```
3. Edit `config/subscriptions.json` with your streaming services
4. Add your TMDB v4 read access token to `config/tmdb_read_token.txt` — one line, no extra formatting
5. Edit `config/search_options.json` to customize genres, decades, moods, formats, runtimes, preferences

The skill reads from `scripts/media-services/config/` at runtime.

## Templates

Templates provide a safe starting point and stay versioned. They are never committed as live config.

* `subscriptions.json.template` — example services list
* `tmdb_read_token.txt.template` — placeholder for token
* `search_options.json.template` — genres, decades, moods, formats, runtimes, preferences

If you reset config, re-copy from templates.

## Git

Config files are ignored via `.gitignore`. Only commit templates, code, and documentation.

```bash
git add templates README.md .gitignore
git commit -m "update"
git push
```
