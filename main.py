#!/usr/bin/env python3
"""The Funniest Office Joke — make.fun entry.

Writes a single one-line joke about office life to
$MAKEFUN_OUTPUT_DIR/entry.txt (falling back to /output/entry.txt
when the variable is unset). Deterministic: the same bytes on
every run. Standard library only.
"""

import hashlib
import os

JOKE = (
    "HR said our new open-plan office would boost collaboration, so now "
    "fifty of us sit side by side in silence, collaborating on ignoring "
    "each other with headphones on."
)

# Integrity anchor for the source text: the entry must be exactly this
# joke, one line, 1-200 characters. The hash is checked on every run
# so a stray edit to JOKE fails loudly instead of shipping silently.
JOKE_SHA256 = "f0a6bb487be5dd42a452af6d8551d7711bcd0ed6c7d551e44e5537b1d3f836e4"


def _validate(text: str) -> None:
    """Gate check: UTF-8, single line, 1-200 chars, not only whitespace."""
    text.encode("utf-8")  # raises if the text is not valid UTF-8
    if not 1 <= len(text) <= 200:
        raise ValueError(f"joke must be 1-200 chars, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")
    if not text.strip():
        raise ValueError("joke must not be only whitespace")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if digest != JOKE_SHA256:
        raise ValueError("joke text does not match its integrity anchor")


def main() -> None:
    _validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(JOKE)
    # Read-back integrity check: what landed on disk must be the joke.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != JOKE:
        raise ValueError("written entry.txt does not match the joke")
    _validate(written)


if __name__ == "__main__":
    main()
