import cv2
import numpy as np
import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp  # Updated import for better compatibility

# Check for CUDA availability at the start
use_cuda = False
try:
    if cv2.cuda.getCudaEnabledDeviceCount() > 0:
        use_cuda = True
        print("CUDA is available. Attempting to use GPU for OpenCV operations.")
    else:
        print("CUDA not available or OpenCV not built with CUDA support. Using CPU for OpenCV operations.")
except AttributeError:
    print("cv2.cuda module not found. Using CPU for OpenCV operations.")

def get_ascii_char(pixel_value):
    # ASCII characters from darkest to lightest
    ascii_chars = "@%#*+=-:. "
    # Map pixel value (0-255) to ASCII character
    index = int(pixel_value / 255 * (len(ascii_chars) - 1))
    return ascii_chars[index]

def frame_to_ascii(frame, width=100):
    # Calculate height to maintain aspect ratio
    aspect_ratio = frame.shape[1] / frame.shape[0]
    height = int(width / aspect_ratio / 2)  # Dividing by 2 because characters are taller than wide

    resized = None # Initialize resized variable

    if use_cuda:
        try:
            # Upload frame to GPU
            gpu_frame = cv2.cuda_GpuMat()
            gpu_frame.upload(frame)

            # Convert color on GPU
            gpu_gray = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)

            # Resize on GPU
            gpu_resized = cv2.cuda.resize(gpu_gray, (width, height))

            # Download result back to CPU
            resized = gpu_resized.download()

        except cv2.error as e:
            print(f"CUDA error during processing: {e}. Falling back to CPU for this frame.")
            # Fallback to CPU if CUDA operations fail for this frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (width, height))
        except Exception as e: # Catch other potential CUDA-related errors
             print(f"An unexpected error occurred with CUDA: {e}. Falling back to CPU for this frame.")
             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
             resized = cv2.resize(gray, (width, height))
    
    # If CUDA is not used or fallback occurred
    if resized is None:
        # CPU implementation
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (width, height))

    # Convert the pixels to ASCII characters
    ascii_frame = ""
    for row in resized:
        for pixel in row:
            ascii_frame += get_ascii_char(pixel)
        ascii_frame += "\n"
    
    return ascii_frame

def ascii_to_image(ascii_text, font_size=15, bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    # Calculate image dimensions based on ASCII text
    lines = ascii_text.split('\n')
    char_width = font_size / 2
    img_width = int(max(len(line) for line in lines) * char_width)
    img_height = int(len(lines) * font_size)
    
    # Create a new image
    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a monospace font (will fall back to default if not available)
    try:
        font = ImageFont.truetype("Courier", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw the ASCII art on the image
    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill=text_color)
        y += font_size
    
    return np.array(img)

def create_output_dir():
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def process_video(video_path, output_width=100, fps=None):
    print(f"Processing video: {video_path}")
    
    # Extract filename without extension
    video_filename = os.path.basename(video_path)
    video_name = os.path.splitext(video_filename)[0]
    
    # Create timestamp for unique output filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output directory
    output_dir = create_output_dir()
    
    # Output path for ASCII video
    output_path = os.path.join(output_dir, f"{video_name}_ascii_{timestamp}.mp4")
    
    # Load the video
    video_clip = mp.VideoFileClip(video_path)
    
    # Use original fps if not specified
    if fps is None:
        fps = video_clip.fps
    
    # Extract audio
    audio = video_clip.audio
    
    # Process frames and convert to ASCII images
    print("Converting frames to ASCII...")
    
    # Temporary list to store the ASCII frames
    ascii_frames = []
    
    # Get total number of frames for progress reporting
    total_frames = int(video_clip.duration * video_clip.fps)
    processed_frames = 0
    
    # Process each frame
    for frame in video_clip.iter_frames(fps=fps):
        # Convert frame to ASCII text (will use GPU if available and working)
        ascii_text = frame_to_ascii(frame, width=output_width)
        
        # Convert ASCII text to image
        ascii_image = ascii_to_image(ascii_text)
        
        # Add frame to list
        ascii_frames.append(ascii_image)
        
        # Update progress
        processed_frames += 1
        if processed_frames % 10 == 0:
            print(f"Processed {processed_frames}/{total_frames} frames ({processed_frames/total_frames*100:.1f}%)")
    
    print("Creating video from ASCII frames...")
    # Create a video from the ASCII frames
    ascii_clip = mp.ImageSequenceClip(ascii_frames, fps=fps)
    
    # Add the original audio to the ASCII video
    if audio is not None:
        ascii_clip = ascii_clip.set_audio(audio)
    
    # Write the result to file
    print(f"Writing ASCII video to {output_path}")
    ascii_clip.write_videofile(output_path, codec='libx264')
    
    # Clean up
    video_clip.close()
    if audio is not None:
        audio.close()
    ascii_clip.close()
    
    print(f"ASCII video saved to {output_path}")
    return output_path

def main():
    # Default sample video path
    default_video = os.path.join(os.path.dirname(os.path.dirname(__file__)), "videos", "sample1.mp4")
    
    # Get user input
    video_path = input(f"Enter path to video file (or press Enter to use sample: {default_video}): ")
    if not video_path:
        video_path = default_video
    
    if not os.path.exists(video_path):
        print(f"Error: File {video_path} not found.")
        return
    
    # Ask for ASCII width
    try:
        width = input("Enter ASCII width (default: 100): ")
        width = int(width) if width else 100
    except ValueError:
        print("Invalid input, using default width of 100")
        width = 100
    
    # Ask for FPS
    try:
        fps_input = input("Enter desired FPS (press Enter to use original): ")
        fps = int(fps_input) if fps_input else None
    except ValueError:
        print("Invalid input, using original FPS")
        fps = None
    
    # Process the video
    start_time = time.time()
    output_file = process_video(video_path, output_width=width, fps=fps)
    end_time = time.time()
    
    print(f"Processing completed in {end_time - start_time:.2f} seconds.")
    print(f"ASCII video saved to: {output_file}")

if __name__ == "__main__":
    main()