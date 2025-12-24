"""
System Information Detection Script
Detects and displays CPU, GPU, and RAM information
"""

import platform
import psutil
import subprocess
import sys

def get_cpu_info():
    """Get CPU information"""
    print("\n" + "="*50)
    print("CPU INFORMATION")
    print("="*50)
    
    # Processor name
    print(f"Processor: {platform.processor()}")
    
    # Physical cores
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    
    # Logical cores
    print(f"Logical cores: {psutil.cpu_count(logical=True)}")
    
    # CPU frequency
    cpu_freq = psutil.cpu_freq()
    print(f"Max Frequency: {cpu_freq.max:.2f} MHz")
    print(f"Min Frequency: {cpu_freq.min:.2f} MHz")
    print(f"Current Frequency: {cpu_freq.current:.2f} MHz")
    
    # CPU usage per core
    print(f"\nCPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"  Core {i}: {percentage}%")
    
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")


def get_ram_info():
    """Get RAM information"""
    print("\n" + "="*50)
    print("MEMORY (RAM) INFORMATION")
    print("="*50)
    
    # Get memory details
    svmem = psutil.virtual_memory()
    
    print(f"Total: {svmem.total / (1024**3):.2f} GB")
    print(f"Available: {svmem.available / (1024**3):.2f} GB")
    print(f"Used: {svmem.used / (1024**3):.2f} GB")
    print(f"Percentage: {svmem.percent}%")
    
    # Get swap memory
    swap = psutil.swap_memory()
    print(f"\nSwap Memory:")
    print(f"Total: {swap.total / (1024**3):.2f} GB")
    print(f"Used: {swap.used / (1024**3):.2f} GB")
    print(f"Free: {swap.free / (1024**3):.2f} GB")
    print(f"Percentage: {swap.percent}%")


def get_gpu_info():
    """Get GPU information"""
    print("\n" + "="*50)
    print("GPU INFORMATION")
    print("="*50)
    
    try:
        # Try to import GPUtil for NVIDIA GPUs
        import GPUtil
        gpus = GPUtil.getGPUs()
        
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"\nGPU {i}: {gpu.name}")
                print(f"  ID: {gpu.id}")
                print(f"  Load: {gpu.load*100:.1f}%")
                print(f"  Free Memory: {gpu.memoryFree} MB")
                print(f"  Used Memory: {gpu.memoryUsed} MB")
                print(f"  Total Memory: {gpu.memoryTotal} MB")
                print(f"  Temperature: {gpu.temperature}°C")
                print(f"  UUID: {gpu.uuid}")
        else:
            print("No NVIDIA GPU detected via GPUtil")
    except ImportError:
        print("GPUtil not installed. Install it with: pip install gputil")
    except Exception as e:
        print(f"Error detecting NVIDIA GPU: {e}")
    
    # Try alternative method using Windows command
    if platform.system() == "Windows":
        try:
            print("\n" + "-"*50)
            print("Attempting to detect GPU using WMIC...")
            print("-"*50)
            result = subprocess.run(
                ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for i, line in enumerate(lines[1:], 1):  # Skip header
                    if line.strip():
                        print(f"GPU {i}: {line.strip()}")
        except Exception as e:
            print(f"Error using WMIC: {e}")


def get_system_info():
    """Get general system information"""
    print("\n" + "="*50)
    print("SYSTEM INFORMATION")
    print("="*50)
    
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Architecture: {platform.architecture()[0]}")


def main():
    """Main function to display all system information"""
    print("\n" + "#"*50)
    print("# SYSTEM HARDWARE INFORMATION DETECTOR")
    print("#"*50)
    
    get_system_info()
    get_cpu_info()
    get_ram_info()
    get_gpu_info()
    
    print("\n" + "#"*50)
    print("# DETECTION COMPLETE")
    print("#"*50 + "\n")


if __name__ == "__main__":
    # Check if psutil is installed
    try:
        import psutil
    except ImportError:
        print("Error: psutil is not installed.")
        print("Install it with: pip install psutil")
        sys.exit(1)
    
    main()
