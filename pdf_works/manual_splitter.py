import PyPDF2
import os

def split_bhagavad_gita_manual():
    """
    Simple manual splitter for Bhagavad Gita PDF
    Adjust the chapter_starts list based on your PDF's actual chapter pages
    """
    
    pdf_path = "The_Bhagavad_Gita.pdf"
    output_dir = "bhagavad_gita_parts"
    
    # ADJUST THESE PAGE NUMBERS BASED ON YOUR PDF!
    # To find the correct pages, open your PDF and note where each chapter starts
    chapter_starts = {
        1: 31,   # Chapter 1 starts at page 31
        2: 50,   # Chapter 2 starts at page 50  
        3: 80,   # Chapter 3 starts at page 80
        4: 105,  # Chapter 4 starts at page 105
        5: 130,  # Chapter 5 starts at page 130
        6: 150,  # Chapter 6 starts at page 150
        7: 175,  # Chapter 7 starts at page 175
        8: 195,  # Chapter 8 starts at page 195
        9: 215,  # Chapter 9 starts at page 215
        10: 235, # Chapter 10 starts at page 235
        11: 260, # Chapter 11 starts at page 260
        12: 285, # Chapter 12 starts at page 285
        13: 300, # Chapter 13 starts at page 300
        14: 320, # Chapter 14 starts at page 320
        15: 335, # Chapter 15 starts at page 335
        16: 350, # Chapter 16 starts at page 350
        17: 365, # Chapter 17 starts at page 365
        18: 380  # Chapter 18 starts at page 380
    }
    
    chapter_titles = {
        1: "Arjuna's Distress",
        2: "The Path of Doctrines", 
        3: "The Path of Action",
        4: "Wisdom in Action",
        5: "The Path of Renunciation",
        6: "The Path of Self Restraint",
        7: "The Path of Knowledge and Wisdom",
        8: "The Imperishable Lord",
        9: "Path of Supreme Knowledge and Secrets",
        10: "Divine Manifestations",
        11: "The Lord's Universal Form",
        12: "The Path of Devotion",
        13: "The Field and The Knower of the Field",
        14: "Division of Qualities",
        15: "Theology of The Supreme Being",
        16: "The Divine and the Demoniac",
        17: "The Threefold Faith",
        18: "Liberation and Renunciation"
    }
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: {pdf_path} not found!")
        return
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created directory: {output_dir}")
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            print(f"📖 PDF loaded: {total_pages} total pages")
            
            # Part 1: Introduction (Pages 1-30)
            print(f"\n🔄 Creating parts...")
            writer = PyPDF2.PdfWriter()
            for page_num in range(0, 30):  # 0-indexed
                if page_num < total_pages:
                    writer.add_page(reader.pages[page_num])
            
            output_path = os.path.join(output_dir, "01_Introduction_Pages_1-30.pdf")
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            print(f"✅ Created: 01_Introduction_Pages_1-30.pdf")
            
            # Chapters 1-18
            chapters = sorted(chapter_starts.keys())
            for i, chapter_num in enumerate(chapters):
                start_page = chapter_starts[chapter_num] - 1  # Convert to 0-indexed
                
                # Determine end page
                if i + 1 < len(chapters):
                    end_page = chapter_starts[chapters[i + 1]] - 1
                else:
                    end_page = total_pages
                
                # Create PDF for this chapter
                writer = PyPDF2.PdfWriter()
                for page_num in range(start_page, min(end_page, total_pages)):
                    writer.add_page(reader.pages[page_num])
                
                # Create filename
                safe_title = chapter_titles[chapter_num].replace(' ', '_').replace("'", "").replace('/', '_')
                filename = f"{chapter_num + 1:02d}_Chapter_{chapter_num:02d}_{safe_title}.pdf"
                output_path = os.path.join(output_dir, filename)
                
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                print(f"✅ Created: {filename} (Pages {start_page + 1}-{end_page})")
            
            print(f"\n🎉 SUCCESS! Created 19 parts in '{output_dir}' directory")
            print(f"📊 Summary:")
            print(f"   • Part 1: Introduction (Pages 1-30)")
            for i, chapter_num in enumerate(chapters):
                start_page = chapter_starts[chapter_num]
                if i + 1 < len(chapters):
                    end_page = chapter_starts[chapters[i + 1]] - 1
                else:
                    end_page = total_pages
                print(f"   • Part {chapter_num + 1}: Chapter {chapter_num} - {chapter_titles[chapter_num]} (Pages {start_page}-{end_page})")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("📖 Bhagavad Gita PDF Splitter (Manual)")
    print("=" * 50)
    print("⚠️  IMPORTANT: Check and adjust chapter page numbers in the script if needed!")
    print()
    
    response = input("🚀 Start splitting? (y/n): ").lower()
    if response in ['y', 'yes']:
        split_bhagavad_gita_manual()
    else:
        print("❌ Cancelled.")
