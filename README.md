# TollTally - Toll for Route (HERE Maps)

This repository provides examples and tools to extend the mapping capabilities of **HERE Maps** by adding toll information from [**TollGuru**](https://tollguru.com/) to the route information.

## Architecture
- **Multi-language support**: Implementations available in JavaScript, Python, and Ruby.
- **Root Configuration**: Centralized `.env` file at the root level shared across all implementations.
- **Routing Integration**: Geocodes addresses and fetches route polylines/actions using HERE Maps Routing API (v8).
- **Toll Calculation**: Integrates with TollGuru's `complete-polyline-from-mapping-service` endpoint.
- **Time-aware Tolls**: Automatically generates `locTimes` from HERE Maps route metadata for accurate time-based toll rates.
- **Flexible Polyline Support**: Handles HERE Maps specific flex-polyline encoding/decoding.
- **Standardized I/O**: Uses `input.json` for requests and `output.json` for results across all languages.
- **Detailed Docs**: See [Architecture](docs/architecture.md) for more details on services and datastores.

## Prerequisites
- API Keys:
  - **TollGuru API Key**: [Get it here](https://tollguru.com/developers/get-api-key)
  - **HERE Maps API Key**: [Get it here](https://developer.here.com/)
- Runtimes:
  - Node.js (for JavaScript)
  - Python 3.x (for Python)
  - Ruby (for Ruby)

## Local Setup
1. Clone the repository.
2. Create a `.env` file in the **root directory**:
   ```bash
   TOLLGURU_API_KEY=your_tollguru_api_key_here
   HERE_API_KEY=your_here_maps_api_key_here
   ```
3. Install dependencies for your preferred language:
   - **JavaScript**: `cd javascript && npm install`
   - **Python**: `cd python && pip install -r requirements.txt`
   - **Ruby**: `cd ruby && bundle install`

## How to Run Tests
Each language folder contains its own testing suite:
- **JavaScript**: Run `node index.js` (uses `input.json`).
- **Python**: Run `python Testing/Test_Here_Maps.py`.
- **Ruby**: Run `ruby TestCases/test_ruby.rb`.

## How to Deploy
These scripts are intended for integration into larger applications or as standalone utilities. To deploy:
1. Ensure API keys are provided via environment variables.
2. Integrate the language-specific logic into your backend service.

## Configuration
- **Location**: Root `.env` file for API keys.
- **Runtime Config**: `javascript/input.json` (for JS) or language-specific test CSVs.

## Known Limitations
- Requires active API keys for both HERE Maps and TollGuru.
- Dependent on HERE Maps Routing API v8 response structure.

## Product Features
Support for [geographies](https://github.com/mapup/tollguru_country_coverage/wiki/Countries-supported-by-TollGuru), [vehicle types](https://github.com/mapup/tollguru_vehicle_coverage/wiki/Vehicle-types-supported-by-TollGuru), and [payment options](https://tollguru.com/developers/features).

---
### Documentation
- [Architecture Details](docs/architecture.md)
- [Runbook / Operations](docs/runbook.md)
