#!/usr/bin/env python3
"""Rich Cat Progress Bar - Complex animated cat loading bars using Rich library.

Features:
- Multiple animated cats with different behaviors
- Colorful gradients and effects  
- Particle system simulation
- Multi-stage progress with different cat personalities
- Rich console integration with live updates
"""

import time
import random
from typing import Iterable, Sequence, Any, Iterator, Optional, List, Tuple
from concurrent.futures import ThreadPoolExecutor
import math

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.layout import Layout
from rich import box

# ---------------------------------------------------------------------------
# Cat Art and Animation Frames
# ---------------------------------------------------------------------------

class CatSprites:
    """Collection of cat sprites for different animation states."""
    
    # Sleeping cat (0-20%)
    SLEEPING = [
        """       /\\_/\\  
      ( o.o ) 
       > ^ <  
    zzZ  |_|  Zzz""",
        """       /\\_/\\  
      ( -.- ) 
       > ^ <  
   zzZ   |_|   Zzz""",
        """       /\\_/\\  
      ( u.u ) 
       > ^ <  
  zzZ    |_|    Zzz"""
    ]
    
    # Waking up cat (20-40%)
    WAKING = [
        """       /\\_/\\  
      ( O.O ) 
       > ^ <  
        |_|   """,
        """       /\\_/\\  
      ( @.@ ) 
       > ^ <  
        |_|   """,
        """       /\\_/\\  
      ( o.O ) 
       > ^ <  
        |_|   """
    ]
    
    # Alert cat (40-60%)
    ALERT = [
        """       /\\_/\\  
      ( ^.^ ) 
       > W <  
        |_|   """,
        """       /\\_/\\  
      ( ^o^ ) 
       > W <  
        |_|   """,
        """    /\\ /\\_/\\  
   (  ( ^.^ ) 
    \\ > W <  
      \\ |_|   """
    ]
    
    # Running cat (60-80%)
    RUNNING = [
        """    /\\_   /\\_/\\  
   /    ( >o< ) ~
  <      > < <   ~
   \\___   |_|  ~~""",
        """     /\\_/\\   _/\\
    ( >o< )   /
    > < <    <
     |_|   ~~~ \\___""",
        """  /\\  /\\_/\\     
 /  ( >o< )  \\  
<    > < <    >
 \\~~  |_|  ~~/  """
    ]
    
    # Flying/jumping cat (80-100%)
    FLYING = [
        """   ✨  /\\_/\\  ✨
  ✨  ( ^ω^ )  ✨
 ✨    > ◇ <    ✨
   ✨   |_|   ✨""",
        """  ⭐  /\\_/\\  ⭐
 ⭐   ( ^ω^ )   ⭐
⭐     > ◇ <     ⭐
  ⭐    |_|    ⭐""",
        """  🌟  /\\_/\\  🌟
 🌟   ( ^ω^ )   🌟
🌟     > ◇ <     🌟
  🌟    |_|    🌟"""
    ]

class ParticleSystem:
    """Simple particle system for visual effects."""
    
    def __init__(self, width: int = 50):
        self.width = width
        self.particles: List[Tuple[int, int, str]] = []
    
    def add_particle(self, x: int, y: int, char: str = "✨"):
        """Add a particle at position (x, y)."""
        self.particles.append((x, y, char))
    
    def update(self):
        """Update particle positions."""
        new_particles = []
        for x, y, char in self.particles:
            # Move particles randomly
            new_x = x + random.randint(-1, 1)
            new_y = y + random.randint(-1, 1)
            
            # Keep particles in bounds and remove old ones
            if 0 <= new_x < self.width and 0 <= new_y < 3 and random.random() > 0.3:
                new_particles.append((new_x, new_y, char))
        
        self.particles = new_particles
    
    def render(self, base_lines: List[str]) -> List[str]:
        """Render particles onto base lines."""
        lines = [list(line.ljust(self.width)) for line in base_lines]
        
        for x, y, char in self.particles:
            if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                lines[y][x] = char
        
        return [''.join(line) for line in lines]

