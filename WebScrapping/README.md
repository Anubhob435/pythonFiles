# WebScrapping

Simple Python scrapers for California CDE school directory pages.

## Files
- `ultimate_script_1.py`: Scrapes basic school list data into `schools_basic_data.json`.
- `ultimate_script_2.py`: Fetches detailed school profiles in parallel and saves `profile_data_1.json` to `profile_data_10.json`.
- `ultimate retry.py`: Retries failed schools and saves output to `retryied.json`.
- `merge.py`: Merges all profile JSON files (+ retry file) into `merged_profiles.json` and `merged_profiles.csv`.
- `ultimate_script_complete.py`: End-to-end script (list + details + JSON/CSV export in one run).

## Quick Run
From the `WebScrapping` folder:

```powershell
python .\ultimate_script_complete.py --list-url "https://www.cde.ca.gov/SchoolDirectory/certified-nonpublic-schools/0/1/500"
```

Output files:
- `complete_school_data.json`
- `complete_school_data.csv`
