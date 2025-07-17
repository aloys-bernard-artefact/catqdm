from catqdm import cat_bar, big_cat_bar

for _ in big_cat_bar(range(100), sleep_per=0.1):
    pass

for _ in cat_bar(range(100), sleep_per=0.1):
    pass