def get_cat_animation(progress_pct: float, frame: int) -> Tuple[List[str], str]:
    """Get appropriate cat animation based on progress percentage."""
    
    if progress_pct < 20:
        # Sleeping phase
        sprites = CatSprites.SLEEPING
        color = "dim blue"
    elif progress_pct < 40:
        # Waking up phase
        sprites = CatSprites.WAKING
        color = "yellow"
    elif progress_pct < 60:
        # Alert phase
        sprites = CatSprites.ALERT
        color = "green"
    elif progress_pct < 80:
        # Running phase
        sprites = CatSprites.RUNNING
        color = "cyan"
    else:
        # Flying phase
        sprites = CatSprites.FLYING
        color = "magenta"
    
    sprite_idx = frame % len(sprites)
    sprite_lines = sprites[sprite_idx].split('\n')
    
    return sprite_lines, color

def create_rainbow_text(text: str, offset: int = 0) -> Text:
    """Create rainbow colored text."""
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    rich_text = Text()
    
    for i, char in enumerate(text):
        color_idx = (i + offset) % len(colors)
        rich_text.append(char, style=colors[color_idx])
    
    return rich_text

class CatProgressDisplay:
    """Rich-based cat progress display with multiple cats and effects."""
    
    def __init__(self, console: Console, width: int = 60):
        self.console = console
        self.width = width
        self.frame = 0
        self.particle_system = ParticleSystem(width)
        self.multiple_cats = True
    
    def create_main_cat_display(self, progress_pct: float) -> Panel:
        """Create the main cat animation panel."""
        cat_lines, color = get_cat_animation(progress_pct, self.frame)
        
        # Add particles during flying phase
        if progress_pct >= 80:
            # Add new particles randomly
            if random.random() > 0.7:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, 2)
                chars = ["✨", "⭐", "🌟", "💫"]
                self.particle_system.add_particle(x, y, random.choice(chars))
            
            self.particle_system.update()
            cat_lines = self.particle_system.render(cat_lines)
        
        # Create colored cat
        cat_text = Text()
        for line in cat_lines:
            cat_text.append(line + "\n", style=color)
        
        # Add position-based movement
        padding = int((progress_pct / 100) * 10)
        cat_text = Text(" " * padding) + cat_text
        
        title = f"Main Cat - {progress_pct:.1f}% Complete"
        if progress_pct >= 80:
            title = create_rainbow_text(title, self.frame)
        
        return Panel(
            Align.center(cat_text),
            title=title,
            border_style=color,
            box=box.ROUNDED
        )
    
    def create_mini_cats_display(self, progress_pct: float) -> Panel:
        """Create display with multiple smaller cats."""
        cats = []
        
        # Create 3 mini cats at different stages
        for i in range(3):
            cat_progress = max(0, progress_pct - (i * 20))
            if cat_progress > 0:
                mood_cats = ["( -.- )", "( o.o )", "( ^.^ )", "( >o< )", "( ^ω^ )"]
                cat_idx = min(int(cat_progress / 25), len(mood_cats) - 1)
                cat = mood_cats[cat_idx]
                
                # Color based on progress
                if cat_progress < 25:
                    color = "dim white"
                elif cat_progress < 50:
                    color = "yellow"
                elif cat_progress < 75:
                    color = "green"
                else:
                    color = "bright_magenta"
                
                cats.append(Text(cat, style=color))
            else:
                cats.append(Text("( z.z )", style="dim"))
        
        cat_line = Text(" " * 5).join(cats)
        
        return Panel(
            Align.center(cat_line),
            title="Cat Squad",
            border_style="bright_blue",
            box=box.SIMPLE
        )
    
    def create_progress_panel(self, progress_pct: float, current: int, total: int) -> Panel:
        """Create a custom progress panel."""
        # Create a visual progress bar using cats
        filled = int((progress_pct / 100) * 20)
        empty = 20 - filled
        
        bar_text = Text()
        
        # Filled portion with cats
        for i in range(filled):
            if i == filled - 1 and progress_pct < 100:
                # Leading cat
                bar_text.append("🐱", style="bright_yellow")
            else:
                bar_text.append("🐾", style="green")
        
        # Empty portion
        bar_text.append("░" * empty, style="dim")
        
        # Progress text
        progress_text = f"\n{current}/{total} ({progress_pct:.1f}%)"
        bar_text.append(progress_text, style="white")
        
        return Panel(
            Align.center(bar_text),
            title="Progress",
            border_style="green",
            box=box.SIMPLE
        )
    
    def update(self, progress_pct: float, current: int, total: int) -> Layout:
        """Update the entire display."""
        self.frame += 1
        
        layout = Layout()
        
        # Create main sections
        layout.split_column(
            Layout(name="header", size=8),
            Layout(name="body", size=6),
            Layout(name="footer", size=4)
        )
        
        # Split body into left and right
        layout["body"].split_row(
            Layout(name="main_cat"),
            Layout(name="progress")
        )
        
        # Populate sections
        layout["header"].update(self.create_main_cat_display(progress_pct))
        layout["main_cat"].update(self.create_mini_cats_display(progress_pct))
        layout["progress"].update(self.create_progress_panel(progress_pct, current, total))
        
        # Footer with status
        if progress_pct < 20:
            status = Text("😴 Cats are sleeping...", style="dim blue")
        elif progress_pct < 40:
            status = Text("😸 Cats are waking up!", style="yellow")
        elif progress_pct < 60:
            status = Text("😺 Cats are alert and ready!", style="green")
        elif progress_pct < 80:
            status = Text("🏃‍♂️ Cats are running!", style="cyan")
        else:
            status = create_rainbow_text("🚀 CATS ARE FLYING! ✨", self.frame)
        
        layout["footer"].update(Panel(Align.center(status), box=box.SIMPLE))
        
        return layout

