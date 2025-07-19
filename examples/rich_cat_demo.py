#!/usr/bin/env python3
"""
Rich Cat Progress Bar Demo - Showcase complex cat loading animations.

This script demonstrates various rich cat progress bars including:
- Basic rich cat progress with multi-stage animations
- Multi-stage loading with different cat behaviors
- Particle effects and rainbow animations
- Multiple cats working together
"""

import time
import random
from pathlib import Path
import sys

# Add the src directory to the path so we can import catqdm
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

from catqdm.rich_cat_bar import rich_cat_bar, multi_stage_cat_loading, demo_basic_rich_cat, demo_multi_stage
from catqdm.rich_cat_bar import CatProgressDisplay

def demo_file_processing():
    """Demo simulating file processing with cats."""
    console = Console()
    
    console.print(Panel(
        Align.center(Text("🗂️  File Processing Demo with Cats  🗂️", style="bold cyan")),
        title="Demo 1",
        border_style="cyan",
        box=box.DOUBLE
    ))
    
    # Simulate processing different types of files
    files = [
        "config.json", "data.csv", "image1.jpg", "image2.png", "video.mp4",
        "document.pdf", "script.py", "style.css", "index.html", "database.db",
        "backup.zip", "logs.txt", "readme.md", "package.json", "requirements.txt"
    ]
    
    for file in rich_cat_bar(files, desc="Processing files", refresh_rate=12):
        # Simulate different processing times for different file types
        if file.endswith(('.jpg', '.png', '.mp4')):
            time.sleep(0.2)  # Images/videos take longer
        elif file.endswith(('.zip', '.db')):
            time.sleep(0.15)  # Archives and databases
        else:
            time.sleep(0.1)  # Text files are quick

def demo_data_analysis():
    """Demo simulating data analysis pipeline."""
    console = Console()
    
    console.print(Panel(
        Align.center(Text("📊  Data Analysis Pipeline  📊", style="bold green")),
        title="Demo 2", 
        border_style="green",
        box=box.DOUBLE
    ))
    
    # Multi-stage data analysis
    stages = [
        ("Loading datasets", 2),
        ("Data cleaning", 3),
        ("Feature extraction", 4),
        ("Model training", 5),
        ("Validation", 2),
        ("Generating reports", 1),
    ]
    
    multi_stage_cat_loading(stages, total_time=12.0)

def demo_network_download():
    """Demo simulating network download with varying speeds."""
    console = Console()
    
    console.print(Panel(
        Align.center(Text("🌐  Network Download Simulation  🌐", style="bold blue")),
        title="Demo 3",
        border_style="blue", 
        box=box.DOUBLE
    ))
    
    # Simulate downloading chunks with varying delays
    chunks = list(range(100))
    
    for chunk in rich_cat_bar(chunks, desc="Downloading data", refresh_rate=20):
        # Simulate network variability
        delay = random.uniform(0.05, 0.15)
        time.sleep(delay)

def demo_batch_processing():
    """Demo simulating batch job processing."""
    console = Console()
    
    console.print(Panel(
        Align.center(Text("⚙️  Batch Job Processing  ⚙️", style="bold magenta")),
        title="Demo 4",
        border_style="magenta",
        box=box.DOUBLE
    ))
    
    # Simulate processing batch jobs
    jobs = [f"Job-{i:03d}" for i in range(1, 31)]
    
    for job in rich_cat_bar(jobs, desc="Processing batch jobs", refresh_rate=15):
        # Some jobs take longer than others
        if int(job.split('-')[1]) % 7 == 0:  # Every 7th job is slower
            time.sleep(0.3)
        else:
            time.sleep(0.1)

def demo_ai_training():
    """Demo simulating AI model training."""
    console = Console()
    
    console.print(Panel(
        Align.center(Text("🤖  AI Model Training  🤖", style="bold yellow")),
        title="Demo 5",
        border_style="yellow",
        box=box.DOUBLE
    ))
    
    # Multi-stage AI training process
    stages = [
        ("Initializing model", 1),
        ("Loading training data", 2),
        ("Epoch 1/5", 3),
        ("Epoch 2/5", 3),
        ("Epoch 3/5", 3),
        ("Epoch 4/5", 3),
        ("Epoch 5/5", 3),
        ("Validation", 2),
        ("Saving model", 1),
    ]
    
    multi_stage_cat_loading(stages, total_time=15.0)

def demo_system_deployment():
    """Demo simulating system deployment."""
    console = Console()
    
    console.print(Panel(
        Align.center(Text("🚀  System Deployment  🚀", style="bold red")),
        title="Demo 6",
        border_style="red",
        box=box.DOUBLE
    ))
    
    # Deployment stages
    stages = [
        ("Building application", 3),
        ("Running tests", 2),
        ("Creating containers", 2),
        ("Pushing to registry", 2),
        ("Deploying to staging", 3),
        ("Health checks", 1),
        ("Deploying to production", 2),
        ("Final verification", 1),
    ]
    
    multi_stage_cat_loading(stages, total_time=10.0)

def interactive_demo():
    """Interactive demo where user can choose what to run."""
    console = Console()
    
    console.print(Panel(
        Align.center(Text("🐱  Interactive Rich Cat Demo  🐱", style="bold rainbow")),
        title="Welcome!",
        border_style="bright_magenta",
        box=box.DOUBLE
    ))
    
    demos = [
        ("File Processing", demo_file_processing),
        ("Data Analysis Pipeline", demo_data_analysis), 
        ("Network Download", demo_network_download),
        ("Batch Processing", demo_batch_processing),
        ("AI Training", demo_ai_training),
        ("System Deployment", demo_system_deployment),
    ]
    
    console.print("\nAvailable demos:")
    for i, (name, _) in enumerate(demos, 1):
        console.print(f"{i}. {name}")
    
    console.print("\nChoose a demo (1-6) or press Enter to run all:")
    
    try:
        choice = input().strip()
        if choice == "":
            # Run all demos
            for name, demo_func in demos:
                console.print(f"\n[bold]Running: {name}[/bold]")
                demo_func()
                time.sleep(1)
        else:
            choice_num = int(choice)
            if 1 <= choice_num <= len(demos):
                name, demo_func = demos[choice_num - 1]
                console.print(f"\n[bold]Running: {name}[/bold]")
                demo_func()
            else:
                console.print("[red]Invalid choice![/red]")
    except (ValueError, KeyboardInterrupt):
        console.print("\n[yellow]Demo cancelled.[/yellow]")

def main():
    """Main demo function."""
    console = Console()
    
    # Show title
    console.print("\n" * 2)
    console.print(Panel(
        Align.center(Text(
            "🐱✨ RICH CAT PROGRESS BAR DEMO ✨🐱\n\n"
            "Experience complex loading animations with cats!\n"
            "Featuring particle effects, rainbow colors, and multi-stage progress.",
            style="bold bright_blue"
        )),
        title="CatQDM Rich Demo",
        subtitle="Press Ctrl+C to stop any demo",
        border_style="bright_blue",
        box=box.DOUBLE_EDGE
    ))
    
    time.sleep(1)
    
    # Run interactive demo
    interactive_demo()
    
    # Final message
    console.print("\n")
    console.print(Panel(
        Align.center(Text("🎉 Thank you for trying Rich Cat Progress Bars! 🎉", style="bold green")),
        title="Demo Complete",
        border_style="bright_green",
        box=box.DOUBLE
    ))

if __name__ == "__main__":
    main() 