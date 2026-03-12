import argparse
import csv
import json
import logging
import os
import re
import threading
import time
from html.parser import HTMLParser
from pathlib import Path
from queue import Empty, Queue
from typing import Any

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

CHECKPOINT_DIR = "checkpoints_complete"
CHECKPOINT_FILE = "complete_checkpoint.json"
DEFAULT_JSON_OUTPUT = "complete_school_data.json"
DEFAULT_CSV_OUTPUT = "complete_school_data.csv"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("school_scraper_complete.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class SchoolProfileParser(HTMLParser):
    """Parser for extracting detailed school profile data."""

    def __init__(self) -> None:
        super().__init__()
        self.data: dict[str, Any] = {}
        self.current_field: str | None = None
        self.current_text = ""
        self.in_th = False
        self.in_td = False
        self.in_table = False
        self.target_table_found = False
        self.current_td_links: list[dict[str, str]] = []
        self.current_td_divs: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)

        if tag == "table" and "class" in attrs_dict and "table table-bordered small" in attrs_dict.get("class", ""):
            self.in_table = True
            self.target_table_found = True
            return

        if not self.target_table_found:
            return

        if tag == "th" and "details-field-label" in attrs_dict.get("class", ""):
            self.in_th = True
            self.current_text = ""
        elif tag == "td":
            self.in_td = True
            self.current_text = ""
            self.current_td_links = []
            self.current_td_divs = []
        elif tag == "a" and self.in_td:
            href = attrs_dict.get("href", "") or ""
            self.current_td_links.append({"text": "", "href": href})
        elif tag == "div" and self.in_td:
            self.current_td_divs.append({"text": ""})

    def handle_endtag(self, tag: str) -> None:
        if tag == "table" and self.in_table:
            self.in_table = False
            self.target_table_found = False
            return

        if not self.target_table_found:
            return

        if tag == "th" and self.in_th:
            self.in_th = False
            self.current_field = self.current_text.strip()
        elif tag == "td" and self.in_td:
            self.in_td = False
            self.process_field(self.current_field, self.current_text.strip(), self.current_td_links, self.current_td_divs)

    def handle_data(self, data: str) -> None:
        if self.in_th:
            self.current_text += data
        elif self.in_td:
            self.current_text += data
            if self.current_td_links:
                self.current_td_links[-1]["text"] += data
            if self.current_td_divs:
                self.current_td_divs[-1]["text"] += data

    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(
            r"\s*(Link opens new browser tab|External link opens in new window or tab|Link opens new Email|Google Map)\s*",
            "",
            text,
        )
        text = re.sub(r"\s{2,}", " ", text)
        return text.strip()

    def process_field(self, label: str | None, text: str, links: list[dict[str, str]], divs: list[dict[str, str]]) -> None:
        if not label:
            return

        label = re.sub(r"\s+", " ", label).strip()

        if label == "County":
            self.data["county"] = text
        elif label == "Located within the boundaries of this public school district":
            self.data["district"] = text
            if links:
                self.data["district_link"] = links[0]["href"]
        elif label == "School":
            self.data["school"] = text
        elif label == "CDS Code":
            self.data["cds_code"] = text
        elif label == "School Address":
            self.data["school_address"] = self.clean_text(text)
            for link in links:
                if "google.com/maps" in link["href"]:
                    self.data["google_map_link"] = link["href"]
        elif label == "Mailing Address":
            self.data["mailing_address"] = self.clean_text(text)
        elif label == "Phone Number":
            self.data["phone_number"] = text
        elif label == "Fax Number":
            self.data["fax_number"] = text
        elif label == "Email":
            if links:
                self.data["email"] = self.clean_text(links[0]["text"])
            else:
                self.data["email"] = self.clean_text(text)
        elif label == "Web Address":
            if links:
                self.data["web_address"] = self.clean_text(links[0]["text"])
                self.data["web_address_link"] = links[0]["href"]
            else:
                self.data["web_address"] = self.clean_text(text)
        elif label == "Administrator":
            admins = []
            for div in divs:
                admin_text = self.clean_text(div["text"])
                if admin_text:
                    admin_data = {"info": admin_text}
                    email_match = re.search(r"([\w\.-]+@[\w\.-]+\.\w+)", admin_text)
                    if email_match:
                        admin_data["email"] = email_match.group(1)
                    admins.append(admin_data)
            self.data["administrators"] = admins
        elif label == "Status":
            self.data["status"] = text
        elif label == "Open Date":
            self.data["open_date"] = text
        elif label == "School Type":
            self.data["school_type"] = text
        elif label == "Educational Program Type":
            self.data["educational_program_type"] = text
        elif label == "Low Grade":
            self.data["low_grade"] = text
        elif label == "High Grade":
            self.data["high_grade"] = text
        elif label == "Public School":
            self.data["public_school"] = text
        elif label == "Statistical Info":
            if links:
                self.data["statistical_info"] = links[0]["text"].strip()
                self.data["statistical_info_link"] = links[0]["href"]
        elif label == "Last Updated":
            self.data["last_updated"] = text


