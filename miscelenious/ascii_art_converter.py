from PIL import Image
import sys

def convert_to_ascii(image_path, width=100, height=None):
    """
    Convert an image to ASCII art.
    
    Args:
        image_path (str): Path to the image file
        width (int): Width of the output ASCII art (in characters)
        height (int): Height of the output ASCII art (in lines)
                     If None, it's calculated to maintain aspect ratio
    
    Returns:
        str: ASCII art representation of the image
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Calculate height to maintain aspect ratio if not provided
        if height is None:
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio * 0.5)  # 0.5 factor because characters are taller than wide
        
        # Resize the image
        img = img.resize((width, height))
        
        # Convert to grayscale
        img = img.convert('L')
        
        # ASCII characters from darkest to lightest
        ascii_chars = '@%#*+=-:. '
        
        # Convert pixels to ASCII characters
        pixels = list(img.getdata())
        ascii_art = ''
        for i, pixel in enumerate(pixels):
            # Map pixel value (0-255) to ASCII character
            ascii_index = int(pixel * len(ascii_chars) / 256)
            ascii_art += ascii_chars[ascii_index]
            if (i + 1) % width == 0:
                ascii_art += '\n'
        
        return ascii_art
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python ascii_art_converter.py <image_path> [width] [height]")
        return
    
    image_path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    height = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    ascii_art = convert_to_ascii(image_path, width, height)
    print(ascii_art)
    
    # Optionally save to file
    save_option = input("Do you want to save the ASCII art to a file? (y/n): ")
    if save_option.lower() == 'y':
        output_file = input("Enter output file name (default: ascii_art.txt): ") or "ascii_art.txt"
        with open(output_file, 'w') as f:
            f.write(ascii_art)
        print(f"ASCII art saved to {output_file}")

if __name__ == "__main__":
    main()
