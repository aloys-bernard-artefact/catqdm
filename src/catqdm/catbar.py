import time
from shutil import get_terminal_size
from tqdm.auto import tqdm

CATS_5PCT = [
    r"(=ＴェＴ=)",  # 0%
    r"(=；ェ；=)",  # 5%
    r"(=；ω；=)",  # 10%
    r"(=ｘェｘ=)",  # 15%
    r"(=ノωヽ=)",  # 20%
    r"(=｀ェ´=)",  # 25%
    r"(=￣ェ￣=)",  # 30%
    r"(=¬ェ¬=)",  # 35%
    r"(=ФェФ=)",  # 40%
    r"(=ↀωↀ=)",  # 45%
    r"(=￣ω￣=)",  # 50%
    r"(=^･ｪ･^=)",  # 55%
    r"(=^･ω･^=)",  # 60%
    r"(=^-ω-^=)",  # 65%
    r"(=^･^=)",    # 70%
    r"(=^ェ^=)",   # 75%
    r"(=^‥^=)",    # 80%
    r"(=^o^=)",    # 85%
    r"(=^▽^=)",   # 90%
    r"=^.^=",      # 95%+
]

# CATS_5PCT = [
#     "😿", "😽", "😾", "😼", "🙀", "😸", "😺", "😹", "😻"
# ]


def cat_bar(
    iterable,
    cats=CATS_5PCT,
    sleep_per=0.0,
    desc="Mood Upgrade",
    **tqdm_kwargs
):
    """
    Progress bar that shows a centered cat (sad->happy) changing every 5%.

    If total != known, cats will just cycle by iteration count.
    """
    total = tqdm_kwargs.pop("total", None)
    if total is None and hasattr(iterable, "__len__"):
        total = len(iterable)

    pct_driven = total is not None and total > 0
    step = 100.0 / len(cats)  # auto-scales if cat list length != 20


    bar_format = tqdm_kwargs.pop("bar_format", "{l_bar}{bar}{r_bar}")

    tqdm_kwargs.setdefault("dynamic_ncols", True)

    with tqdm(total=total, bar_format=bar_format, desc=desc, **tqdm_kwargs) as pbar:
        for item in iterable:
            if pct_driven:
                # percent *after* this iteration
                pct = ((pbar.n + 1) / total) * 100.0
                idx = int(pct // step)
                if idx >= len(cats):
                    idx = len(cats) - 1
                cat = cats[idx]
            else:
                idx = pbar.n % len(cats)
                cat = cats[idx]

            
            pbar.set_postfix_str(cat)

            yield item
            pbar.update(1)
            if sleep_per:
                time.sleep(sleep_per)
        else : 
            print("\nAll done! Here's the final cat:")


if __name__ == "__main__":
    # 100 steps -> clean 5% increments
    print(f"Terminal width: {get_terminal_size().columns}")
    for _ in cat_bar(range(100), sleep_per=0.1):
        pass

    # Non-100 total still works; cats scaled evenly across progress
    for _ in cat_bar(range(247),  sleep_per=0.25):
        pass
