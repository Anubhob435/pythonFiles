import json
import re
from html.parser import HTMLParser

class SchoolProfileParser(HTMLParser):
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
            # Update link text if we have links
            if self.current_td_links:
                self.current_td_links[-1]['text'] += data
            # Update div text if we have divs
            if self.current_td_divs:
                self.current_td_divs[-1]['text'] += data
            
    def clean_text(self, text):
        """Clean up extracted text"""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        # Remove common UI text artifacts
        text = re.sub(r'\s*(Link opens new browser tab|External link opens in new window or tab|Link opens new Email|Google Map)\s*', '', text)
        # Remove multiple spaces
        text = re.sub(r'\s{2,}', ' ', text)
        return text.strip()
    
    def process_field(self, label, text, links, divs):
        if not label:
            return
            
        # Normalize label
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
            # Clean up the address - extract just the address part
            address_match = re.search(r'([\d]+\s+[^<]+?(?:Rd\.|Road|St\.|Street|Ave\.|Avenue|Blvd\.|Boulevard)[^,]*,\s*[^,]+,\s*CA\s*\d+-?\d*)', text, re.IGNORECASE)
            if address_match:
                self.data['school_address'] = address_match.group(1).strip()
            else:
                self.data['school_address'] = self.clean_text(text)
            # Find Google Maps link
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
            # Parse administrators from divs
            administrators = []
            for div in divs:
                admin_text = self.clean_text(div['text'])
                if admin_text:
                    # Extract email from the admin text
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


# Read the HTML file
with open('profile.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Parse the HTML
parser = SchoolProfileParser()
parser.feed(html_content)

# Save to JSON file
with open('school_profile_data.json', 'w', encoding='utf-8') as f:
    json.dump(parser.data, f, indent=2, ensure_ascii=False)

print(f"Successfully extracted school profile data to school_profile_data.json")
print(f"Extracted {len(parser.data)} fields")
