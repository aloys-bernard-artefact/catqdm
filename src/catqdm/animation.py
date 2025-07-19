#!/usr/bin/env python3
"""Cat animation module for catqdm library."""

import time
import os
import random
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.columns import Columns

class CatAnimation:
    """Library loading animation."""
    
    def __init__(self):
        self.console = Console()
        self.has_run = False
    
    def print_colored(self, text: str, color: str = "white", style: str = ""):
        """Print colored text if rich is available, otherwise regular print."""
        self.console.print(text, style=f"{color} {style}".strip())
    
    def clear_screen(self):
        """Clear the screen."""
        self.console.clear()
    
    def main_animation(self):
        """Two-stage animation with colors and effects."""
        stages = [
            ("🐱 Waking up the cat...", "bright_yellow", "bold"),
            ("😴 Stretching...", "cyan")
        ]
        
        # Sleeping animation frames
        sleeping_frames = [
            (r"""
          |\      _,,,---,,_
    ZZZzz /,`.-'`'    -.  ;-;;,_
         |,4-  ) )-,_. ,\ (  `'-'
        '---''(_/--'  `-'\_)   
    """, "dim blue"),
            (r"""
          |\      _,,,---,,_
    zzzZZ /,`.-'`'    -.  ;-;;,_
         |,4-  ) )-,_. ,\ (  `'-'
        '---''(_/--'  `-'\_)   
    """, "dim blue"),
            (r"""
          |\      _,,,---,,_
    ZZZzz /,`.-'`'    -.  ;-;;,_
         |,4-  ) )-,_. ,\ (  `'-'
        '---''(_/--'  `-'\_)   💤
    """, "dim blue")
        ]
        
        # Stretching animation frames
        stretching_frames = [
            (r"""
        |\__/,|   (`\
      _.|o o  |_   ) )
    -(((---(((--------
    """, "bright_green"),
            (r"""
        |\__/,|   (`\
      _.|^_^  |_   ) )
    -(((---(((--------
    """, "bright_green"),
            (r"""
        |\__/,|   (`\
      _.|^o^  |_   ) )
    -(((---(((--------
    """, "bright_green")
        ]
        

        
        # Final cat
        final_cat = (r"""
        |\__/,|   (`\
      _.|^_^  |_   ) )  ✨
    -(((---(((--------
    """, "bright_yellow")
        
        # Execute animation stages
        for i, (stage_text, color, *styles) in enumerate(stages):
            if i == 0:  # Sleeping stage
                for frame, frame_color in sleeping_frames:
                    self.clear_screen()
                    self.print_colored(stage_text, color, " ".join(styles))
                    self.print_colored(frame, frame_color)
                    time.sleep(0.4)
            elif i == 1:  # Stretching stage
                for frame, frame_color in stretching_frames:
                    self.clear_screen()
                    for j in range(i + 1):
                        prev_text, prev_color, *prev_styles = stages[j]
                        self.print_colored(prev_text, prev_color, " ".join(prev_styles))
                    self.print_colored(frame, frame_color)
                    time.sleep(0.3)
        
        self.clear_screen()
        self.print_colored("🎉 Cat is ready!", "bright_green", "bold")
        self.print_colored(final_cat[0], final_cat[1])
        time.sleep(0.3) 
        
        self._show_library_info()
        
        time.sleep(0.5)
    

    
    def _show_library_info(self):
        """Show library information."""
        table = Table(title="🐱 catqdm Library Loaded!", show_header=False, border_style="bright_green")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="bright_white")
        
        table.add_row("Version", "1.0.0")
        table.add_row("Status", "Ready to use! 🚀")
        table.add_row("Created by", "https://github.com/aloysbernard")

        
        self.console.print(table)
        print("\n")

    
    def run(self):
        """Run the animation."""
        self.main_animation()

def should_show_animation() -> bool:
    """Check if animation should be shown."""
    return os.getenv('CATQDM_ANIMATION', '').lower() != 'false'

def run_cat_animation():
    """Run the cat animation with current configuration."""
    if not should_show_animation():
        return
    
    if hasattr(run_cat_animation, '_has_run'):
        return
    run_cat_animation._has_run = True
    
    animation = CatAnimation()
    animation.run() 