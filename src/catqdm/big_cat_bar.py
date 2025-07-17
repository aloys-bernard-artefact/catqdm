#!/usr/bin/env python3
"""BigCat tqdm progress bar (multi-line ASCII cat above progress).

Notebook *and* terminal friendly live animation with eye updates.

Your requirements:
- Only the big 3-line cat (no tiny mood faces).
- Progress bar immediately below the cat.
- Eyes update as progress advances.
- **In notebooks too** (no output spam / wall of cats).

Implementation notes
-------------------
We choose a backend at runtime:

* **Notebook live backend** – Uses `IPython.display` with a persistent
  `display_id` (via a `DisplayHandle`) so the cat is **updated in place** each
  iteration. No repeated printing; the cell output shows one cat that changes
  eyes, and the tqdm notebook widget sits just below it.
* **ANSI live backend** – For real TTY terminals that honor cursor movement,
  we reserve screen rows above the tqdm bar and re-draw the cat using escape
  codes (`ESC[{n}F`, line clears, etc.).
* **Static fallback** – If neither backend is viable (or `live=False`), we
  print the cat once and run a normal tqdm bar beneath it.

Auto mode (`live=None`, the default) picks *Notebook* when running in an
IPython kernel, else ANSI if stdout is a TTY, else Static.

You can override: `big_cat_bar(..., live=True)` forces live (Notebook if in one,
else ANSI); `live=False` forces Static.
"""
from __future__ import annotations

import sys
import time
import html
from shutil import get_terminal_size
from typing import Iterable, Sequence, Any, Iterator, Optional

from tqdm.auto import tqdm

# ---------------------------------------------------------------------------
# Base cat art size requested by user (used only for reference / static print)
# ---------------------------------------------------------------------------
LOADED_ART = r"""    |\__/,|   (`\
  _.|o o  |_   ) )
-(((---(((--------"""

# Eyes we can cycle through every ~5% if desired. Feel free to trim / edit.
CAT_EYES_5PCT: Sequence[str] = [
    "T_T",  # 0%
    "T_T",  # 5%
    ";_;",  # 10%
    ";_;",  # 15%
    "-_-",  # 20%
    "-_-",  # 25%
    "-_-",  # 30%
    "-_-",  # 35%
    "O_O",  # 40%
    "O_O",  # 45%
    "-.-",  # 50%
    "^.^",  # 55%
    "^.^",  # 60%
    "^.^",  # 65%
    "^_^",  # 70%
    "^_^",  # 75%
    "^_^",  # 80%
    "^o^",  # 85%
    "^o^",  # 90%
    "^_^",  # 95%+
]

# Tail states that alternate as progress advances
CAT_TAILS: Sequence[str] = [
    "(`\\",  # Original tail pointing right
    " /')",   # New tail pointing left
]

# ---------------------------------------------------------------------------
# Environment detection helpers
# ---------------------------------------------------------------------------

def _supports_ansi(stream) -> bool:
    """Best-effort check whether *stream* is a real TTY that honors cursor moves."""
    try:
        return bool(stream.isatty())  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover
        return False


def _in_notebook() -> bool:
    """Rudimentary notebook detection (IPython kernel / Jupyter / Colab)."""
    try:  # pragma: no cover - light best-effort
        from IPython import get_ipython  # type: ignore
        ip = get_ipython()
        if ip is None:
            return False
        cls = ip.__class__.__name__
        if cls.startswith("ZMQ"):
            return True
        if "IPKernelApp" in getattr(ip, "config", {}):
            return True
        return False
    except Exception:
        return False

# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

