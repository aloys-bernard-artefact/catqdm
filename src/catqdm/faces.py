#!/usr/bin/env python3
"""Cat Faces Collection - Various cat expressions and ASCII art for progress bars."""

# Classic emoji cats for simple displays
EMOJI_CATS = [
    "😿",  # crying cat - 0%
    "😾",  # pouting cat - 10%
    "🙀",  # weary cat - 20%
    "😼",  # cat with wry smile - 30%
    "😽",  # kissing cat - 40%
    "😸",  # grinning cat - 50%
    "😺",  # smiling cat - 60%
    "😹",  # cat with tears of joy - 70%
    "😻",  # smiling cat with heart-eyes - 80%
    "😻",  # heart-eyes cat - 90%
    "😻",  # super happy cat - 100%
]

# ASCII cat faces with different moods
ASCII_CAT_FACES = [
    "(=ＴェＴ=)",  # Very sad - 0%
    "(=；ェ；=)",  # Crying - 5%
    "(=；ω；=)",  # Still crying - 10%
    "(=ｘェｘ=)",  # Exhausted - 15%
    "(=ノωヽ=)",  # Tired - 20%
    "(=｀ェ´=)",  # Grumpy - 25%
    "(=￣ェ￣=)",  # Neutral - 30%
    "(=¬ェ¬=)",  # Skeptical - 35%
    "(=ФェФ=)",  # Alert - 40%
    "(=ↀωↀ=)",  # Curious - 45%
    "(=￣ω￣=)",  # Content - 50%
    "(=^･ｪ･^=)",  # Interested - 55%
    "(=^･ω･^=)",  # Happy - 60%
    "(=^-ω-^=)",  # Pleased - 65%
    "(=^･^=)",    # Satisfied - 70%
    "(=^ェ^=)",   # Cheerful - 75%
    "(=^‥^=)",    # Very happy - 80%
    "(=^o^=)",    # Excited - 85%
    "(=^▽^=)",   # Joyful - 90%
    "=^.^=",      # Blissful - 95%+
]

# Simple cat face progression
SIMPLE_CATS = [
    "( T_T )",  # Crying
    "( -_- )",  # Tired
    "( o_o )",  # Alert
    "( ^_^ )",  # Happy
    "( *_* )",  # Star-struck
]

# Rich-compatible cat faces with styling hints
RICH_CAT_MOODS = [
    {"face": "(=ＴェＴ=)", "color": "dim blue", "mood": "very_sad"},
    {"face": "(=；ω；=)", "color": "blue", "mood": "sad"},
    {"face": "(=｀ェ´=)", "color": "yellow", "mood": "grumpy"},
    {"face": "(=￣ェ￣=)", "color": "white", "mood": "neutral"},
    {"face": "(=ФェФ=)", "color": "green", "mood": "alert"},
    {"face": "(=^･ω･^=)", "color": "bright_green", "mood": "happy"},
    {"face": "(=^ェ^=)", "color": "cyan", "mood": "cheerful"},
    {"face": "(=^o^=)", "color": "bright_cyan", "mood": "excited"},
    {"face": "(=^▽^=)", "color": "magenta", "mood": "joyful"},
    {"face": "=^.^=", "color": "bright_magenta", "mood": "blissful"},
]

# Multi-line ASCII cats for complex displays
MULTILINE_CATS = {
    "sleeping": """
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)
""",
    "awake": """
    |\__/,|   (`\
  _.|o o  |_   ) )
-(((---(((--------
""",
    "happy": """
    |\__/,|   (`\
  _.|^_^  |_   ) )
-(((---(((--------
""",
    "excited": """
    |\__/,|   (`\
  _.|^o^  |_   ) )
-(((---(((--------
""",
    "flying": """
    |\__/,|     ✨
  _.|★_★  |_   /) )
-(((----)))----
""",
}

