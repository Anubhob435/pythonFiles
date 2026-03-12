import requests
import json
import re
import time
import threading
import logging
import os
from html.parser import HTMLParser
from queue import Queue
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('school_scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Checkpoint configuration
CHECKPOINT_INTERVAL = 15  # Save progress every 15 items
CHECKPOINT_DIR = 'checkpoints'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


# Create checkpoint directory if it doesn't exist
os.makedirs(CHECKPOINT_DIR, exist_ok=True)


class SchoolProfileParser(HTMLParser):
    """Parser for extracting detailed school profile data"""
    def __init__(self):
        super().__init__()
        self.data = {}
        self.current_field = None
        self.current_text = ""
        self.in_th = False
        self.in_td = False
        self.in_table = False
        self.target_table_found = False
        self.current_td_links = []
        self.current_td_divs = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'table' and 'class' in attrs_dict and 'table table-bordered small' in attrs_dict.get('class', ''):
            self.in_table = True
            self.target_table_found = True
            return
            
        if not self.target_table_found:
            return
            
        if tag == 'th' and 'details-field-label' in attrs_dict.get('class', ''):
            self.in_th = True
            self.current_text = ""
        elif tag == 'td':
            self.in_td = True
            self.current_text = ""
            self.current_td_links = []
            self.current_td_divs = []
        elif tag == 'a' and self.in_td:
            href = attrs_dict.get('href', '')
            self.current_td_links.append({
                'text': '',
                'href': href
            })
        elif tag == 'div' and self.in_td:
            self.current_td_divs.append({'text': ''})
            
    def handle_endtag(self, tag):
        if tag == 'table' and self.in_table:
            self.in_table = False
            self.target_table_found = False
            return
            
        if not self.target_table_found:
            return
            
        if tag == 'th' and self.in_th:
            self.in_th = False
            self.current_field = self.current_text.strip()
        elif tag == 'td' and self.in_td:
            self.in_td = False
            self.process_field(self.current_field, self.current_text.strip(), self.current_td_links, self.current_td_divs)
            
    def handle_data(self, data):
        if self.in_th:
            self.current_text += data
        elif self.in_td:
            self.current_text += data
            if self.current_td_links:
                self.current_td_links[-1]['text'] += data
            if self.current_td_divs:
                self.current_td_divs[-1]['text'] += data
            
    def clean_text(self, text):
        """Clean up extracted text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s*(Link opens new browser tab|External link opens in new window or tab|Link opens new Email|Google Map)\s*', '', text)
        text = re.sub(r'\s{2,}', ' ', text)
        return text.strip()
    
    def process_field(self, label, text, links, divs):
        if not label:
            return
            
        label = re.sub(r'\s+', ' ', label).strip()
        
        if label == 'County':
            self.data['county'] = text
        elif label == 'Located within the boundaries of this public school district':
            self.data['district'] = text
            if links:
                self.data['district_link'] = links[0]['href']
        elif label == 'School':
            self.data['school'] = text
        elif label == 'CDS Code':
            self.data['cds_code'] = text
        elif label == 'School Address':
            self.data['school_address'] = self.clean_text(text)
            for link in links:
                if 'google.com/maps' in link['href']:
                    self.data['google_map_link'] = link['href']
        elif label == 'Mailing Address':
            self.data['mailing_address'] = self.clean_text(text)
        elif label == 'Phone Number':
            self.data['phone_number'] = text
        elif label == 'Fax Number':
            self.data['fax_number'] = text
        elif label == 'Email':
            if links:
                self.data['email'] = self.clean_text(links[0]['text'])
            else:
                self.data['email'] = self.clean_text(text)
        elif label == 'Web Address':
            if links:
                self.data['web_address'] = self.clean_text(links[0]['text'])
                self.data['web_address_link'] = links[0]['href']
            else:
                self.data['web_address'] = self.clean_text(text)
        elif label == 'Administrator':
            administrators = []
            for div in divs:
                admin_text = self.clean_text(div['text'])
                if admin_text:
                    email_match = re.search(r'([\w\.-]+@[\w\.-]+\.\w+)', admin_text)
                    admin_data = {'info': admin_text}
                    if email_match:
                        admin_data['email'] = email_match.group(1)
                    administrators.append(admin_data)
            self.data['administrators'] = administrators
        elif label == 'Status':
            self.data['status'] = text
        elif label == 'Open Date':
            self.data['open_date'] = text
        elif label == 'School Type':
            self.data['school_type'] = text
        elif label == 'Educational Program Type':
            self.data['educational_program_type'] = text
        elif label == 'Low Grade':
            self.data['low_grade'] = text
        elif label == 'High Grade':
            self.data['high_grade'] = text
        elif label == 'Public School':
            self.data['public_school'] = text
        elif label == 'Statistical Info':
            if links:
                self.data['statistical_info'] = links[0]['text'].strip()
                self.data['statistical_info_link'] = links[0]['href']
        elif label == 'Last Updated':
            self.data['last_updated'] = text


class WorkerStats:
    """Thread-safe statistics tracking"""
    def __init__(self):
        self.lock = threading.Lock()
        self.stats = {i: {'processed': 0, 'successful': 0, 'failed': 0} for i in range(1, 11)}
        self.global_processed = 0
        self.global_total = 0
    
    def increment(self, worker_id, success):
        with self.lock:
            self.stats[worker_id]['processed'] += 1
            if success:
                self.stats[worker_id]['successful'] += 1
            else:
                self.stats[worker_id]['failed'] += 1
            self.global_processed += 1
    
    def set_total(self, total):
        with self.lock:
            self.global_total = total
    
    def get_progress(self):
        with self.lock:
            return self.global_processed, self.global_total


def fetch_url(url, timeout=30, max_retries=3):
    """Fetch URL with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                return None
            time.sleep(1)
        except requests.exceptions.RequestException:
            return None
    return None


def fetch_school_details(detail_link):
    """Fetch and parse school detail page"""
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


def load_checkpoint(worker_id):
    """Load checkpoint for a worker if it exists"""
    checkpoint_file = os.path.join(CHECKPOINT_DIR, f'worker_{worker_id}_checkpoint.json')
    
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            logger.info(f"[Worker {worker_id}] Loaded checkpoint: {len(checkpoint['processed_cds'])} already processed")
            return checkpoint
        except Exception as e:
            logger.warning(f"[Worker {worker_id}] Failed to load checkpoint: {e}")
            return None
    return None


def save_checkpoint(worker_id, processed_cds, worker_results):
    """Save checkpoint for a worker"""
    checkpoint_file = os.path.join(CHECKPOINT_DIR, f'worker_{worker_id}_checkpoint.json')
    
    checkpoint = {
        'worker_id': worker_id,
        'processed_cds': list(processed_cds),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'results_count': len(worker_results)
    }
    
    try:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)
        
        # Also save current results to output file
        output_file = f'profile_data_{worker_id}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(worker_results, f, indent=2, ensure_ascii=False)
            
        return True
    except Exception as e:
        logger.error(f"[Worker {worker_id}] Failed to save checkpoint: {e}")
        return False