def rich_cat_bar(
    iterable: Iterable[Any],
    *,
    desc: str = "Processing with Cats",
    console: Optional[Console] = None,
    refresh_rate: float = 10.0,
    width: int = 60,
    **kwargs
) -> Iterator[Any]:
    """
    Rich-based complex cat progress bar with animations and effects.
    
    Parameters
    ----------
    iterable : Iterable[Any]
        The iterable to process
    desc : str
        Description for the progress bar
    console : Optional[Console]
        Rich console instance (creates new one if None)
    refresh_rate : float
        Display refresh rate (Hz)
    width : int
        Display width for animations
    **kwargs
        Additional arguments (currently unused)
    
    Yields
    ------
    Any
        Items from the iterable
    """
    if console is None:
        console = Console()
    
    # Get total length
    try:
        total = len(iterable)
    except TypeError:
        total = None
    
    if total is None:
        # For unknown length iterables, just show a spinning cat
        with Live(console=console, refresh_per_second=refresh_rate) as live:
            spinner_cats = ["(=^.^=)", "(=^o^=)", "(=^_^=)", "(=^-^=)"]
            for i, item in enumerate(iterable):
                cat = spinner_cats[i % len(spinner_cats)]
                live.update(Panel(
                    Align.center(Text(f"{cat}\n{desc}\nItem #{i+1}", style="cyan")),
                    title="Processing...",
                    border_style="cyan"
                ))
                yield item
                time.sleep(1.0 / refresh_rate)
        return
    
    # Known length - full animation
    display = CatProgressDisplay(console, width)
    
    with Live(console=console, refresh_per_second=refresh_rate) as live:
        for i, item in enumerate(iterable):
            progress_pct = ((i + 1) / total) * 100
            layout = display.update(progress_pct, i + 1, total)
            live.update(layout)
            
            yield item
            
            # Small delay for animation smoothness
            time.sleep(1.0 / refresh_rate)
    
    # Final celebration
    console.print("\n")
    console.print(Panel(
        Align.center(create_rainbow_text("🎉 ALL CATS HAVE COMPLETED THEIR MISSION! 🎉", 0)),
        title="SUCCESS!",
        border_style="bright_green",
        box=box.DOUBLE
    ))

