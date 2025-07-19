#!/usr/bin/env python3
"""
Simple Rich Cat Demo - Quick test of the rich cat progress bars.
"""

import time
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from catqdm.rich_cat_bar import rich_cat_bar, multi_stage_cat_loading

def main():
    print("🐱 Starting Rich Cat Demo! 🐱\n")
    
    # Demo 1: Basic rich cat progress bar
    print("Demo 1: File processing with animated cats")
    
    for file in rich_cat_bar(range(100), desc="Processing files", sleep_per=0.1):
        time.sleep(0.5)  # Simulate processing time
    
    time.sleep(1)
    
    # Demo 2: Multi-stage loading
    print("\nDemo 2: Multi-stage cat loading")
    stages = [
        ("Waking up cats", 5),
        ("Loading cat data", 7),
        ("Training cats", 10),
        ("Cat deployment", 5),
    ]
    
    multi_stage_cat_loading(stages, total_time=6.0)
    
    print("\n🎉 Rich Cat Demo Complete! 🎉")

if __name__ == "__main__":
    main() 