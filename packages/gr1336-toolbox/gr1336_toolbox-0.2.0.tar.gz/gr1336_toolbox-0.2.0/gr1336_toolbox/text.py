import re
import pyperclip
import markdown2
from datetime import datetime
from textblob import TextBlob
from .fast_types import is_string
from markdownify import markdownify as md


class ProcessSplit:
    """
    Apache 2.0 license
    Modified from https://github.com/fakerybakery/txtsplit/blob/main/txtsplit/__init__.py
    with was modified from Modified from https://github.com/neonbjb/tortoise-tts/blob/main/tortoise/utils/text.py
    """

    def __init__(self, text: str, desired_length=100, max_length=200):
        self.text = text
        self.rv = []
        self.in_quote = False
        self.current = ""
        self.split_pos = []
        self.pos = -1
        self.end_pos = len(self.text) - 1
        self.max_length = max_length
        self.desired_length = desired_length

    def seek(self, delta):
        is_neg = delta < 0
        for _ in range(abs(delta)):
            if is_neg:
                self.pos -= 1
                self.current = self.current[:-1]
            else:
                self.pos += 1
                self.current += self.text[self.pos]
            if self.text[self.pos] in '"“”':
                self.in_quote = not self.in_quote
        return self.text[self.pos]

    def peek(self, delta):
        p = self.pos + delta
        return self.text[p] if p < self.end_pos and p >= 0 else ""

    def commit(self):
        self.rv.append(self.current)
        self.current = ""
        self.split_pos = []

    def run(self) -> list[str]:
        while self.pos < self.end_pos:
            c = self.seek(1)
            if len(self.current) >= self.max_length:
                if len(self.split_pos) > 0 and len(self.current) > (
                    self.desired_length / 2
                ):
                    d = self.pos - self.split_pos[-1]
                    self.seek(-d)
                else:
                    while (
                        c not in "!?.\n "
                        and self.pos > 0
                        and len(self.current) > self.desired_length
                    ):
                        c = self.seek(-1)
                self.commit()
            elif not self.in_quote and (
                c in "!?\n" or (c == "." and self.peek(1) in "\n ")
            ):
                while (
                    self.pos < len(self.text) - 1
                    and len(self.current) < self.max_length
                    and self.peek(1) in "!?."
                ):
                    c = self.seek(1)
                self.split_pos.append(self.pos)
                if len(self.current) >= self.desired_length:
                    self.commit()
            elif self.in_quote and self.peek(1) == '"“”' and self.peek(2) in "\n ":
                self.seek(2)
                self.split_pos.append(self.pos)
        self.rv.append(self.current)
        self.rv = [s.strip() for s in self.rv]
        self.rv = [
            s for s in self.rv if len(s) > 0 and not re.match(r"^[\s\.,;:!?]*$", s)
        ]
        return self.rv


def current_time():
    return f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"


def recursive_replacer(text: str, dic: dict) -> str:
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def clipboard(text: str):
    """
    Set the clipboard to the given text.
    """
    pyperclip.copy(text)


def unescape(elem: str) -> str:
    assert is_string(elem, True), "The input should be a valid string."
    return elem.encode().decode("unicode-escape", "ignore")


def blob_split(text: str) -> list[str]:
    return [x for x in TextBlob(text).raw_sentences]


def trimincompletesentence(txt: str) -> str:
    ln = len(txt)
    lastpunc = max(txt.rfind(". "), txt.rfind("!"), txt.rfind("?"))
    if lastpunc < ln - 1:
        if txt[lastpunc + 1] == '"':
            lastpunc = lastpunc + 1
    if lastpunc >= 0:
        txt = txt[: lastpunc + 1]
    return txt


def simplify_quotes(txt: str) -> str:
    assert is_string(txt, True), f"The input '{txt}' is not a valid string"
    replacements = {
        "“": '"',
        "”": '"',
        "’": "'",
        "‘": "'",
        "`": "'",
    }
    return recursive_replacer(txt, replacements)


def clear_empty(text: str, clear_empty_lines: bool = True) -> str:
    """A better way to clear multiple empty lines than just using regex for it all.
    For example if you use:
    ```py
    text = "Here is my text.\nIt should only clear empty spaces and           not clear the lines out.\n\n\nThe lines should be preserved!"

    results = re.sub(r"\s+", " ", text)
    # results = "Here is my text. It should only clear empty spaces and not clear the lines out. The lines should be preserved!"
    ```
    As shown in the example above, the lines were all removed even if we just wanted to remove empty spaces.

    This function can also clear empty lines out, with may be useful. Its enabled by default.
    """
    return "\n".join(
        [
            re.sub(r"\s+", " ", x.strip())
            for x in text.splitlines()
            if not clear_empty_lines or x.strip()
        ]
    )


def txtsplit(
    text: str,
    desired_length=100,
    max_length=200,
    simplify_quote: bool = True,
) -> list[str]:
    text = clear_empty(text, True)
    if simplify_quote:
        text = simplify_quotes(text)
    processor = ProcessSplit(text, desired_length, max_length)
    return processor.run()


def remove_special_characters(text: str) -> str:
    """
    Remove special characters from the given text using regular expressions.
    """
    pattern = r"[^A-Za-z0-9\s,.\"'?!()\[\];:]"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def html_to_markdown(html: str) -> str:
    """Converts HTML to Markdown"""
    return md(html)


def markdown_to_html(markdown: str) -> str:
    """Converts Markdown to HTML"""
    return markdown2.markdown(markdown)


__all__ = [
    "current_time",
    "recursive_replacer",
    "clipboard",
    "unescape",
    "blob_split",
    "trimincompletesentence",
    "clear_empty",
    "txtsplit",
    "remove_special_characters",
    "markdown_to_html",
]