# ---------------------------------------------------------------------------
# Advanced Multi-Stage Cat Loading
# ---------------------------------------------------------------------------

def multi_stage_cat_loading(
    stages: List[Tuple[str, int]],
    *,
    console: Optional[Console] = None,
    total_time: float = 10.0
) -> None:
    """
    Multi-stage loading animation with different cat behaviors per stage.
    
    Parameters
    ----------
    stages : List[Tuple[str, int]]
        List of (stage_name, weight) pairs
    console : Optional[Console]
        Rich console instance
    total_time : float
        Total time for all stages
    """
    if console is None:
        console = Console()
    
    total_weight = sum(weight for _, weight in stages)
    
    with Live(console=console, refresh_per_second=10) as live:
        elapsed_time = 0
        
        for stage_name, weight in stages:
            stage_duration = (weight / total_weight) * total_time
            stage_steps = int(stage_duration * 10)  # 10 steps per second
            
            for step in range(stage_steps):
                stage_progress = (step + 1) / stage_steps
                overall_progress = (elapsed_time + stage_progress * stage_duration) / total_time
                
                # Create stage-specific animation
                cat_lines, color = get_cat_animation(overall_progress * 100, step)
                
                cat_text = Text()
                for line in cat_lines:
                    cat_text.append(line + "\n", style=color)
                
                # Stage progress bar
                stage_bar_filled = int(stage_progress * 20)
                stage_bar = "█" * stage_bar_filled + "░" * (20 - stage_bar_filled)
                
                # Overall progress bar  
                overall_bar_filled = int(overall_progress * 20)
                overall_bar = "█" * overall_bar_filled + "░" * (20 - overall_bar_filled)
                
                content = Table.grid()
                content.add_row(Align.center(cat_text))
                content.add_row("")
                content.add_row(f"Current Stage: {stage_name}")
                content.add_row(f"Stage Progress: {stage_bar} {stage_progress*100:.1f}%")
                content.add_row(f"Overall Progress: {overall_bar} {overall_progress*100:.1f}%")
                
                live.update(Panel(
                    content,
                    title=f"Multi-Stage Cat Loading",
                    border_style=color,
                    box=box.ROUNDED
                ))
                
                time.sleep(0.1)
            
            elapsed_time += stage_duration

# ---------------------------------------------------------------------------
# Demo Functions
# ---------------------------------------------------------------------------

def demo_basic_rich_cat():
    """Demo the basic rich cat progress bar."""
    console = Console()
    console.print(Panel(
        "Starting Rich Cat Progress Bar Demo!",
        title="Demo",
        style="bold green"
    ))
    
    # Demo with range
    for _ in rich_cat_bar(range(50), desc="Processing files", refresh_rate=15):
        time.sleep(0.1)

def demo_multi_stage():
    """Demo the multi-stage cat loading."""
    console = Console()
    console.print(Panel(
        "Starting Multi-Stage Cat Loading Demo!",
        title="Demo",
        style="bold blue"
    ))
    
    stages = [
        ("Initializing cats", 1),
        ("Loading cat database", 3),
        ("Training cats", 4),
        ("Deploying cats", 2),
        ("Finalizing", 1)
    ]
    
    multi_stage_cat_loading(stages, console=console, total_time=8.0)

if __name__ == "__main__":
    console = Console()
    
    console.print("[bold magenta]🐱 Rich Cat Progress Bar Demos 🐱[/bold magenta]\n")
    
    # Run basic demo
    demo_basic_rich_cat()
    
    time.sleep(2)
    
    # Run multi-stage demo
    demo_multi_stage()
    
    console.print("\n[bold green]All demos completed! 🎉[/bold green]") 