import time
import os

os.environ['CATQDM_ANIMATION'] = 'true'

from catqdm import CatProgressBar

print("Method 1: Minimal Loading")
with CatProgressBar(100, "Processing files", unit="file", width=20) as pbar:
    for i in range(100):
        time.sleep(0.05)
        pbar.update(1)

print("Method 2: With Colored Postfix")
print("=== Method 1: Context manager with colored postfix ===")
with CatProgressBar(100, "Processing files", unit="file") as pbar:
    for i in range(100):
        if i < 33:
            pbar.set_postfix(color="yellow", size=f"{i*10}MB", status="reading")
        elif i < 66:
            pbar.set_postfix(color="blue", size=f"{i*10}MB", status="processing")
        else:
            pbar.set_postfix(color="green", size=f"{i*10}MB", status="finalizing")
        time.sleep(0.05)
        pbar.update(1)

print("\n=== Method 2: Unit scaling ===")
with CatProgressBar(10000, "Downloading", unit="B", unit_scale=True) as pbar:
    for i in range(10000):
        pbar.set_postfix(speed=f"{i*1000}B/s")
        time.sleep(0.001)
        pbar.update(1)

print("\n=== Method 3: Dynamic description and postfix with colors ===")
with CatProgressBar(50, "Initializing") as pbar:
    for i in range(50):
        if i == 10:
            pbar.set_description("Processing data", color="yellow")
            pbar.set_postfix(color="yellow", phase="data", progress="loading")
        elif i == 25:
            pbar.set_description("Saving results", color="orange3")
            pbar.set_postfix(color="orange3", phase="save", progress="writing")
        elif i == 40:
            pbar.set_description("Finalizing", color="green")
            pbar.set_postfix(color="green", phase="final", progress="complete")
        time.sleep(0.1)
        pbar.update(1)

print("\n=== Method 4: Custom unit with color themes ===")
with CatProgressBar(1000, "Training model", unit="epoch") as pbar:
    for i in range(1000):
        loss = 0.1 + i * 0.001
        accuracy = 0.8 + i * 0.0001
        
        # Change colors based on performance
        if loss > 0.8:
            color = "red"
        elif loss > 0.5:
            color = "yellow" 
        else:
            color = "green"
        
        pbar.set_postfix(color=color, loss=loss, accuracy=accuracy, epoch=i+1)
        time.sleep(0.01)
        pbar.update(1)

print("\n=== Method 5: Advanced postfix formatting with color themes ===")
with CatProgressBar(500, "Data processing", unit="batch") as pbar:
    for i in range(500):
        # Simulate different types of data
        memory_usage = 1024 + i * 2
        error_rate = 0.05 - i * 0.0001
        throughput = 1000 + i * 5
        
        # Dynamic color based on system health
        if error_rate > 0.03:
            color = "red"
            pbar.set_description("Data processing [HIGH ERRORS]", color="red")
        elif memory_usage > 1800:
            color = "yellow"
            pbar.set_description("Data processing [HIGH MEMORY]", color="yellow")
        else:
            color = "green"
            pbar.set_description("Data processing", color="cyan")
        
        pbar.set_postfix(
            color=color,
            memory=f"{memory_usage}MB",
            errors=f"{error_rate:.4f}",
            throughput=f"{throughput:,}",
            batch=i+1
        )
        time.sleep(0.02)
        pbar.update(1)
