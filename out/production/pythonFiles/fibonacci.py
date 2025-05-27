import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

def generate_fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence

def fibonacci_spiral_animation(n=16, interval=500, save_gif=False):
    """Create an enhanced animated Fibonacci spiral with sequence visualization."""
    # Create custom colormap for better visual appeal
    colors = [(0.2, 0.4, 0.6), (0.4, 0.7, 0.9), (0.95, 0.5, 0.1), (0.9, 0.3, 0.3)]
    custom_cmap = LinearSegmentedColormap.from_list("fibonacci_colors", colors, N=n)
    
    # Generate complete Fibonacci sequence for the graph
    fibonacci_sequence = generate_fibonacci(n+5)
    
    # Set up the figure with grid layout - modified to remove the bar chart column
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
    
    # Spiral animation subplot - now takes full width
    ax_spiral = plt.subplot(gs[0, 0])
    ax_spiral.set_xlim(-150, 150)
    ax_spiral.set_ylim(-150, 150)
    ax_spiral.set_title('Fibonacci Spiral', fontsize=18, fontweight='bold')
    ax_spiral.axis('equal')
    ax_spiral.axis('off')
    
    # Golden ratio information subplot
    ax_info = plt.subplot(gs[1, 0])
    ax_info.axis('off')
    
    # Add title to the figure
    fig.suptitle('The Fibonacci Sequence & Golden Spiral', fontsize=22, fontweight='bold')
    
    # Initialize elements
    rectangles = []
    spirals = []
    text_artists = []
    
    def init():
        return []
    
    def animate(frame):
        # Clear previous frame elements
        for rect in rectangles:
            rect.remove()
        rectangles.clear()
        
        if spirals:
            spirals[0].remove()
        spirals.clear()
        
        for text in text_artists:
            text.remove()
        text_artists.clear()
        
        # Create Fibonacci sequence up to current frame
        fib_values = fibonacci_sequence[:frame+2]
        
        # Draw rectangles for the golden spiral
        x, y = 0, 0
        a, b = 0, 1
        
        # Add spiral center marker
        center_marker = ax_spiral.plot(0, 0, 'o', color='black', markersize=5)[0]
        rectangles.append(center_marker)
        
        for i in range(min(frame + 1, n)):
            color = custom_cmap(i/n)
            
            if i % 4 == 0:
                rect = patches.Rectangle((x, y), b, a, fill=False, 
                                        edgecolor=color, linewidth=2)
                x += b
            elif i % 4 == 1:
                rect = patches.Rectangle((x-a, y), a, b, fill=False, 
                                        edgecolor=color, linewidth=2)
                y += b
            elif i % 4 == 2:
                rect = patches.Rectangle((x-a-b, y), b, a, fill=False, 
                                        edgecolor=color, linewidth=2)
                x -= b
            else:
                rect = patches.Rectangle((x-a, y-a), a, b, fill=False, 
                                        edgecolor=color, linewidth=2)
                y -= b
            
            ax_spiral.add_patch(rect)
            rectangles.append(rect)
            
            # Add rectangle dimension text for better understanding
            size_text = ax_spiral.text(x-a/2, y-b/2, f"{b}×{a}", 
                                     ha='center', va='center', fontsize=8,
                                     color='black', alpha=0.7)
            text_artists.append(size_text)
            
            a, b = b, a+b
        
        # Draw the spiral for the current frame
        theta = np.linspace(0, (frame/2 + 1) * np.pi, 1000)
        golden_ratio = (1 + np.sqrt(5)) / 2
        r = golden_ratio ** (theta / np.pi)
        spiral, = ax_spiral.plot(r * np.cos(theta), r * np.sin(theta), color='red', linewidth=2.5)
        spirals.append(spiral)
        
        # Display golden ratio approximation
        if len(fib_values) >= 3:
            ratio_text = f"F({frame+1})/F({frame}) = {fib_values[-1]}/{fib_values[-2]} = {fib_values[-1]/fib_values[-2]:.6f}"
            golden_text = f"Golden Ratio (φ) = {(1 + np.sqrt(5))/2:.6f}"
            diff = abs((fib_values[-1]/fib_values[-2]) - (1 + np.sqrt(5))/2)
            accuracy = f"Difference: {diff:.6f}"
            
            # Add sequence display to info panel since we removed the bar chart
            sequence_text = f"Fibonacci Sequence: {', '.join(map(str, fib_values))}"
            
            info_text = ax_info.text(0.5, 0.5, 
                              f"{sequence_text}\n\n{ratio_text}\n{golden_text}\n{accuracy}\n\n"
                              f"As the sequence progresses, the ratio between consecutive\n"
                              f"Fibonacci numbers approaches the Golden Ratio (φ).",
                              ha='center', va='center', fontsize=12,
                              bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
            text_artists.append(info_text)
        
        # Add current frame info to spiral plot
        if frame >= 0:
            frame_text = ax_spiral.text(0.05, 0.95, 
                                     f"Step: {frame+1}\nCurrent Fibonacci: {fib_values[frame+1]}",
                                     transform=ax_spiral.transAxes, fontsize=12,
                                     verticalalignment='top',
                                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            text_artists.append(frame_text)
        
        # Combine all artists
        all_artists = rectangles + spirals + text_artists
        return all_artists
    
    # Set up animation with progress bar
    from tqdm import tqdm
    progress_bar = tqdm(total=n, desc="Generating animation")
    
    def update_progress(frame, *args):
        progress_bar.update(1)
        return animate(frame)
    
    # Limit the animation to exactly n frames (stopping at step 16 by default)
    anim = FuncAnimation(fig, update_progress, frames=range(n), 
                         init_func=init, blit=True,
                         interval=interval, repeat=False)  # Changed repeat to False to stop at the last frame
    
    # Add animation control buttons
    ax_buttons = plt.axes([0.81, 0.02, 0.1, 0.04])
    button_pause = plt.Button(ax_buttons, 'Pause/Play')
    
    def toggle_pause(event):
        if anim.event_source:
            if anim.event_source.running:
                anim.event_source.stop()
            else:
                anim.event_source.start()
    
    button_pause.on_clicked(toggle_pause)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to accommodate the title
    
    # Save animation if requested with error handling
    if save_gif:
        try:
            from datetime import datetime
            import os
            
            # Create output directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'fibonacci_spiral_{timestamp}.gif'
            filepath = os.path.join(output_dir, filename)
            
            # Save with progress indicator
            print(f"Saving animation to: {filepath}")
            anim.save(filepath, writer='pillow', fps=2, dpi=120)
            print(f"Animation saved successfully!")
        except Exception as e:
            print(f"Error saving animation: {str(e)}")
    
    # Close progress bar after animation is complete
    progress_bar.close()
    
    return fig, anim

if __name__ == "__main__":
    # Create and display animation - ensuring we stop at exactly step 16
    fig, anim = fibonacci_spiral_animation(n=16, interval=800, save_gif=True)
    
    plt.show()