# Activity-based cat expressions
ACTIVITY_CATS = {
    "loading": ["(=^.^=)", "(=^o^=)", "(=^_^=)", "(=^-^=)"],
    "processing": ["(=￣ω￣=)", "(=^･ω･^=)", "(=^‥^=)", "(=^ェ^=)"],
    "thinking": ["(=｀ェ´=)", "(=¬ェ¬=)", "(=ФェФ=)", "(=ↀωↀ=)"],
    "working": ["(=^･ｪ･^=)", "(=^･ω･^=)", "(=^-ω-^=)", "(=^･^=)"],
    "celebrating": ["(=^o^=)", "(=^▽^=)", "=^.^=", "(=^ェ^=)"],
}

# Color themes for different moods
CAT_COLOR_THEMES = {
    "progress": {
        0: "dim red",
        20: "red", 
        40: "yellow",
        60: "green",
        80: "cyan",
        100: "bright_magenta"
    },
    "rainbow": ["red", "yellow", "green", "cyan", "blue", "magenta"],
    "ocean": ["deep_sky_blue1", "dodger_blue1", "turquoise2", "cyan1"],
    "sunset": ["red", "orange1", "yellow", "gold1"],
    "forest": ["green", "forest_green", "dark_green", "spring_green1"],
}

def get_cat_for_progress(progress_pct: float, cat_set: str = "ascii") -> str:
    """
    Get appropriate cat face for given progress percentage.
    
    Args:
        progress_pct: Progress from 0 to 100
        cat_set: Type of cat set ('emoji', 'ascii', 'simple')
    
    Returns:
        Cat face string
    """
    if cat_set == "emoji":
        cats = EMOJI_CATS
    elif cat_set == "simple":
        cats = SIMPLE_CATS
    else:
        cats = ASCII_CAT_FACES
    
    # Map progress to cat index
    index = min(int((progress_pct / 100) * len(cats)), len(cats) - 1)
    return cats[index]

def get_rich_cat_with_color(progress_pct: float) -> tuple[str, str]:
    """
    Get cat face with appropriate color for rich display.
    
    Args:
        progress_pct: Progress from 0 to 100
        
    Returns:
        Tuple of (cat_face, color_style)
    """
    index = min(int((progress_pct / 100) * len(RICH_CAT_MOODS)), len(RICH_CAT_MOODS) - 1)
    cat_data = RICH_CAT_MOODS[index]
    return cat_data["face"], cat_data["color"]

def get_activity_cats(activity: str) -> list[str]:
    """
    Get list of cats for specific activity.
    
    Args:
        activity: Activity type ('loading', 'processing', 'thinking', 'working', 'celebrating')
        
    Returns:
        List of cat faces for the activity
    """
    return ACTIVITY_CATS.get(activity, ACTIVITY_CATS["loading"])

def get_color_for_progress(progress_pct: float, theme: str = "progress") -> str:
    """
    Get color for given progress using specified theme.
    
    Args:
        progress_pct: Progress from 0 to 100
        theme: Color theme ('progress', 'rainbow', 'ocean', 'sunset', 'forest')
        
    Returns:
        Color string for rich styling
    """
    if theme == "progress":
        theme_colors = CAT_COLOR_THEMES["progress"]
        # Find the closest progress point
        for threshold in sorted(theme_colors.keys(), reverse=True):
            if progress_pct >= threshold:
                return theme_colors[threshold]
        return theme_colors[0]
    
    elif theme in CAT_COLOR_THEMES:
        colors = CAT_COLOR_THEMES[theme]
        index = min(int((progress_pct / 100) * len(colors)), len(colors) - 1)
        return colors[index]
    
    return "white"  # Default color

# Special cat collections for specific use cases
SPECIAL_CATS = {
    "programmer": [
        "(=￣ω￣=)",  # Thinking
        "(=^･ｪ･^=)",  # Coding
        "(=ＴェＴ=)",  # Debugging
        "(=^o^=)",    # Success!
    ],
    "sleepy": [
        "(=－ω－=)",  # Drowsy
        "(=＿ω＿=)",  # Sleepy
        "(=ｘωｘ=)",  # Sleeping
        "( -.- )",   # Deep sleep
    ],
    "excited": [
        "(=^ェ^=)",   # Happy
        "(=^o^=)",    # Excited
        "(=^▽^=)",   # Very excited
        "(=★ω★=)",   # Star-struck
    ]
}
