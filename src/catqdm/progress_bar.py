from rich.console import Console
from rich.text import Text
from rich.live import Live
import time
from typing import Any, Iterator, Dict
from datetime import datetime, timedelta
from catqdm.utils.notebook import _in_notebook
from IPython.display import display, HTML
class CatProgressBar:
    """A functional progress bar with cat emojis."""

    DEFAULT_DESC_COLOR = "cyan"
    DEFAULT_POSTFIX_COLOR = "bright_black"
    DEFAULT_HTML_POSTFIX_COLOR = "#888"
    DEFAULT_CAT_COLOR = "yellow; font-weight: bold"
    DEFAULT_PAW_COLOR = "green"
    DEFAULT_EMPTY_COLOR = "#666"
    DEFAULT_METRICS_COLOR = "white"

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
        self.width = width
        self.unit = unit
        self.unit_scale = unit_scale
        self.unit_divisor = unit_divisor
        self.postfix = postfix or {}
        self.bar_format = bar_format
        self.desc_color = self.DEFAULT_DESC_COLOR
        self.postfix_color = self.DEFAULT_POSTFIX_COLOR
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
        self.width = min(width, 50)
        
    def _init_display(self):
        """Initialize display."""
        self.start_time = datetime.now()
        self.last_update_time = self.start_time
        
        if self.in_notebook:
            try:
                self.display_handle = display(HTML(self._create_html_display()), display_id=True)
                return
            except Exception:
                pass
        
        self.live = Live(self._create_display(), console=self.console, refresh_per_second=10)
        self.live.start()
        
    def __enter__(self):
        """Context manager entry."""
        self._init_display()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.live:
            self.live.stop()
        if self.in_notebook and self.display_handle:
            try:
                self.current = self.total
                self.display_handle.update(HTML(self._create_html_display()))
            except Exception:
                pass
            
    def _format_number(self, n: float) -> str:
        """Format number with unit scaling if enabled."""
        if not self.unit_scale:
            return f"{n:.0f}"
        
        for unit in ['', 'K', 'M', 'G', 'T']:
            if n < self.unit_divisor:
                return f"{n:.1f}{unit}" if n != int(n) else f"{int(n)}{unit}"
            n /= self.unit_divisor
        return f"{n:.1f}P"
    
    def _format_postfix_value(self, v: Any) -> str:
        """Format a single postfix value."""
        if isinstance(v, float):
            return f"{v:.3f}" if abs(v) < 100 else f"{v:.1f}"
        elif isinstance(v, int) and v > 1000:
            return f"{v:,}"
        return str(v)
    
    def _progress_info(self):
        """Calculate progress percentage and filled width."""
        if self.total == 0:
            return 0, 0
        progress_pct = (self.current / self.total * 100)
        filled = int((progress_pct / 100) * self.width)
        return progress_pct, filled
    
    def _build_progress_bar(self, progress_pct: float, filled: int, html_mode: bool = False):
        """Build the progress bar characters/emojis."""
        bar_parts = []
        for i in range(self.width):
            if i < filled:
                emoji = "🐱" if i == filled - 1 and progress_pct < 100 else "🐾"
                if html_mode:
                    color = self.DEFAULT_CAT_COLOR if emoji == "🐱" else self.DEFAULT_PAW_COLOR
                    bar_parts.append(f'<span style="color: {color};">{emoji}</span>')
                else:
                    style = "bright_yellow" if emoji == "🐱" else "green"
                    bar_parts.append((emoji, style))
            else:
                if html_mode:
                    bar_parts.append(f'<span style="color: {self.DEFAULT_EMPTY_COLOR};">░</span>')
                else:
                    bar_parts.append(("░", "dim"))
        return bar_parts
    
    def _format_postfix_display(self, html_mode: bool = False):
        """Format postfix for display."""
        if not self.postfix:
            return "" if html_mode else ("", "")
        
        postfix_parts = []
        for k, v in self.postfix.items():
            if k != "_color":
                formatted_value = self._format_postfix_value(v)
                postfix_parts.append(f"{k}={formatted_value}")
        
        if not postfix_parts:
            return "" if html_mode else ("", "")
        
        postfix_color = self.postfix.get("_color", self.DEFAULT_HTML_POSTFIX_COLOR if html_mode else self.DEFAULT_POSTFIX_COLOR)
        separator = " | "
        content = ", ".join(postfix_parts)
        
        if html_mode:
            return f'<span style="color: {postfix_color};">{separator}{content}</span>'
        else:
            return f"{separator}{content}", postfix_color
    
    def _create_html_display(self) -> str:
        """Create HTML display for Jupyter notebooks."""
        progress_pct, filled = self._progress_info()
        
        parts = [f'<span style="color: {self.DEFAULT_DESC_COLOR}; font-weight: bold;">{self.description}: </span>']
        
        # Progress bar
        bar_parts = self._build_progress_bar(progress_pct, filled, html_mode=True)
        parts.extend(bar_parts)
        
        # Metrics and postfix
        parts.append(f' <span style="color: {self.DEFAULT_METRICS_COLOR};">{self._get_metrics()}</span>')
        
        postfix_display = self._format_postfix_display(html_mode=True)
        if postfix_display:
            parts.append(postfix_display)
        
        return f'<pre style="margin:0;line-height:1.1;">{"".join(parts)}</pre>'
    
    def _create_display(self) -> Text:
        """Create the tqdm-like display."""
        progress_pct, filled = self._progress_info()

        display = Text()
        display.append(f"{self.description}: ", style=self.desc_color)
        
        # Progress bar
        bar_parts = self._build_progress_bar(progress_pct, filled, html_mode=False)
        for content, style in bar_parts:
            display.append(content, style=style)
        
        # Metrics and postfix
        display.append(f" {self._get_metrics()}", style="white")
        
        postfix_display, postfix_color = self._format_postfix_display(html_mode=False)
        if postfix_display:
            display.append(postfix_display, style=postfix_color)
        
        return display
        
    def _get_metrics(self) -> str:
        """Get progress metrics like tqdm."""
        if self.total == 0:
            return "0/0 (0.0%)"
            
        progress_pct, _ = self._progress_info()
        current_str = self._format_number(self.current)
        total_str = self._format_number(self.total)
        base_metrics = f"{current_str}/{total_str} ({progress_pct:.1f}%)"
        
        if not (self.start_time and self.current > 0):
            return base_metrics
            
        elapsed = datetime.now() - self.start_time
        rate = self.current / elapsed.total_seconds()
        
        if rate > 0:
            eta_seconds = (self.total - self.current) / rate
            eta = timedelta(seconds=int(eta_seconds))
            elapsed_str = str(elapsed).split('.')[0]  
            eta_str = str(eta).split('.')[0]
            rate_str = self._format_number(rate)
            return f"{base_metrics} [{elapsed_str}<{eta_str}, {rate_str}{self.unit}/s]"
        else:
            elapsed_str = str(elapsed).split('.')[0]
            return f"{base_metrics} [{elapsed_str}, ?{self.unit}/s]"
        
    def update(self, n: int = 1):
        """Update the progress by n steps."""
        self.current = min(self.current + n, self.total)
        self.last_update_time = datetime.now()
        self._update_display()
            
    def set_description(self, description: str, color: str = None):
        """Set the description of the progress bar with optional color."""
        self.description = description
        if color:
            self.desc_color = color
        self._update_display()
            
    def set_postfix(self, color: str = None, **kwargs):
        """Set postfix information with optional color."""
        if color:
            kwargs["_color"] = color
        self.postfix.update(kwargs)
        self._update_display()
        
    def _update_display(self):
        """Update the display based on environment."""
        if self.in_notebook and self.display_handle:
            try:
                self.display_handle.update(HTML(self._create_html_display()))
                return
            except Exception:
                pass
                
        if self.live:
            self.live.update(self._create_display())
            
    def __iter__(self) -> Iterator[int]:
        """Make the progress bar iterable."""
        self._init_display()
        try:
            for i in range(self.total):
                yield i
                self.update(1)
        finally:
            if self.live:
                self.live.stop()
            
    def iter(self, iterable: Iterator[Any]) -> Iterator[Any]:
        """Iterate over an iterable with progress updates."""
        self._init_display()
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

