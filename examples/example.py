from catqdm import cat_bar, big_cat_bar, big_cat_bar_fullpath, CatProgressBar
import time

for _ in big_cat_bar(range(100), sleep_per=0.1):
    pass

for _ in cat_bar(range(100), sleep_per=0.1):
    pass

for _ in big_cat_bar_fullpath(range(100), sleep_per=0.1):
    pass

with CatProgressBar(100, "Processing files", unit="file", width=20) as pbar:
    for i in range(100):
        time.sleep(0.05)
        pbar.update(1)