# Runbook

## How to recover from common failures
- **Invalid API Keys**: Ensure `HERE_API_KEY` and `TOLLGURU_API_KEY` are correctly set in the root `.env` file.
- **Geocoding Failures**: Check address connectivity or ensure the address exists in HERE Maps database.
- **TollGuru API Errors**: Verify your account balance and API plan limits.

## Rollback basics
- This repo contains stateless scripts. Revert code changes via Git if a new update breaks functionality.

## On-call / Logs / Monitoring entry points
- **Logs**: Standard output (stdout) and error (stderr) provide detailed logs of API requests and responses.
- **Output Files**: Check `output.json` for script execution results and `testCases_result.csv` for test outputs.

## Cron jobs / Scheduled jobs
- None configured in this repository.

## Data backfill scripts
- None applicable.