def _render_big_cat(*, eyes: str = "o o", tail: str = "(`\\", width: Optional[int] = None) -> Sequence[str]:
    """Return lines for the big cat; center to *width* if provided.

    Eyes are centered into a 5-char slot (truncated if longer).
    Tail is used in the first line of the cat art.
    """
    eyes5 = f"{eyes:^5}"[:5]
    line1 = f"    |\\__/,|   {tail}"
    line2 = f"  _.|{eyes5}|_   ) )"
    line3 = "-(((---(((--------"
    lines = [line1, line2, line3]
    if width is not None:
        max_len = max(len(l) for l in lines)
        pad = max((width - max_len) // 2, 0)
        if pad:
            pad_str = " " * pad
            lines = [pad_str + l for l in lines]
    return lines


def _cat_text_block(eyes: str, tail: str, width: Optional[int]) -> str:
    """Full text block for printing (joined with newlines)."""
    return "\n".join(_render_big_cat(eyes=eyes, tail=tail, width=width))


# ------------------------------ ANSI printer ------------------------------

def _make_ansi_cat_printer(nlines: int, stream=None):
    if stream is None:
        stream = sys.stdout
    esc = "\x1b["

    def _print(lines: Sequence[str]) -> None:
        # Move cursor up *nlines* to start of the cat block.
        stream.write(f"{esc}{nlines}F")  # move cursor to column 0 nlines up
        for i, ln in enumerate(lines):
            stream.write("\x1b[2K")  # clear line
            stream.write(ln)
            if i < nlines - 1:
                stream.write("\n")
        stream.write("\n")  # leave cursor on bar line
        stream.flush()

    return _print


# ---------------------------- Notebook printer ----------------------------

def _make_nb_cat_printer(initial_block: str):
    """Return an updater callable that rewrites a notebook display area."""
    try:
        from IPython.display import display, HTML
        handle = display(HTML(_html_wrap(initial_block)), display_id=True)
    except Exception:  # pragma: no cover - fallback to stdout
        handle = None

    def _update(block: str) -> None:
        if handle is not None:
            try:
                handle.update(HTML(_html_wrap(block)))
                return
            except Exception:  # pragma: no cover
                pass
        # Fallback: print a carriage-returned single line summary when update fails
        sys.stdout.write("\r" + block.replace("\n", " | "))
        sys.stdout.flush()

    return _update


def _html_wrap(text_block: str) -> str:
    return "<pre style='margin:0;line-height:1.1;'>" + html.escape(text_block) + "</pre>"


# ---------------------------------------------------------------------------
# Progress bar
# ---------------------------------------------------------------------------

def big_cat_bar(
    iterable: Iterable[Any],
    *,
    eyes: Optional[Sequence[str]] = CAT_EYES_5PCT,
    tails: Optional[Sequence[str]] = CAT_TAILS,
    sleep_per: float = 0.0,
    desc: str = "Mood Upgrade",
    stream=None,
    live: Optional[bool] = None,
    center_term: bool = True,
    **tqdm_kwargs,
) -> Iterator[Any]:
    """Iterate *iterable* with a big-cat progress bar.

    Parameters
    ----------
    iterable:
        Any iterable whose progress you want to track.
    eyes:
        Sequence of eye strings to roughly indicate mood. If None or len<=1,
        eyes won't animate.
    tails:
        Sequence of tail strings to alternate. If None or len<=1, tails won't
        animate.
    sleep_per:
        Optional sleep after each iteration (demo / pacing only).
    desc:
        tqdm description.
    stream:
        Output stream for ANSI/static modes (default sys.stdout).
    live:
        Force live redraw (True) or static print once (False). Default None =
        auto (Notebook if running in one, else ANSI if TTY, else static).
    center_term:
        Center cat horizontally when using ANSI mode. Ignored in notebook mode.
    tqdm_kwargs:
        Passed through to tqdm.
    """
    if stream is None:
        stream = sys.stdout

    in_nb = _in_notebook()
    ansi_ok = _supports_ansi(stream)

    # Auto backend selection
    if live is None:
        live = True if in_nb or ansi_ok else False

    backend = "static"
    if live:
        backend = "notebook" if in_nb else ("ansi" if ansi_ok else "static")

    total = tqdm_kwargs.pop("total", None)
    if total is None and hasattr(iterable, "__len__"):
        try:
            total = len(iterable)  # type: ignore[arg-type]
        except TypeError:  # pragma: no cover
            total = None

    pct_driven = total is not None and total > 0
    if eyes and len(eyes) > 1:
        eye_step = 100.0 / len(eyes)
    else:
        eye_step = 100.0  # never advance
    
    if tails and len(tails) > 1:
        tail_step = 100.0 / len(tails)
    else:
        tail_step = 100.0  # never advance

    bar_format = tqdm_kwargs.pop("bar_format", "{l_bar}{bar}{r_bar}")
    tqdm_kwargs.setdefault("dynamic_ncols", True)

    # --------------------------- STATIC PATH ---------------------------
    if backend == "static":
        initial_eye = eyes[0] if eyes and len(eyes) > 0 else "o o"
        initial_tail = tails[0] if tails and len(tails) > 0 else "(`\\"
        static_cat = _cat_text_block(initial_eye, initial_tail, width=None)
        print(static_cat, file=stream)
        stream.flush()
        with tqdm(total=total, bar_format=bar_format, desc=desc, **tqdm_kwargs) as pbar:
            for item in iterable:
                yield item
                pbar.update(1)
                if sleep_per:
                    time.sleep(sleep_per)
        stream.write("\n")
        stream.flush()
        return

    # --------------------------- NOTEBOOK PATH -------------------------
    if backend == "notebook":
        # Display initial cat block (not centered; notebooks wrap text differently)
        initial_eye = eyes[0] if eyes and len(eyes) > 0 else "o o"
        initial_tail = tails[0] if tails and len(tails) > 0 else "(`\\"
        block = _cat_text_block(initial_eye, initial_tail, width=None)
        printer = _make_nb_cat_printer(block)
        with tqdm(total=total, bar_format=bar_format, desc=desc, **tqdm_kwargs) as pbar:
            for item in iterable:
                if eyes and len(eyes) > 1 and pct_driven:
                    pct = ((pbar.n + 1) / total) * 100.0
                    idx = int(pct // eye_step)
                    if idx >= len(eyes):
                        idx = len(eyes) - 1
                    eye = eyes[idx]
                elif eyes and len(eyes) > 1:
                    eye = eyes[pbar.n % len(eyes)]
                else:
                    eye = eyes[0] if eyes else "o o"

                if tails and len(tails) > 1 and pct_driven:
                    # Make tail movement more frequent - alternate every few iterations
                    tail_idx = (pbar.n // 3) % len(tails)  # Change every 3 iterations
                    tail = tails[tail_idx]
                elif tails and len(tails) > 1:
                    tail = tails[pbar.n % len(tails)]
                else:
                    tail = tails[0] if tails else "(`\\"

                printer(_cat_text_block(eye, tail, width=None))
                yield item
                pbar.update(1)
                if sleep_per:
                    time.sleep(sleep_per)
        return

    # --------------------------- ANSI PATH -----------------------------
    term_w = get_terminal_size().columns if center_term else None
    initial_eye = eyes[0] if eyes and len(eyes) > 0 else "o o"
    initial_tail = tails[0] if tails and len(tails) > 0 else "(`\\"
    init_lines = _render_big_cat(eyes=initial_eye, tail=initial_tail, width=term_w)
    nlines = len(init_lines)

    # Reserve the vertical space so tqdm prints *below* the cat.
    stream.write("\n" * nlines)
    stream.flush()
    printer = _make_ansi_cat_printer(nlines, stream=stream)
    printer(init_lines)  # draw once immediately so we see something

    with tqdm(total=total, bar_format=bar_format, desc=desc, **tqdm_kwargs) as pbar:
        for item in iterable:
            if eyes and len(eyes) > 1 and pct_driven:
                pct = ((pbar.n + 1) / total) * 100.0
                idx = int(pct // eye_step)
                if idx >= len(eyes):
                    idx = len(eyes) - 1
                eye = eyes[idx]
            elif eyes and len(eyes) > 1:
                eye = eyes[pbar.n % len(eyes)]
            else:
                eye = eyes[0] if eyes else "o o"

            if tails and len(tails) > 1 and pct_driven:
                # Make tail movement more frequent - alternate every few iterations
                tail_idx = (pbar.n // 3) % len(tails)  # Change every 3 iterations
                tail = tails[tail_idx]
            elif tails and len(tails) > 1:
                tail = tails[pbar.n % len(tails)]
            else:
                tail = tails[0] if tails else "(`\\"

            lines = _render_big_cat(eyes=eye, tail=tail, width=term_w)
            printer(lines)

            yield item
            pbar.update(1)
            if sleep_per:
                time.sleep(sleep_per)

    stream.write("\n")  # clean line after completion
    stream.flush()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Terminal width: {get_terminal_size().columns}")

    print("\n-- Demo: 100 steps (5% increments) big cat --")
    for _ in big_cat_bar(range(100), sleep_per=0.05):
        pass

    print("\n-- Demo: 247 steps big cat --")
    for _ in big_cat_bar(range(247), sleep_per=0.01):
        pass