def delete_checkpoint(worker_id):
    """Delete checkpoint file after worker completes"""
    checkpoint_file = os.path.join(CHECKPOINT_DIR, f'worker_{worker_id}_checkpoint.json')
    try:
        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)
            logger.info(f"[Worker {worker_id}] Checkpoint deleted (worker completed)")
    except Exception as e:
        logger.warning(f"[Worker {worker_id}] Failed to delete checkpoint: {e}")


def load_existing_results(worker_id):
    """Load existing results from output file if it exists"""
    output_file = f'profile_data_{worker_id}.json'
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"[Worker {worker_id}] Failed to load existing results: {e}")
            return []
    return []


def worker(worker_id, task_queue, stats, logger_lock):
    """Worker thread that processes schools from the queue with checkpoint support"""
    worker_logger = logging.getLogger(f'__main__.worker{worker_id}')
    
    # Load checkpoint if exists
    checkpoint = load_checkpoint(worker_id)
    processed_cds = set(checkpoint['processed_cds']) if checkpoint else set()
    
    # Load existing results
    worker_results = load_existing_results(worker_id)
    
    with logger_lock:
        if checkpoint:
            worker_logger.info(f"Resuming from checkpoint - {len(processed_cds)} schools already processed")
        else:
            worker_logger.info(f"Starting fresh - no checkpoint found")
    
    items_since_checkpoint = 0
    
    while True:
        try:
            school = task_queue.get(timeout=1)
            if school is None:  # Poison pill
                break
            
            # Process school
            school_name = school.get('school', 'Unknown')
            cds_code = school.get('cds_code', 'Unknown')
            detail_link = school.get('detail_link', '')
            
            # Skip if already processed (from checkpoint)
            if cds_code in processed_cds:
                with logger_lock:
                    worker_logger.info(f"⊙ Skipping (already processed): {school_name[:40]:40s}")
                task_queue.task_done()
                continue
            
            if detail_link:
                details = fetch_school_details(detail_link)
                if details:
                    # Merge basic info with detailed info
                    result = {**school, 'detailed_info': details}
                    worker_results.append(result)
                    processed_cds.add(cds_code)
                    stats.increment(worker_id, True)
                    
                    with logger_lock:
                        processed, total = stats.get_progress()
                        worker_logger.info(f"✓ {school_name[:40]:40s} [{processed}/{total}]")
                else:
                    result = {**school, 'detailed_info': {}, 'error': 'Failed to fetch details'}
                    worker_results.append(result)
                    processed_cds.add(cds_code)
                    stats.increment(worker_id, False)
                    
                    with logger_lock:
                        processed, total = stats.get_progress()
                        worker_logger.warning(f"✗ {school_name[:40]:40s} [{processed}/{total}]")
            else:
                result = {**school, 'detailed_info': {}, 'error': 'No detail link'}
                worker_results.append(result)
                processed_cds.add(cds_code)
                stats.increment(worker_id, False)
            
            items_since_checkpoint += 1
            
            # Save checkpoint every CHECKPOINT_INTERVAL items
            if items_since_checkpoint >= CHECKPOINT_INTERVAL:
                with logger_lock:
                    worker_logger.info(f"💾 Saving checkpoint ({len(processed_cds)} processed)")
                save_checkpoint(worker_id, processed_cds, worker_results)
                items_since_checkpoint = 0
            
            # Small delay to be nice to server
            time.sleep(0.3)
            
            task_queue.task_done()
            
        except Exception as e:
            with logger_lock:
                worker_logger.error(f"Error processing school: {e}")
            break
    
    # Final save of results
    output_file = f'profile_data_{worker_id}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(worker_results, f, indent=2, ensure_ascii=False)
    
    # Delete checkpoint after successful completion
    delete_checkpoint(worker_id)
    
    with logger_lock:
        worker_logger.info(f"✓ Completed - Saved {len(worker_results)} schools to {output_file}")


