from catqdm import cat_bar, big_cat_bar, big_cat_bar_fullpath, rich_cat_bar, multi_stage_cat_loading

for _ in big_cat_bar(range(100), sleep_per=0.1):
    pass

for _ in cat_bar(range(100), sleep_per=0.1):
    pass

for _ in big_cat_bar_fullpath(range(100), sleep_per=0.1):
    pass

for _ in rich_cat_bar(range(100), sleep_per=0.1):
    pass

# Multi-stage loading demo
stages = [
    ("Initializing cats", 1),
    ("Loading cat database", 3), 
    ("Training cats", 4),
    ("Deploying cats", 2),
    ("Finalizing", 1)
]
multi_stage_cat_loading(stages, total_time=5.0)