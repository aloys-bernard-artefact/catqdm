# CatQDM 🐱

A delightful progress bar library featuring animated cats! CatQDM provides both a simple cat progress bar and a more elaborate big cat with animated eyes and tail.

## Features

- **Simple Cat Bar**: A cute single-line cat progress bar
- **Big Cat Bar**: A multi-line ASCII cat with animated eyes and tail
- **Notebook Support**: Works seamlessly in Jupyter notebooks
- **Terminal Support**: Full ANSI support for real terminals
- **Fallback Mode**: Graceful degradation for unsupported environments

## Installation

### From PyPI (when published)
```bash
pip install catqdm
```

### From Source
```bash
git clone https://github.com/yourusername/catqdm.git
cd catqdm
pip install -e .
```

## Quick Start

### Simple Cat Progress Bar

```python
from catqdm import catbar

# Basic usage
for i in catbar(range(100)):
    # Your work here
    pass
```

### Big Cat Progress Bar

```python
from catqdm import big_cat_bar

# Basic usage with animated eyes and tail
for i in big_cat_bar(range(100)):
    # Your work here
    pass
```

## Usage Examples

### Simple Cat Bar

```python
from catqdm import catbar
import time

# Basic iteration
for i in catbar(range(50), desc="Processing"):
    time.sleep(0.1)

# With custom description
for i in catbar(range(100), desc="🐱 Cat Processing"):
    time.sleep(0.05)
```

### Big Cat Bar

```python
from catqdm import big_cat_bar
import time

# Basic usage
for i in big_cat_bar(range(100), desc="Mood Upgrade"):
    time.sleep(0.05)

# Custom eyes animation
custom_eyes = ["T_T", ";_;", "-_-", "O_O", "^.^", "^_^"]
for i in big_cat_bar(range(100), eyes=custom_eyes, desc="Happy Cat",sleep_per=0.1  ):
   pass 


# Disable animations
for i in big_cat_bar(range(20), eyes=None, tails=None, desc="Static Cat"):
    time.sleep(0.1)
```

### In Jupyter Notebooks

```python
# Works seamlessly in notebooks
for i in big_cat_bar(range(50), desc="Notebook Cat"):
    # Your computation here
    pass
```

## API Reference

### `catbar(iterable, **kwargs)`

Simple cat progress bar.

**Parameters:**
- `iterable`: Any iterable to track progress
- `desc`: Description text (default: "Cat Processing")
- `**kwargs`: Additional tqdm parameters

### `big_cat_bar(iterable, **kwargs)`

Big cat progress bar with animated eyes and tail.

**Parameters:**
- `iterable`: Any iterable to track progress
- `eyes`: Sequence of eye strings for animation (default: predefined mood eyes)
- `tails`: Sequence of tail strings for animation (default: `["(`\\", "/')"]`)
- `sleep_per`: Optional sleep after each iteration (for demo/pacing)
- `desc`: Description text (default: "Mood Upgrade")
- `live`: Force live redraw (True) or static print (False). Default: auto-detect
- `center_term`: Center cat horizontally in terminal mode (default: True)
- `**kwargs`: Additional tqdm parameters

## Backend Modes

CatQDM automatically selects the best backend for your environment:

1. **Notebook Mode**: Uses IPython display for live updates in Jupyter
2. **ANSI Mode**: Uses terminal escape codes for real TTY terminals
3. **Static Mode**: Prints cat once and shows normal tqdm bar (fallback)

## Customization

### Custom Eye Animations

```python
# Create your own eye progression
my_eyes = ["😿", "😾", "😸", "😺", "😻"]
for i in big_cat_bar(range(100), eyes=my_eyes):
    pass
```

### Custom Tail Animations

```python
# Create your own tail movements
my_tails = ["(`\\", "/')", "~`~", "=^=", "(`\\"]
for i in big_cat_bar(range(100), tails=my_tails):
    pass
```

### Disable Animations

```python
# Static cat (no eye/tail movement)
for i in big_cat_bar(range(100), eyes=None, tails=None):
    pass
```

## Examples

Check out the `examples/` directory for more detailed usage examples:

- `example.py`: Command-line examples
- `example.ipynb`: Jupyter notebook examples


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on top of the excellent [tqdm](https://github.com/tqdm/tqdm) library
- Inspired by the joy of cats and progress bars
