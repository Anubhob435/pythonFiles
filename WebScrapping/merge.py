import csv
import json
import logging
import re
from pathlib import Path
from typing import Any


logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("merge_profiles")


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_JSON = BASE_DIR / "merged_profiles.json"
OUTPUT_CSV = BASE_DIR / "merged_profiles.csv"


def load_json_array(file_path: Path) -> list[dict[str, Any]]:
	"""Load a JSON file expected to contain a list of objects."""
	try:
		with file_path.open("r", encoding="utf-8") as f:
			data = json.load(f)
		if isinstance(data, list):
			return [item for item in data if isinstance(item, dict)]
		logger.warning("Skipping %s: expected top-level JSON array", file_path.name)
		return []
	except Exception as exc:
		logger.warning("Failed to load %s: %s", file_path.name, exc)
		return []


def normalize_text(value: Any) -> str:
	if value is None:
		return ""
	return re.sub(r"\s+", " ", str(value).strip()).casefold()


def make_record_key(record: dict[str, Any]) -> str:
	"""Create a stable key for deduplication, preferring cds_code."""
	cds_code = normalize_text(record.get("cds_code"))
	if cds_code:
		return f"cds:{cds_code}"

	detail_link = normalize_text(record.get("detail_link"))
	if detail_link:
		return f"link:{detail_link}"

	school_name = normalize_text(record.get("school"))
	return f"name:{school_name}"


def should_replace(existing: dict[str, Any], incoming: dict[str, Any]) -> bool:
	"""Choose the better record when duplicate keys are found."""
	existing_details = existing.get("detailed_info")
	incoming_details = incoming.get("detailed_info")

	existing_has_details = isinstance(existing_details, dict) and bool(existing_details)
	incoming_has_details = isinstance(incoming_details, dict) and bool(incoming_details)

	if incoming_has_details and not existing_has_details:
		return True

	# Prefer records without an error marker.
	existing_error = bool(existing.get("error"))
	incoming_error = bool(incoming.get("error"))
	if existing_error and not incoming_error:
		return True

	if incoming_has_details and incoming_error is False:
		# If both have details, keep incoming to preserve potential newer retry data.
		return True

	return False


def flatten_for_csv(data: Any, prefix: str = "") -> dict[str, Any]:
	"""Flatten nested dicts/lists so each row can be written to CSV."""
	flat: dict[str, Any] = {}

	if isinstance(data, dict):
		for key, value in data.items():
			key_name = f"{prefix}.{key}" if prefix else str(key)
			flat.update(flatten_for_csv(value, key_name))
	elif isinstance(data, list):
		# Keep lists as JSON strings to preserve structure in CSV.
		flat[prefix] = json.dumps(data, ensure_ascii=False)
	else:
		flat[prefix] = data

	return flat


def pick_retry_file(base_dir: Path) -> Path | None:
	"""Support both retried.json and retryied.json filenames."""
	preferred = base_dir / "retried.json"
	typo_name = base_dir / "retryied.json"

	if preferred.exists():
		return preferred
	if typo_name.exists():
		return typo_name
	return None


def main() -> None:
	profile_files = sorted(base_dir_file for base_dir_file in BASE_DIR.glob("profile_data_*.json"))
	retry_file = pick_retry_file(BASE_DIR)

	if not profile_files:
		logger.error("No profile_data_*.json files found in %s", BASE_DIR)
		return

	logger.info("Found %d profile data files", len(profile_files))
	if retry_file:
		logger.info("Using retry file: %s", retry_file.name)
	else:
		logger.warning("Retry file not found (checked retried.json and retryied.json)")

	merged: dict[str, dict[str, Any]] = {}

	# Load all profile_data files first.
	for file_path in profile_files:
		records = load_json_array(file_path)
		logger.info("Loaded %d records from %s", len(records), file_path.name)
		for record in records:
			key = make_record_key(record)
			if key not in merged:
				merged[key] = record
			elif should_replace(merged[key], record):
				merged[key] = record

	# Overlay retry records so successful retries can replace failed originals.
	if retry_file:
		retry_records = load_json_array(retry_file)
		logger.info("Loaded %d records from %s", len(retry_records), retry_file.name)
		for record in retry_records:
			key = make_record_key(record)
			if key not in merged or should_replace(merged[key], record):
				merged[key] = record

	merged_records = list(merged.values())

	with OUTPUT_JSON.open("w", encoding="utf-8") as f:
		json.dump(merged_records, f, indent=2, ensure_ascii=False)
	logger.info("Wrote merged JSON: %s (%d records)", OUTPUT_JSON.name, len(merged_records))

	flattened_rows = [flatten_for_csv(record) for record in merged_records]
	headers = sorted({key for row in flattened_rows for key in row.keys()})

	with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
		writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
		writer.writeheader()
		for row in flattened_rows:
			writer.writerow(row)

	logger.info("Wrote merged CSV: %s (%d rows)", OUTPUT_CSV.name, len(flattened_rows))


if __name__ == "__main__":
	main()
