import os
import math
import time
import numpy as np

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_frame(A, B):
    # Precompute sines and cosines of A and B
    cosA, sinA = math.cos(A), math.sin(A)
    cosB, sinB = math.cos(B), math.sin(B)
    
    # Screen dimensions
    width, height = 80, 24
    
    # Buffer for the output
    output = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Z-buffer for depth
    zbuffer = [[0 for _ in range(width)] for _ in range(height)]
    
    # Donut parameters
    R1 = 1    # Distance from center to center of torus tube
    R2 = 2    # Radius of torus tube
    K2 = 5    # Distance from viewer to donut
    K1 = width * K2 * 3 / (8 * (R1 + R2))  # Scaling factor
    
    # Rotation around the y-axis (vertical)
    for theta in np.linspace(0, 2 * math.pi, 50):
        cosTheta, sinTheta = math.cos(theta), math.sin(theta)
        
        # Rotation around the x-axis (horizontal)
        for phi in np.linspace(0, 2 * math.pi, 20):
            cosPhi, sinPhi = math.cos(phi), math.sin(phi)
            
            # 3D coordinates of the point on the torus
            x = R2 * cosTheta + R1
            y = R2 * sinTheta
            
            # 3D rotation
            x1 = x * cosB - y * sinB
            y1 = x * sinB + y * cosB
            z1 = R2 * cosPhi + R1
            
            # Rotate around x-axis
            y2 = y1 * cosA - z1 * sinA
            z2 = y1 * sinA + z1 * cosA
            
            # 3D to 2D projection
            z = 1 / (K2 + z2)
            x3 = int(width / 2 + K1 * x1 * z)
            y3 = int(height / 2 - K1 * y2 * z)
            
            # Calculate luminance
            L = cosPhi * cosTheta * sinB - cosA * cosTheta * sinPhi - sinA * sinTheta + cosB * (cosA * sinTheta - cosTheta * sinA * sinPhi)
            
            # Only render if point is visible and in front of previous points
            if 0 <= x3 < width and 0 <= y3 < height and z > zbuffer[y3][x3]:
                zbuffer[y3][x3] = z
                luminance_index = int(L * 8)
                # ASCII chars by increasing luminance
                chars = '.,-~:;=!*#$@'
                output[y3][x3] = chars[max(0, min(luminance_index, len(chars) - 1))]
    
    # Render the frame
    result = '\n'.join(''.join(row) for row in output)
    clear_screen()
    print(result)

def main():
    A = 0
    B = 0
    try:
        while True:
            render_frame(A, B)
            A += 0.07
            B += 0.03
            time.sleep(0.03)
    except KeyboardInterrupt:
        print("Animation stopped")

if __name__ == "__main__":
    main()
