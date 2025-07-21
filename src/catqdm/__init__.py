import time
import os
import sys
from catqdm.catbar import cat_bar
from catqdm.big_cat_bar import big_cat_bar
from catqdm.big_cat_bar_fullpath import big_cat_bar_fullpath
from catqdm.progress_bar import CatProgressBar

from catqdm.utils.animation import run_cat_animation

try:
    run_cat_animation()
except Exception as e:
    pass