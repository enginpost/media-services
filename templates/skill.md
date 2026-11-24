---
name: streaming-recommender
description: Recommend movies/TV on your streaming subscriptions.
---

# Streaming Recommender

## When to Use
Use when user wants movie or TV recommendations constrained to streaming services they subscribe to, or wants "what's new" on those services.

## Interview Flow
When user requests a recommendation, interview with options from `scripts/media-services/config/search_options.json`. Use `clarify` for questions with ≤4 options. For long lists >4 options, present a numbered list in an open-ended clarify question and have user reply with the number. Map number → value via search_options.json.

Interview steps:
1. Format
2. Genre
3. Decade
4. Runtime
5. Mood
6. Final open-ended question: "Any preferences?"

The preferences question is post-criteria and not used for TMDB query. After results are fetched, examine each result's description and poster context to see if the preference applies. If preference matches description text or visual cues in poster, boost those items to top of results. Preference is a soft filter/rank, not a hard query constraint.

Trigger interview on phrases like "I need a media recommendation" or "Lets start over" while using the skill. Interview should reload options and restart the flow.

Pitfall: `clarify` is limited to 4 choices per question and 5 questions per call. Do not attempt to present 19 genres as choices. Use numbered list + open-ended clarify instead.

## Behavior
1. Load subscriptions from `scripts/media-services/config/subscriptions.json`. If missing, prompt user for list and save.
2. Load TMDB read access token from `scripts/media-services/config/tmdb_read_token.txt`. If missing, prompt user to provide one and save.
3. Load options from `scripts/media-services/config/search_options.json` for interview.
4. For recommendation requests using TMDB v4 read access token:
   - Auth: send `Authorization: Bearer <token>` header. Token works for both v3 read endpoints and v4 endpoints. Do not use v4 /4/account for app token; use v3 /3/movie /3/discover endpoints with Bearer auth.
   - Mood/genre: call `GET https://api.themoviedb.org/3/discover/movie?...` with Bearer auth, then filter results to titles where `watch/providers` includes any of user's services.
   - What's new/trending: fetch TMDB trending or discover with `primary_release_date.gte` last N days, filter by providers.
5. Presentation:
   - Default to no more than 5 results per recommendation. Show up to 5, fewer if criteria limits results.
   - Show as markdown table with 2 columns: Poster | Details.
   - Poster column: TMDB image `w154` thumbnail.
   - Details column: **Movie name (runtime in parenthesis)** on first line, then line break and description below.
   - If user asks for more, fetch next page and append. Never return >20 items without pagination.
   - Include provider info: flatrate vs rent/buy, and highlight matches to user's subscriptions.
6. Selection view:
   - When user says "show me..." or "Tell me about..." an item, present a detailed selection table with columns: Poster | Info | Subscriptions | Free | Rent/Buy.
   - Poster: TMDB `w154` thumbnail.
   - Info: **Name (runtime)** line break + description.
   - Subscriptions: unordered list of services available as flatrate. Do not show provider IDs and do not remind user they have the service.
   - Free: unordered list of free/ad-supported services with note e.g., "Kanopy: free with participating library". Do not show provider IDs.
   - Rent/Buy: unordered list of services.
7. Config files live under `scripts/media-services/config/` and are gitignored. Templates live under `scripts/media-services/templates/`. Code must never read config from skill root.
8. Fallback: if no TMDB token, use web_search for "[service] new movies [month]" and aggregate.
9. Output concise list with title, year, genre, service(s) available, and one-line why.
6. Config files live under `scripts/media-services/config/` and are gitignored. Templates live under `scripts/media-services/templates/`. Code must never read config from skill root.
7. Fallback: if no TMDB token, use web_search for "[service] new movies [month]" and aggregate.
8. Output concise list with title, year, genre, service(s) available, and one-line why.

## Project layout
Skill root contains SKILL.md only. All code, config, templates live under `scripts/media-services/`:

```
scripts/media-services/
  config/               # gitignored runtime files
    subscriptions.json
    tmdb_read_token.txt
    search_options.json
  templates/           # template files for config
  scripts/             # helper scripts
  README.md
```

Pitfall: config must stay under `scripts/media-services/config/`. Moving config to skill root breaks the skill's self-contained design and causes duplicate files.

Code must find config via `scripts/media-services/config/`, not skill root.

## Config files
- `scripts/media-services/config/subscriptions.json` → {"services": ["netflix","prime_video",...]}
- `scripts/media-services/config/tmdb_read_token.txt` → TMDB v4 read access token
- `scripts/media-services/config/search_options.json` → genres, decades, moods for dropdowns

See `references/tmdb-auth.md` for authentication details and endpoint notes.

Git: `scripts/media-services/` is a git repo. `config/*` is gitignored. Commit templates, README, scripts only.

## Provider mapping
Maintain mapping TMDB provider IDs:
netflix=8, prime_video=9, disney_plus=337, hbo_max=384, hulu=15, paramount_plus=531, apple_tv=350, plex=... etc.

Pitfall: TMDB watch/providers returns `flatrate`, `rent`, `buy`, `free`. Flatrate means subscription streaming; rent/buy are pay-per-title. Filter accordingly when user wants free-with-subscription.

## Commands
- `streaming-recommender recommend --mood "cozy thriller" --limit 5`
- `streaming-recommender new --days 30`
- `streaming-recommender set-subscriptions`

Respect user's preference for concise responses.