import json
import logging
import re
import time
from pathlib import Path

# Reuse robust fetch + parser logic from your existing script
from ultimate_script_2 import fetch_school_details

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("retry_failed_schools")

INPUT_FILE = "schools_basic_data.json"
OUTPUT_FILE = "retryied.json"

FAILED_SCHOOL_NAMES = [
    "San Antonio Christian School",
    "St. George",
    "International Montessori School",
    "Kraft Academy",
    "Orion International Academy",
    "Ontario Christian Elementary",
    "Ahrens Child Care Center",
    "Choices Life Plan Mentoring Program",
    "Arrowhead Christian Academy-Upper School",
    "California University Preparatory Academ",
    "Barton House Playschool",
    "Christ the King Lutheran Childcare Cente",
    "Citrus Valley Christian Academy PSP",
    "Deeper Roots Academy",
    "Needles SDA School",
    "Hunter Academies",
    "NotYourRegularChurch",
    "Hope Center Academy",
]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip()).casefold()


def find_school_record(target_name, schools):
    target_n = norm(target_name)

    # Exact normalized match first
    exact = [s for s in schools if norm(s.get("school", "")) == target_n]
    if exact:
        return exact[0], "exact"

    # Prefix/fuzzy match (handles truncated names from logs)
    fuzzy = []
    for s in schools:
        s_name_n = norm(s.get("school", ""))
        if s_name_n.startswith(target_n) or target_n.startswith(s_name_n):
            fuzzy.append(s)

    if len(fuzzy) == 1:
        return fuzzy[0], "fuzzy"
    if len(fuzzy) > 1:
        logger.warning(f"Multiple matches for '{target_name}', using first: '{fuzzy[0].get('school')}'")
        return fuzzy[0], "fuzzy-multiple"

    return None, "not-found"


def retry_fetch(detail_link, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        details = fetch_school_details(detail_link)
        if details:
            return details, attempt
        wait_s = min(2 * attempt, 8)
        logger.warning(f"Retry attempt {attempt}/{max_attempts} failed. Waiting {wait_s}s...")
        time.sleep(wait_s)
    return None, max_attempts


def main():
    if not Path(INPUT_FILE).exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        schools = json.load(f)

    logger.info(f"Loaded {len(schools)} schools from {INPUT_FILE}")
    logger.info(f"Retry target count: {len(FAILED_SCHOOL_NAMES)}")

    results = []
    success_count = 0
    failed_count = 0
    not_found_count = 0

    for i, failed_name in enumerate(FAILED_SCHOOL_NAMES, start=1):
        school, match_type = find_school_record(failed_name, schools)

        if not school:
            logger.error(f"[{i}/{len(FAILED_SCHOOL_NAMES)}] Not found in input: {failed_name}")
            results.append({
                "requested_name": failed_name,
                "status": "not_found",
                "error": "School not found in schools_basic_data.json",
            })
            not_found_count += 1
            continue

        school_name = school.get("school", failed_name)
        detail_link = school.get("detail_link", "")
        cds_code = school.get("cds_code", "")

        logger.info(f"[{i}/{len(FAILED_SCHOOL_NAMES)}] Retrying: {school_name} ({match_type})")

        if not detail_link:
            logger.warning(f"No detail link: {school_name}")
            results.append({
                **school,
                "requested_name": failed_name,
                "status": "failed",
                "error": "No detail link",
                "detailed_info": {},
            })
            failed_count += 1
            continue

        details, attempts_used = retry_fetch(detail_link, max_attempts=5)
        if details:
            logger.info(f"✓ Success: {school_name} (attempt {attempts_used})")
            results.append({
                **school,
                "requested_name": failed_name,
                "status": "success",
                "attempts_used": attempts_used,
                "detailed_info": details,
            })
            success_count += 1
        else:
            logger.warning(f"✗ Failed after retries: {school_name}")
            results.append({
                **school,
                "requested_name": failed_name,
                "status": "failed",
                "attempts_used": attempts_used,
                "error": "Failed to fetch details after retries",
                "detailed_info": {},
            })
            failed_count += 1

        time.sleep(0.3)  # be polite to server

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info("=" * 70)
    logger.info(f"Saved retry results to: {OUTPUT_FILE}")
    logger.info(f"Success: {success_count} | Failed: {failed_count} | Not found: {not_found_count}")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()