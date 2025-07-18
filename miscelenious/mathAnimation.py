import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import hsv_to_rgb

class MathematicalArtGenerator:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.t = 0
        self.dt = np.pi / 240  # Time step
        
        # Setup the plot
        self.fig, self.ax = plt.subplots(figsize=(12, 9), facecolor='black')
        self.ax.set_facecolor('black')
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # Initialize empty line plot
        self.line, = self.ax.plot([], [], 'o', markersize=0.5, alpha=0.7)
        
        # Store points for trailing effect
        self.points_history = []
        self.max_history = 5
        
    def mag(self, x, y):
        """Calculate magnitude of vector (x, y)"""
        return np.sqrt(x**2 + y**2)
    
    def calculate_point(self, x, y):
        """
        Mathematical art function based on the original code:
        a=(x,y,d=mag(k=(4+sin(y*2-t)*3)*cos(x/29),e=y/8-13))=>
        point((q=3*sin(k*2)+.3/k+sin(y/25)*k*(9+4*sin(e*9-d*3+t*2)))+30*cos(c=d-t)+200,
        q*sin(c)+d*39-220)
        """
        # Calculate k and e
        k = (4 + np.sin(y * 2 - self.t) * 3) * np.cos(x / 29)
        e = y / 8 - 13
        
        # Calculate d (magnitude)
        d = self.mag(k, e)
        
        # Calculate q (complex expression)
        q = (3 * np.sin(k * 2) + 
             0.3 / (k + 0.01) +  # Add small value to avoid division by zero
             np.sin(y / 25) * k * (9 + 4 * np.sin(e * 9 - d * 3 + self.t * 2)))
        
        # Calculate c
        c = d - self.t
        
        # Calculate final coordinates
        px = q + 30 * np.cos(c) + 200
        py = q * np.sin(c) + d * 39 - 220
        
        return px, py
    
    def generate_frame(self):
        """Generate points for current frame"""
        x_coords = []
        y_coords = []
        
        # Generate points similar to the original loop
        iterations = 10000
        for i in range(iterations):
            x = (i / 235) % self.width
            y = (i / 200) % self.height
            
            px, py = self.calculate_point(x, y)
            
            # Only add points within canvas bounds
            if 0 <= px < self.width and 0 <= py < self.height:
                x_coords.append(px)
                y_coords.append(py)
        
        return np.array(x_coords), np.array(y_coords)
    
    def animate(self, frame):
        """Animation function for matplotlib"""
        # Generate new points
        x_coords, y_coords = self.generate_frame()
        
        # Calculate color based on time (cycling through hues)
        hue = (self.t * 0.1) % 1.0
        color = hsv_to_rgb([hue, 0.7, 0.9])
        
        # Update the plot
        self.line.set_data(x_coords, y_coords)
        self.line.set_color(color)
        
        # Update time
        self.t += self.dt
        
        # Set title with current time
        self.ax.set_title(f'Mathematical Art - t = {self.t:.2f}', 
                         color='white', fontsize=14, pad=20)
        
        return self.line,
    
    def static_plot(self, t_value=0):
        """Create a static plot at a specific time"""
        self.t = t_value
        x_coords, y_coords = self.generate_frame()
        
        # Calculate color
        hue = (self.t * 0.1) % 1.0
        color = hsv_to_rgb([hue, 0.7, 0.9])
        
        # Plot
        self.ax.clear()
        self.ax.set_facecolor('black')
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        self.ax.scatter(x_coords, y_coords, s=0.5, c=[color], alpha=0.7)
        self.ax.set_title(f'Mathematical Art - t = {self.t:.2f}', 
                         color='white', fontsize=14, pad=20)
        
        plt.tight_layout()
        return self.fig
    
    def create_animation(self, frames=500, interval=50):
        """Create and return animation object"""
        anim = animation.FuncAnimation(
            self.fig, self.animate, frames=frames, 
            interval=interval, blit=True, repeat=True
        )
        return anim

# Usage examples:

# 1. Static plot
def create_static_plot():
    """Create a static version of the mathematical art"""
    generator = MathematicalArtGenerator()
    fig = generator.static_plot(t_value=5.0)  # You can change t_value
    plt.show()
    return fig

# 2. Animated plot
def create_animated_plot():
    """Create an animated version"""
    generator = MathematicalArtGenerator()
    anim = generator.create_animation(frames=1000, interval=50)
    plt.show()
    return anim

# 3. Save multiple frames
def save_frames():
    """Save multiple frames as images"""
    generator = MathematicalArtGenerator()
    
    # Save frames at different time values
    time_values = np.linspace(0, 20, 10)
    
    for i, t_val in enumerate(time_values):
        fig = generator.static_plot(t_value=t_val)
        plt.savefig(f'math_art_frame_{i:03d}.png', 
                   facecolor='black', dpi=150, bbox_inches='tight')
        plt.close()
    
    print(f"Saved {len(time_values)} frames")

# 4. Create high-resolution version
def create_high_res_plot():
    """Create a high-resolution static plot"""
    generator = MathematicalArtGenerator(width=1600, height=1200)
    fig = generator.static_plot(t_value=10.0)
    plt.savefig('math_art_high_res.png', 
               facecolor='black', dpi=300, bbox_inches='tight')
    plt.show()
    return fig

if __name__ == "__main__":
    print("Mathematical Art Generator")
    print("by yuruyurau - Python implementation")
    print("\nChoose an option:")
    print("1. Static plot")
    print("2. Animated plot")
    print("3. Save multiple frames")
    print("4. High-resolution plot")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        create_static_plot()
    elif choice == "2":
        create_animated_plot()
    elif choice == "3":
        save_frames()
    elif choice == "4":
        create_high_res_plot()
    else:
        print("Invalid choice. Creating static plot...")
        create_static_plot()