def main():
    """Main function to coordinate parallel scraping with checkpoint support"""
    logger.info("=" * 80)
    logger.info("ULTIMATE SCHOOL SCRAPER - PART 2: DETAILED INFO (10 PARALLEL WORKERS)")
    logger.info("WITH CHECKPOINT SUPPORT - SAVES EVERY 15 ITEMS")
    logger.info("=" * 80)
    
    # Check for existing checkpoints
    existing_checkpoints = [f for f in os.listdir(CHECKPOINT_DIR) if f.endswith('_checkpoint.json')]
    if existing_checkpoints:
        logger.info(f"Found {len(existing_checkpoints)} existing checkpoint(s) - will resume from where left off")
    
    # Load basic school data
    input_file = 'schools_basic_data.json'
    if not Path(input_file).exists():
        logger.error(f"Error: {input_file} not found!")
        logger.error("Please run ultimate_script_1.py first to generate basic school data.")
        return
    
    logger.info(f"Loading schools from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        schools = json.load(f)
    
    logger.info(f"Loaded {len(schools)} schools")
    
    # Filter schools with detail links
    schools_with_links = [s for s in schools if s.get('detail_link')]
    logger.info(f"{len(schools_with_links)} schools have detail links")
    
    if not schools_with_links:
        logger.error("No schools with detail links found!")
        return
    
    # Setup
    task_queue = Queue()
    stats = WorkerStats()
    stats.set_total(len(schools_with_links))
    logger_lock = threading.Lock()
    
    # Add all schools to queue
    for school in schools_with_links:
        task_queue.put(school)
    
    # Add poison pills for workers
    for _ in range(10):
        task_queue.put(None)
    
    logger.info("Starting 10 parallel workers...")
    logger.info(f"Checkpoint directory: {CHECKPOINT_DIR}/")
    logger.info(f"Checkpoint interval: every {CHECKPOINT_INTERVAL} items")
    logger.info("=" * 80)
    
    # Start worker threads
    threads = []
    start_time = time.time()
    
    for worker_id in range(1, 11):
        thread = threading.Thread(target=worker, args=(worker_id, task_queue, stats, logger_lock))
        thread.start()
        threads.append(thread)
    
    # Wait for all workers to finish
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Summary
    logger.info("=" * 80)
    logger.info("SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total processing time: {duration:.2f} seconds")
    logger.info(f"Total schools processed: {len(schools_with_links)}")
    logger.info("Per-worker statistics:")
    logger.info("-" * 80)
    
    total_successful = 0
    total_failed = 0
    
    for worker_id in range(1, 11):
        w_stats = stats.stats[worker_id]
        total_successful += w_stats['successful']
        total_failed += w_stats['failed']
        logger.info(f"  Worker {worker_id:2d}: {w_stats['processed']:4d} processed | "
              f"{w_stats['successful']:4d} successful | {w_stats['failed']:4d} failed | "
              f"File: profile_data_{worker_id}.json")
    
    logger.info("-" * 80)
    logger.info(f"  Total:     {total_successful + total_failed:4d} processed | "
          f"{total_successful:4d} successful | {total_failed:4d} failed")
    logger.info("=" * 80)
    logger.info(f"Results saved to: profile_data_1.json through profile_data_10.json")
    logger.info(f"Checkpoints directory: {CHECKPOINT_DIR}/")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
