from rich.console import Console
from rich.text import Text
from rich.live import Live
import time
from typing import Optional, Any, Iterator, Dict
from datetime import datetime, timedelta
from catqdm.utils.notebook import _in_notebook
class CatProgressBar:
    """A functional progress bar with cat emojis."""
    
    def __init__(self, 
                 total: int, 
                 description: str = "Progress", 
                 width: int = None,
                 unit: str = "it",
                 unit_scale: bool = False,
                 unit_divisor: int = 1000,
                 postfix: Dict[str, Any] = None,
                 bar_format: str = None):
        self.total = total
        self.current = 0
        self.description = description
        self.unit = unit
        self.unit_scale = unit_scale
        self.unit_divisor = unit_divisor
        self.postfix = postfix or {}
        self.bar_format = bar_format
        self.desc_color = "cyan"
        self.postfix_color = "bright_black"
        self.console = Console()
        self.live = None
        self.start_time = None
        self.last_update_time = None
        self.in_notebook = _in_notebook()
        self.display_handle = None
        
        if width is None:
            try:
                width = self.console.width - 20
            except:
                width = 80
        self.width = width
        
    def __enter__(self):
        """Context manager entry."""
        self.start_time = datetime.now()
        self.last_update_time = self.start_time
        
        if self.in_notebook:
            try:
                from IPython.display import display, HTML
                initial_display = self._create_html_display()
                self.display_handle = display(HTML(initial_display), display_id=True)
            except ImportError:
                self.live = Live(self._create_display(), console=self.console, refresh_per_second=10)
                self.live.start()
        else:
            self.live = Live(self._create_display(), console=self.console, refresh_per_second=10)
            self.live.start()
        
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.live:
            self.live.stop()
            
    def _format_number(self, n: float) -> str:
        """Format number with unit scaling if enabled."""
        if not self.unit_scale:
            return f"{n:.0f}"
        
        for unit in ['', 'K', 'M', 'G', 'T']:
            if n < self.unit_divisor:
                return f"{n:.1f}{unit}"
            n /= self.unit_divisor
        return f"{n:.1f}P"
    
    def _create_html_display(self) -> str:
        """Create HTML display for Jupyter notebooks."""
        if self.total == 0:
            progress_pct = 0
        else:
            progress_pct = (self.current / self.total) * 100
            
        bar_width = 20
            
        filled = int((progress_pct / 100) * bar_width)
        empty = bar_width - filled

        html_parts = []
        
        # Description
        html_parts.append(f'<span style="color: cyan; font-weight: bold;">{self.description}: </span>')
        
        # Progress bar
        for i in range(bar_width):
            if i < filled:
                if i == filled - 1 and progress_pct < 100:
                    html_parts.append('<span style="color: yellow; font-weight: bold;">🐱</span>')
                else:
                    html_parts.append('<span style="color: green;">🐾</span>')
            else:
                html_parts.append('<span style="color: #666;">░</span>')
        
        # Metrics
        metrics = self._get_metrics()
        html_parts.append(f' <span style="color: white;">{metrics}</span>')
        
        # Postfix
        if self.postfix:
            postfix_parts = []
            for k, v in self.postfix.items():
                if k == "_color":
                    continue
                if isinstance(v, float):
                    formatted_v = f"{v:.3f}" if abs(v) < 100 else f"{v:.1f}"
                elif isinstance(v, int) and v > 1000:
                    formatted_v = f"{v:,}"
                else:
                    formatted_v = str(v)
                postfix_parts.append(f"{k}={formatted_v}")
            
            postfix_str = ", ".join(postfix_parts)
            postfix_color = self.postfix.get("_color", "#888")
            html_parts.append(f' <span style="color: {postfix_color};">| {postfix_str}</span>')
        
        return f'<pre style="margin:0;line-height:1.1;">{"".join(html_parts)}</pre>'
    
    def _create_display(self) -> Text:
        """Create the tqdm-like display."""
        if self.total == 0:
            progress_pct = 0
        else:
            progress_pct = (self.current / self.total) * 100
            
        bar_width = 20
            
        filled = int((progress_pct / 100) * bar_width)
        empty = bar_width - filled

        display = Text()
        
        display.append(f"{self.description}: ", style=self.desc_color)
        
        for i in range(bar_width):
            if i < filled:
                if i == filled - 1 and progress_pct < 100:
                    display.append("🐱", style="bright_yellow")
                else:
                    display.append("🐾", style="green")
            else:
                display.append("░", style="dim")
        
        # Metrics
        metrics = self._get_metrics()
        display.append(f" {metrics}", style="white")
        
        # Postfix
        if self.postfix:
            postfix_parts = []
            for k, v in self.postfix.items():
                if k == "_color":
                    continue
                if isinstance(v, float):
                    formatted_v = f"{v:.3f}" if abs(v) < 100 else f"{v:.1f}"
                elif isinstance(v, int) and v > 1000:
                    formatted_v = f"{v:,}"
                else:
                    formatted_v = str(v)
                postfix_parts.append(f"{k}={formatted_v}")
            
            postfix_str = ", ".join(postfix_parts)
            postfix_color = self.postfix.get("_color", self.postfix_color)
            display.append(f" | {postfix_str}", style=postfix_color)
        
        return display
        
    def _get_metrics(self) -> str:
        """Get progress metrics like tqdm."""
        if self.total == 0:
            return f"0/0 (0.0%)"
            
        progress_pct = (self.current / self.total) * 100
        
        current_str = self._format_number(self.current)
        total_str = self._format_number(self.total)
        
        metrics = f"{current_str}/{total_str} ({progress_pct:.1f}%)"
        
        if self.start_time and self.current > 0:
            elapsed = datetime.now() - self.start_time
            rate = self.current / elapsed.total_seconds()
            if rate > 0:
                eta_seconds = (self.total - self.current) / rate
                eta = timedelta(seconds=int(eta_seconds))
                elapsed_str = str(elapsed).split('.')[0]  
                eta_str = str(eta).split('.')[0]
                rate_str = self._format_number(rate)
                metrics += f" [{elapsed_str}<{eta_str}, {rate_str}{self.unit}/s]"
            else:
                elapsed_str = str(elapsed).split('.')[0]
                metrics += f" [{elapsed_str}, ?{self.unit}/s]"
        
        return metrics
        
    def update(self, n: int = 1):
        """Update the progress by n steps."""
        self.current = min(self.current + n, self.total)
        self.last_update_time = datetime.now()
        
        if self.in_notebook and self.display_handle:
            try:
                from IPython.display import HTML
                self.display_handle.update(HTML(self._create_html_display()))
            except Exception:
                # Fallback to console if update fails
                if self.live:
                    self.live.update(self._create_display())
        elif self.live:
            self.live.update(self._create_display())
            
    def set_description(self, description: str, color: str = None):
        """Set the description of the progress bar with optional color.
        
        Args:
            description: New description text
            color: Color for the description text (e.g., "green", "red", "yellow", "blue", "magenta")
        """
        self.description = description
        if color:
            self.desc_color = color
        self._update_display()
            
    def set_postfix(self, color: str = None, **kwargs):
        """Set postfix information with optional color (like tqdm.set_postfix).
        
        Args:
            color: Color for the postfix text (e.g., "green", "red", "yellow", "blue", "magenta")
            **kwargs: Key-value pairs to display in postfix
        """
        if color:
            kwargs["_color"] = color
        self.postfix.update(kwargs)
        self._update_display()
            
    def set_postfix_str(self, s: str):
        """Set postfix string directly."""
        self.postfix = {"info": s}
        self._update_display()
            
    def set_postfix_dict(self, postfix_dict: Dict[str, Any]):
        """Set postfix from a dictionary with automatic formatting."""
        self.postfix = postfix_dict
        self._update_display()
    
    def _update_display(self):
        """Update the display based on environment."""
        if self.in_notebook and self.display_handle:
            try:
                from IPython.display import HTML
                self.display_handle.update(HTML(self._create_html_display()))
            except Exception:
                if self.live:
                    self.live.update(self._create_display())
        elif self.live:
            self.live.update(self._create_display())
            
    def __iter__(self) -> Iterator[int]:
        """Make the progress bar iterable."""
        self.start_time = datetime.now()
        self.last_update_time = self.start_time
        
        if self.in_notebook:
            try:
                from IPython.display import display, HTML
                initial_display = self._create_html_display()
                self.display_handle = display(HTML(initial_display), display_id=True)
            except ImportError:
                self.live = Live(self._create_display(), console=self.console, refresh_per_second=10)
                self.live.start()
        else:
            self.live = Live(self._create_display(), console=self.console, refresh_per_second=10)
            self.live.start()
        
        try:
            for i in range(self.total):
                yield i
                self.update(1)
        finally:
            if self.live:
                self.live.stop()
            
    def iter(self, iterable: Iterator[Any]) -> Iterator[Any]:
        """Iterate over an iterable with progress updates."""
        self.start_time = datetime.now()
        self.last_update_time = self.start_time
        
        if self.in_notebook:
            try:
                from IPython.display import display, HTML
                initial_display = self._create_html_display()
                self.display_handle = display(HTML(initial_display), display_id=True)
            except ImportError:
                self.live = Live(self._create_display(), console=self.console, refresh_per_second=10)
                self.live.start()
        else:
            self.live = Live(self._create_display(), console=self.console, refresh_per_second=10)
            self.live.start()
        
        try:
            for item in iterable:
                yield item
                self.update(1)
        finally:
            if self.live:
                self.live.stop()

if __name__ == "__main__":
    with CatProgressBar(100, "Processing files", unit="file", width=20) as pbar:
        for i in range(100):
            time.sleep(0.05)
            pbar.update(1)

