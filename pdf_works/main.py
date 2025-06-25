import PyPDF2
import re
import os
from pathlib import Path

class BhagavadGitaSplitter:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.reader = None
        self.total_pages = 0
        self.chapter_pages = {}
        self.output_dir = "bhagavad_gita_parts"
        
    def load_pdf(self):
        """Load the PDF file and get basic information"""
        try:
            with open(self.pdf_path, 'rb') as file:
                self.reader = PyPDF2.PdfReader(file)
                self.total_pages = len(self.reader.pages)
                print(f"PDF loaded successfully. Total pages: {self.total_pages}")
                return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def find_chapter_pages(self):
        """Find the starting page of each chapter by searching for chapter headers"""
        chapter_pattern = re.compile(r'Chapter\s+(\d+)\s*[–-]\s*(.+)', re.IGNORECASE)
        
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(reader.pages)):
                    try:
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        
                        # Search for chapter headers
                        matches = chapter_pattern.findall(text)
                        for match in matches:
                            chapter_num = int(match[0])
                            chapter_title = match[1].strip()
                            if chapter_num not in self.chapter_pages:
                                self.chapter_pages[chapter_num] = {
                                    'start_page': page_num + 1,  # 1-indexed
                                    'title': chapter_title
                                }
                                print(f"Found Chapter {chapter_num}: {chapter_title} on page {page_num + 1}")
                    
                    except Exception as e:
                        print(f"Error processing page {page_num + 1}: {e}")
                        continue
        
        except Exception as e:
            print(f"Error finding chapters: {e}")
            
        # If automatic detection fails, provide manual chapter page numbers
        if not self.chapter_pages:
            print("Automatic chapter detection failed. Using manual chapter pages...")
            self.chapter_pages = self.get_manual_chapter_pages()
    
    def get_manual_chapter_pages(self):
        """Manual chapter page numbers (you may need to adjust these)"""
        return {
            1: {'start_page': 31, 'title': "Arjuna's Distress"},
            2: {'start_page': 45, 'title': "The Path of Doctrines"},
            3: {'start_page': 75, 'title': "The Path of Action"},
            4: {'start_page': 95, 'title': "The Path of Knowledge"},
            5: {'start_page': 115, 'title': "The Path of Renunciation"},
            6: {'start_page': 135, 'title': "The Path of Meditation"},
            7: {'start_page': 155, 'title': "The Path of Realization"},
            8: {'start_page': 175, 'title': "The Imperishable Brahman"},
            9: {'start_page': 190, 'title': "The Royal Knowledge"},
            10: {'start_page': 210, 'title': "The Divine Manifestations"},
            11: {'start_page': 235, 'title': "The Universal Form"},
            12: {'start_page': 260, 'title': "The Path of Devotion"},
            13: {'start_page': 275, 'title': "The Field and the Knower"},
            14: {'start_page': 295, 'title': "The Three Gunas"},
            15: {'start_page': 315, 'title': "The Supreme Person"},
            16: {'start_page': 330, 'title': "Divine and Demonic Natures"},
            17: {'start_page': 345, 'title': "The Three Types of Faith"},
            18: {'start_page': 365, 'title': "The Path of Liberation"}
        }
    
    def create_output_directory(self):
        """Create output directory for the split PDFs"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
    
    def split_pdf_by_pages(self, start_page, end_page, output_filename):
        """Split PDF by page range and save to file"""
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                # Add pages (convert to 0-indexed)
                for page_num in range(start_page - 1, min(end_page, len(reader.pages))):
                    writer.add_page(reader.pages[page_num])
                
                # Write to output file
                output_path = os.path.join(self.output_dir, output_filename)
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                print(f"Created: {output_filename} (Pages {start_page}-{end_page})")
                return True
                
        except Exception as e:
            print(f"Error creating {output_filename}: {e}")
            return False
    
    def split_bhagavad_gita(self):
        """Main function to split the Bhagavad Gita into 19 parts"""
        if not self.load_pdf():
            return False
        
        self.create_output_directory()
        self.find_chapter_pages()
        
        # Part 1: Pages 1-30 (Introduction/Preface)
        self.split_pdf_by_pages(1, 30, "01_Introduction_Pages_1-30.pdf")
        
        # Get sorted chapter numbers
        sorted_chapters = sorted(self.chapter_pages.keys())
        
        # Split by chapters
        for i, chapter_num in enumerate(sorted_chapters):
            chapter_info = self.chapter_pages[chapter_num]
            start_page = chapter_info['start_page']
            chapter_title = chapter_info['title']
            
            # Determine end page (start of next chapter - 1, or end of PDF)
            if i + 1 < len(sorted_chapters):
                next_chapter = sorted_chapters[i + 1]
                end_page = self.chapter_pages[next_chapter]['start_page'] - 1
            else:
                end_page = self.total_pages
            
            # Create filename
            filename = f"{chapter_num + 1:02d}_Chapter_{chapter_num}_{chapter_title.replace(' ', '_').replace('/', '_')}.pdf"
            # Clean filename of invalid characters
            filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
            
            self.split_pdf_by_pages(start_page, end_page, filename)
        
        print(f"\nSplitting complete! All parts saved in '{self.output_dir}' directory.")
        print(f"Total parts created: {len(sorted_chapters) + 1}")
        
        return True

def main():
    pdf_path = "The_Bhagavad_Gita.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found in current directory.")
        return
    
    print("Bhagavad Gita PDF Splitter")
    print("=" * 40)
    
    splitter = BhagavadGitaSplitter(pdf_path)
    
    # Ask user if they want to proceed
    response = input(f"Split '{pdf_path}' into 19 parts? (y/n): ").lower()
    if response == 'y' or response == 'yes':
        splitter.split_bhagavad_gita()
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()