import PyPDF2
import re
import os
from pathlib import Path

class BhagavadGitaSplitter:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.reader = None
        self.total_pages = 0
        self.output_dir = "bhagavad_gita_parts"
        
        # Manual chapter page numbers based on your specific PDF
        # Chapter start pages: 31, 53, 101, 129, 158, 179, 202, 222, 238, 260, 282, 306, 318, 340, 354, 371, 366, 395
        self.chapter_pages = {
            1: {'start_page': 31, 'title': "Arjuna's Distress"},
            2: {'start_page': 53, 'title': "The Path of Doctrines"},
            3: {'start_page': 101, 'title': "The Path of Action"},
            4: {'start_page': 129, 'title': "Wisdom in Action"},
            5: {'start_page': 158, 'title': "The Path of Renunciation"},
            6: {'start_page': 179, 'title': "The Path of Self Restraint"},
            7: {'start_page': 202, 'title': "The Path of Knowledge and Wisdom"},
            8: {'start_page': 222, 'title': "The Imperishable Lord"},
            9: {'start_page': 238, 'title': "Path of Supreme Knowledge and Secrets"},
            10: {'start_page': 260, 'title': "Divine Manifestations"},
            11: {'start_page': 282, 'title': "The Lord's Universal Form"},
            12: {'start_page': 306, 'title': "The Path of Devotion"},
            13: {'start_page': 318, 'title': "The Field and The Knower of the Field"},
            14: {'start_page': 340, 'title': "Division of Qualities"},
            15: {'start_page': 354, 'title': "Theology of The Supreme Being"},
            16: {'start_page': 366, 'title': "The Divine and the Demoniac"},
            17: {'start_page': 371, 'title': "The Threefold Faith"},
            18: {'start_page': 395, 'title': "Liberation and Renunciation"}
        }
        
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
    
    def scan_for_chapters(self):
        """Scan PDF to find actual chapter start pages"""
        print("Scanning PDF to find chapter start pages...")
        
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                detected_chapters = {}
                
                # Start scanning from page 31 (after introduction)
                for page_num in range(30, min(len(reader.pages), 450)):
                    try:
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        
                        # Look for chapter headers at the beginning of pages
                        lines = text.split('\n')[:10]  # Check first 10 lines
                        for line in lines:
                            line = line.strip()
                            # Look for patterns like "Chapter 1" or "Chapter One"
                            chapter_match = re.search(r'Chapter\s+(\d+|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen)', line, re.IGNORECASE)
                            
                            if chapter_match:
                                chapter_text = chapter_match.group(1)
                                if chapter_text.isdigit():
                                    chapter_num = int(chapter_text)
                                else:
                                    # Convert word numbers to digits
                                    word_to_num = {
                                        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                                        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
                                        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
                                        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18
                                    }
                                    chapter_num = word_to_num.get(chapter_text.lower(), 0)
                                
                                if 1 <= chapter_num <= 18 and chapter_num not in detected_chapters:
                                    detected_chapters[chapter_num] = page_num + 1
                                    print(f"Found Chapter {chapter_num} on page {page_num + 1}")
                                    break
                    
                    except Exception as e:
                        continue
                
                # Update chapter pages if we found any
                if detected_chapters:
                    print(f"Auto-detected {len(detected_chapters)} chapters")
                    for chapter_num, page_num in detected_chapters.items():
                        if chapter_num in self.chapter_pages:
                            self.chapter_pages[chapter_num]['start_page'] = page_num
                else:
                    print("Using manual chapter page numbers")
                    
        except Exception as e:
            print(f"Error scanning for chapters: {e}")
            print("Using manual chapter page numbers")
    
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
        
        # Ask user if they want to scan for chapters or use manual pages
        print("\nOptions:")
        print("1. Auto-scan for chapters (recommended)")
        print("2. Use manual chapter pages")
        
        while True:
            choice = input("Choose option (1 or 2): ").strip()
            if choice == '1':
                self.scan_for_chapters()
                break
            elif choice == '2':
                print("Using manual chapter page numbers")
                break
            else:
                print("Please enter 1 or 2")
        
        # Part 1: Pages 15-30 (Introduction/Preface)
        print(f"\nCreating parts...")
        self.split_pdf_by_pages(15, 30, "01_Introduction_Pages_15-30.pdf")
        
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
            
            # Create clean filename
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', chapter_title)
            safe_title = safe_title.replace(' ', '_')
            filename = f"{chapter_num + 1:02d}_Chapter_{chapter_num:02d}_{safe_title}.pdf"
            
            self.split_pdf_by_pages(start_page, end_page, filename)
        
        print(f"\n✅ Splitting complete! All parts saved in '{self.output_dir}' directory.")
        print(f"📚 Total parts created: {len(sorted_chapters) + 1}")
        
        # Show summary
        print(f"\n📋 Summary:")
        print(f"   Part 1: Introduction (Pages 15-30)")
        for i, chapter_num in enumerate(sorted_chapters):
            chapter_info = self.chapter_pages[chapter_num]
            start_page = chapter_info['start_page']
            if i + 1 < len(sorted_chapters):
                next_chapter = sorted_chapters[i + 1]
                end_page = self.chapter_pages[next_chapter]['start_page'] - 1
            else:
                end_page = self.total_pages
            print(f"   Part {chapter_num + 1}: Chapter {chapter_num} - {chapter_info['title']} (Pages {start_page}-{end_page})")
        
        return True

def main():
    pdf_path = "The_Bhagavad_Gita.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file '{pdf_path}' not found in current directory.")
        return
    
    print("📖 Bhagavad Gita PDF Splitter")
    print("=" * 50)
    print("This script will split the Bhagavad Gita into 19 parts:")
    print("• Part 1: Introduction (Pages 15-30)")
    print("• Parts 2-19: Individual chapters (18 chapters)")
    print()
    
    splitter = BhagavadGitaSplitter(pdf_path)
    
    # Ask user if they want to proceed
    response = input(f"📝 Split '{pdf_path}' into 19 parts? (y/n): ").lower()
    if response in ['y', 'yes']:
        splitter.split_bhagavad_gita()
    else:
        print("❌ Operation cancelled.")

if __name__ == "__main__":
    main()
