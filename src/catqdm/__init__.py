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

time.sleep(2)  # Simulate loading time
LOADED_ART = r"""
    |\__/,|   (`\
  _.|o o  |_   ) )
-(((---(((--------
"""
print("Cat is ready !")
print(LOADED_ART)