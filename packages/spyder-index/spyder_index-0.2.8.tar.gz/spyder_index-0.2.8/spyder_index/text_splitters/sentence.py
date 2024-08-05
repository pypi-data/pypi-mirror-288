from typing import List, Tuple

from spyder_index.core.document import Document

from spyder_index.core.text_splitters.utils import (
    split_by_regex,
    split_by_sep,
    split_by_sentence_tokenizer,
    split_by_char,
    tokenizer
)


class SentenceSplitter:
    """SentenceSplitter is designed to split input text into smaller chunks,
    particularly useful for processing large documents or texts.

    Args:
        chunk_size (int, optional): Size of each chunk. Default is ``512``.
        chunk_overlap (int, optional): Amount of overlap between chunks. Default is ``256``.
        separator (str, optional): Separators used for splitting into words. Default is ``" "``
    """

    def __init__(self,
                 chunk_size: int = 512,
                 chunk_overlap: int = 256,
                 separator=" "
                 ) -> None:

        if chunk_overlap > chunk_size:
            raise ValueError(
                f"Got a larger `chunk_overlap` ({chunk_overlap}) than `chunk_size` "
                f"({chunk_size}). `chunk_overlap` should be smaller."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self._split_fns = [
            split_by_sep("\n\n\n"),
            split_by_sentence_tokenizer()
        ]
        self._sub_split_fns = [
            split_by_regex("[^,.;？！]+[,.;？！]?"),
            split_by_sep(separator),
            split_by_char()
        ]

    def from_text(self, text: str) -> List[str]:
        """Split text into chunks.
        
        Args:
        - text (str): Input text to split.
        """
        splits = self._split(text)
        chunks = self._merge(splits)

        return chunks

    def from_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks.

        Args:
            documents (List[Document]): List of Documents
        """
        chunks = []

        for document in documents:
            texts = self.from_text(document.get_content())

            for text in texts:
                chunks.append(Document(text=text, metadata=document.get_metadata()))

        return chunks

    def _split(self, text: str) -> List[dict]:

        token_size = len(tokenizer(text))
        if token_size <= self.chunk_size:
            return [{"text": text, "is_sentence": True, "token_size": token_size}]

        text_splits = []
        text_splits_by_fns, is_sentence = self._split_by_fns(text)

        for text_split_by_fns in text_splits_by_fns:
            token_size = len(tokenizer(text))
            if token_size <= self.chunk_size:
                text_splits.append({"text": text_split_by_fns, "is_sentence": is_sentence, "token_size": token_size})

            else:
                recursive_text_splits = self._split(text_split_by_fns)
                text_splits.extend(recursive_text_splits)

        return text_splits

    def _split_by_fns(self, text: str) -> Tuple[List[str], bool]:

        for split_fn in self._split_fns:
            splits = split_fn(text)
            if len(splits) > 1:
                return splits, True

        for split_fn in self._sub_split_fns:
            splits = split_fn(text)
            if len(splits) > 1:
                return splits, False

    def _merge(self, splits: List[dict]) -> List[str]:
        """Merge splits into chunks."""
        chunks: List[str] = []
        cur_chunk: List[Tuple[str, int]] = []
        cur_chunk_len = 0
        last_chunk: List[Tuple[str, int]] = []
        new_chunk = True

        def close_chunk() -> None:
            nonlocal chunks, cur_chunk, last_chunk, cur_chunk_len, new_chunk

            chunks.append("".join([text for text, length in cur_chunk]))
            last_chunk = cur_chunk
            cur_chunk = []
            cur_chunk_len = 0
            new_chunk = True

            # add overlap to the next chunk using previous chunk
            if len(last_chunk) > 0:
                last_index = len(last_chunk) - 1
                while (
                    last_index >= 0
                    and cur_chunk_len + last_chunk[last_index][1] <= self.chunk_overlap
                ):
                    text, length = last_chunk[last_index]
                    cur_chunk_len += length
                    cur_chunk.insert(0, (text, length))
                    last_index -= 1

        def postprocess_chunks(chunks: List[str]) -> List[str]:
            """Post-process chunks."""
            new_chunks = []
            for chunk in chunks:
                stripped_chunk = chunk.strip()
                if stripped_chunk == "":
                    continue
                new_chunks.append(stripped_chunk)
            return new_chunks

        while len(splits) > 0:
            cur_split = splits[0]

            if cur_split['token_size'] > self.chunk_size:
                raise ValueError("Single token exceeded chunk size")

            if cur_chunk_len + cur_split['token_size'] > self.chunk_size and not new_chunk:
                close_chunk()
            else:
                if (
                    cur_split['is_sentence']
                    or cur_chunk_len + cur_split['token_size'] <= self.chunk_size
                    or new_chunk  # If `new_chunk`, always add at least one split
                ):
                    cur_chunk_len += cur_split['token_size']
                    cur_chunk.append((cur_split['text'], cur_split['token_size']))
                    splits.pop(0)
                    new_chunk = False
                else:
                    close_chunk()

        if not new_chunk:
            chunk = "".join([text for text, length in cur_chunk])
            chunks.append(chunk)

        return postprocess_chunks(chunks)

