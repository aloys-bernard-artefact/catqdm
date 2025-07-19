import time
print("Waking up the cat...")
LOADING_ART = r"""
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)   
"""
print(LOADING_ART)

from catqdm.catbar import cat_bar
from catqdm.big_cat_bar import big_cat_bar
from catqdm.big_cat_bar_fullpath import big_cat_bar_fullpath
from catqdm.rich_cat_bar import rich_cat_bar, multi_stage_cat_loading

time.sleep(2)
LOADED_ART = r"""
    |\__/,|   (`\
  _.|o o  |_   ) )
-(((---(((--------
"""
print("Cat is ready !")
print(LOADED_ART)