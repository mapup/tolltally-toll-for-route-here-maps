# Architecture Overview

## Major Services
- **HERE Maps API**: Used for geocoding addresses and calculating route polylines/actions.
- **TollGuru API**: Used for calculating toll costs based on the route polyline and vehicle parameters.

## Datastore Choices
- **Filesystem**: Input configuration is read from `input.json`, and results are written to `output.json`.
- **CSV**: Test cases and results are managed via `testCases.csv` in the language-specific testing folders.

## Queues/Jobs
- Not applicable. This project consists of synchronous client-side scripts.

## Third-party Dependencies
- See `package.json` (JavaScript), `requirements.txt` (Python), and `Gemfile` (Ruby).

## Auth Model
- **API Key Authentication**: Uses `HERE_API_KEY` and `TOLLGURU_API_KEY` loaded from a root `.env` file.

## Tenancy Model
- Not applicable.