def fetch_url(url: str, timeout: int = 30, max_retries: int = 3) -> requests.Response | None:
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                return None
            time.sleep(2)
        except requests.exceptions.RequestException:
            return None
    return None


def parse_school_list(html_content: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", class_="table table-bordered small")
    if not table:
        return []

    rows = table.find("tbody").find_all("tr") if table.find("tbody") else table.find_all("tr")[1:]
    records: list[dict[str, Any]] = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 8:
            continue

        school_cell = cells[3].find("a")
        if school_cell:
            school_name = school_cell.get_text(strip=True)
            detail_link = school_cell.get("href", "")
            if detail_link.startswith("/"):
                detail_link = "https://www.cde.ca.gov" + detail_link
        else:
            school_name = cells[3].get_text(strip=True)
            detail_link = ""

        records.append(
            {
                "cds_code": cells[0].get_text(strip=True),
                "county": cells[1].get_text(strip=True),
                "district": cells[2].get_text(strip=True),
                "school": school_name,
                "school_type": cells[4].get_text(strip=True),
                "sector_type": cells[5].get_text(strip=True),
                "charter": cells[6].get_text(strip=True),
                "status": cells[7].get_text(strip=True),
                "detail_link": detail_link,
            }
        )

    return records


def fetch_school_details(detail_link: str) -> dict[str, Any] | None:
    if not detail_link:
        return None
    response = fetch_url(detail_link)
    if not response:
        return None
    try:
        parser = SchoolProfileParser()
        parser.feed(response.text)
        return parser.data
    except Exception:
        return None


def flatten_for_csv(data: Any, prefix: str = "") -> dict[str, Any]:
    flat: dict[str, Any] = {}
    if isinstance(data, dict):
        for key, value in data.items():
            key_name = f"{prefix}.{key}" if prefix else str(key)
            flat.update(flatten_for_csv(value, key_name))
    elif isinstance(data, list):
        flat[prefix] = json.dumps(data, ensure_ascii=False)
    else:
        flat[prefix] = data
    return flat


def save_checkpoint(checkpoint_path: Path, processed_cds: set[str], results: list[dict[str, Any]]) -> None:
    checkpoint = {
        "processed_cds": sorted(processed_cds),
        "results_count": len(results),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with checkpoint_path.open("w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)


def load_checkpoint(checkpoint_path: Path) -> set[str]:
    if not checkpoint_path.exists():
        return set()
    try:
        with checkpoint_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("processed_cds", []))
    except Exception:
        return set()


def load_existing_results(output_json_path: Path) -> list[dict[str, Any]]:
    if not output_json_path.exists():
        return []
    try:
        with output_json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def run_detail_workers(
    schools: list[dict[str, Any]],
    output_json_path: Path,
    workers: int,
    checkpoint_interval: int,
    polite_delay: float,
) -> list[dict[str, Any]]:
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    checkpoint_path = Path(CHECKPOINT_DIR) / CHECKPOINT_FILE

    task_queue: Queue[dict[str, Any] | None] = Queue()
    for school in schools:
        task_queue.put(school)
    for _ in range(workers):
        task_queue.put(None)

    processed_cds = load_checkpoint(checkpoint_path)
    results = load_existing_results(output_json_path)

    # Merge checkpoint and existing outputs to avoid duplicate work after restart.
    for row in results:
        cds_code = str(row.get("cds_code", "")).strip()
        if cds_code:
            processed_cds.add(cds_code)

    lock = threading.Lock()
    progress = {"done": len(processed_cds), "total": len(schools), "since_checkpoint": 0}

    def worker(worker_id: int) -> None:
        while True:
            try:
                school = task_queue.get(timeout=1)
            except Empty:
                continue

            if school is None:
                task_queue.task_done()
                return

            school_name = school.get("school", "Unknown")
            cds_code = str(school.get("cds_code", "")).strip()
            detail_link = school.get("detail_link", "")

            with lock:
                if cds_code and cds_code in processed_cds:
                    logger.info("[W%02d] ⊙ Skipping already processed: %s", worker_id, school_name[:50])
                    task_queue.task_done()
                    continue

            if detail_link:
                details = fetch_school_details(detail_link)
                if details:
                    result = {**school, "detailed_info": details}
                    ok = True
                else:
                    result = {**school, "detailed_info": {}, "error": "Failed to fetch details"}
                    ok = False
            else:
                result = {**school, "detailed_info": {}, "error": "No detail link"}
                ok = False

            with lock:
                results.append(result)
                if cds_code:
                    processed_cds.add(cds_code)
                progress["done"] += 1
                progress["since_checkpoint"] += 1

                if ok:
                    logger.info("[W%02d] ✓ %-45s [%d/%d]", worker_id, school_name[:45], progress["done"], progress["total"])
                else:
                    logger.warning("[W%02d] ✗ %-45s [%d/%d]", worker_id, school_name[:45], progress["done"], progress["total"])

                if progress["since_checkpoint"] >= checkpoint_interval:
                    with output_json_path.open("w", encoding="utf-8") as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
                    save_checkpoint(checkpoint_path, processed_cds, results)
                    logger.info("[W%02d] 💾 Checkpoint saved (%d processed)", worker_id, len(processed_cds))
                    progress["since_checkpoint"] = 0

            task_queue.task_done()
            time.sleep(polite_delay)

    threads: list[threading.Thread] = []
    for worker_id in range(1, workers + 1):
        t = threading.Thread(target=worker, args=(worker_id,), daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with output_json_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    if checkpoint_path.exists():
        checkpoint_path.unlink()

    return results


def write_csv(records: list[dict[str, Any]], csv_path: Path) -> None:
    flattened_rows = [flatten_for_csv(row) for row in records]
    headers = sorted({k for row in flattened_rows for k in row.keys()})
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in flattened_rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Complete CDE scraper: list + detailed profiles + JSON/CSV export")
    parser.add_argument(
        "--list-url",
        default="https://www.cde.ca.gov/SchoolDirectory/certified-nonpublic-schools/0/1/500",
        help="School list URL to scrape",
    )
    parser.add_argument("--workers", type=int, default=10, help="Number of parallel worker threads")
    parser.add_argument("--checkpoint-interval", type=int, default=15, help="Save checkpoint every N processed records")
    parser.add_argument("--delay", type=float, default=0.3, help="Delay between detail requests per worker")
    parser.add_argument("--output-json", default=DEFAULT_JSON_OUTPUT, help="Output JSON file path")
    parser.add_argument("--output-csv", default=DEFAULT_CSV_OUTPUT, help="Output CSV file path")
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("ULTIMATE SCHOOL SCRAPER - COMPLETE")
    logger.info("List URL: %s", args.list_url)
    logger.info("Workers: %d | Checkpoint Interval: %d", args.workers, args.checkpoint_interval)
    logger.info("=" * 80)

    response = fetch_url(args.list_url)
    if not response:
        logger.error("Failed to fetch list URL: %s", args.list_url)
        return

    schools = parse_school_list(response.text)
    if not schools:
        logger.error("No school records found on page.")
        return

    logger.info("Found %d schools on list page", len(schools))

    output_json_path = Path(args.output_json)
    output_csv_path = Path(args.output_csv)

    start_time = time.time()
    results = run_detail_workers(
        schools=schools,
        output_json_path=output_json_path,
        workers=max(1, args.workers),
        checkpoint_interval=max(1, args.checkpoint_interval),
        polite_delay=max(0.0, args.delay),
    )
    duration = time.time() - start_time

    write_csv(results, output_csv_path)

    success = sum(1 for r in results if isinstance(r.get("detailed_info"), dict) and r.get("detailed_info"))
    failed = len(results) - success

    logger.info("=" * 80)
    logger.info("SUMMARY")
    logger.info("Total schools scraped: %d", len(results))
    logger.info("Successful detail fetches: %d", success)
    logger.info("Failed detail fetches: %d", failed)
    logger.info("JSON output: %s", output_json_path)
    logger.info("CSV output: %s", output_csv_path)
    logger.info("Duration: %.2f seconds", duration)
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
