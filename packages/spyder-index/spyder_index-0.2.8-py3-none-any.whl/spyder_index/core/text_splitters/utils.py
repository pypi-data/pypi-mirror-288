from typing import List, Callable


def tokenizer(text: str) -> List:
    try:
        import tiktoken
    except ImportError:
        raise ImportError("tiktoken package not found, please install it with `pip install tiktoken`")

    enc = tiktoken.get_encoding("cl100k_base")
    return enc.encode(text)


def split_by_sep(sep) -> Callable[[str], List[str]]:
    """Split text by separator."""
    return lambda text: text.split(sep)


def split_by_regex(regex: str) -> Callable[[str], List[str]]:
    """Split text by regex."""
    import re

    return lambda text: re.findall(regex, text)


def split_by_char() -> Callable[[str], List[str]]:
    """Split text by character."""
    return lambda text: list(text)


def split_by_sentence_tokenizer() -> Callable[[str], List[str]]:
    try:
        import nltk
    except ImportError:
        raise ImportError("nltk package not found, please install it with `pip install nltk`")

    sentence_tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    return lambda text: _split_by_sentence_tokenizer(text, sentence_tokenizer)


def _split_by_sentence_tokenizer(text: str, sentence_tokenizer) -> List[str]:
    """Get the spans and then return the sentences.

    Using the start index of each span
    Instead of using end, use the start of the next span
    """
    spans = list(sentence_tokenizer.span_tokenize(text))
    sentences = []
    for i, span in enumerate(spans):
        start = span[0]
        if i < len(spans) - 1:
            end = spans[i + 1][0]
        else:
            end = len(text)
        sentences.append(text[start:end])
    return sentences
