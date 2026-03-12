import requests
import json
import time
from bs4 import BeautifulSoup

# List of URLs to scrape
SCHOOL_LIST_URLS = [
    "https://www.cde.ca.gov/SchoolDirectory/active-or-pending-schools/2/0/1/500",
    "https://www.cde.ca.gov/SchoolDirectory/active-or-pending-schools/2/1/1/500",
    "https://www.cde.ca.gov/SchoolDirectory/active-or-pending-schools/2/2/1/500",
    "https://www.cde.ca.gov/SchoolDirectory/active-or-pending-schools/2/3/1/500",
    "https://www.cde.ca.gov/SchoolDirectory/active-or-pending-schools/2/4/1/500",
    "https://www.cde.ca.gov/SchoolDirectory/active-or-pending-schools/2/5/1/500",
    "https://www.cde.ca.gov/SchoolDirectory/active-or-pending-schools/2/6/1/500"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


def fetch_url(url, timeout=30, max_retries=3):
    """Fetch URL with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print(f"  ⚠ Timeout on attempt {attempt + 1}/{max_retries}")
            if attempt == max_retries - 1:
                print(f"  ✗ Failed after {max_retries} attempts: {url}")
                return None
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error: {e}")
            return None
    return None


def parse_school_list(html_content):
    """Parse school list HTML and extract school information"""
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table table-bordered small')
    
    if not table:
        return []
    
    records = []
    rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')[1:]
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 8:
            cds_code = cells[0].get_text(strip=True)
            county = cells[1].get_text(strip=True)
            district = cells[2].get_text(strip=True)
            
            school_cell = cells[3].find('a')
            if school_cell:
                school_name = school_cell.get_text(strip=True)
                detail_link = school_cell.get('href', '')
                if detail_link.startswith('/'):
                    detail_link = 'https://www.cde.ca.gov' + detail_link
            else:
                school_name = cells[3].get_text(strip=True)
                detail_link = ''
            
            school_type = cells[4].get_text(strip=True)
            sector_type = cells[5].get_text(strip=True)
            charter = cells[6].get_text(strip=True)
            status = cells[7].get_text(strip=True)
            
            record = {
                'cds_code': cds_code,
                'county': county,
                'district': district,
                'school': school_name,
                'school_type': school_type,
                'sector_type': sector_type,
                'charter': charter,
                'status': status,
                'detail_link': detail_link
            }
            
            records.append(record)
    
    return records


def main():
    """Main function to orchestrate the scraping process"""
    print("=" * 80)
    print("ULTIMATE SCHOOL SCRAPER - PART 1: BASIC INFO")
    print("=" * 80)
    
    all_schools = []
    
    # Fetch all school list pages
    print(f"\n📋 Fetching {len(SCHOOL_LIST_URLS)} school list pages...")
    for idx, url in enumerate(SCHOOL_LIST_URLS, 1):
        print(f"\n[{idx}/{len(SCHOOL_LIST_URLS)}] Fetching: {url}")
        response = fetch_url(url)
        
        if response:
            print(f"  ✓ Status Code: {response.status_code}")
            schools = parse_school_list(response.text)
            print(f"  ✓ Found {len(schools)} schools")
            all_schools.extend(schools)
        else:
            print(f"  ✗ Failed to fetch")
        
        # Be nice to the server
        time.sleep(1)
    
    print(f"\n✓ Total schools found: {len(all_schools)}")
    
    # Save to JSON
    print(f"\n💾 Saving basic data to JSON...")
    output_file = 'schools_basic_data.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_schools, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Successfully saved to '{output_file}'")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total schools: {len(all_schools)}")
    print(f"Schools with detail links: {sum(1 for s in all_schools if s.get('detail_link'))}")
    print(f"Output file: {output_file}")
    print("=" * 80)
    print("\nNext step: Run ultimate_script_2.py to fetch detailed information for each school")


if __name__ == "__main__":
    main()