import json
from bs4 import BeautifulSoup

# Read the HTML file
with open('response.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table
table = soup.find('table', class_='table table-bordered small')

# Extract all records
records = []
rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')[1:]  # Skip header row

for row in rows:
    cells = row.find_all('td')
    if len(cells) >= 8:  # Ensure we have all columns
        # Extract CDS Code
        cds_code = cells[0].get_text(strip=True)
        
        # Extract County
        county = cells[1].get_text(strip=True)
        
        # Extract District
        district = cells[2].get_text(strip=True)
        
        # Extract School name and link
        school_cell = cells[3].find('a')
        if school_cell:
            school_name = school_cell.get_text(strip=True)
            detail_link = school_cell.get('href', '')
            # Make the link absolute
            if detail_link.startswith('/'):
                detail_link = 'https://www.cde.ca.gov' + detail_link
        else:
            school_name = cells[3].get_text(strip=True)
            detail_link = ''
        
        # Extract School Type
        school_type = cells[4].get_text(strip=True)
        
        # Extract Sector Type
        sector_type = cells[5].get_text(strip=True)
        
        # Extract Charter
        charter = cells[6].get_text(strip=True)
        
        # Extract Status
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

# Save to JSON file
with open('schools_data.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"Successfully extracted {len(records)} records to schools_data.json")
