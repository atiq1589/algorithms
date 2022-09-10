# Add some code
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import wraps
from typing import DefaultDict, Generator, List, Optional, Tuple


@dataclass
class TrieNode:
    children: DefaultDict[str, "TrieNode"] = field(default_factory=lambda: defaultdict(lambda: TrieNode()))
    suffix_link: Optional["TrieNode"] = None
    output_link: Optional["TrieNode"] = None
    dict_word_idx: Optional[int] = None


class AhoCorasick:

    def __init__(self, dictionary: List[str]):
        self._dictionary = dictionary
        self._trie_root = TrieNode()
        self._tree_build_complete = False
        self._suffix_link_complete = False

    def _add_to_trie(self, word: str, idx: int):
        trie_node: TrieNode = self._trie_root
        for c in word:
            trie_node: TrieNode = trie_node.children[c]
        trie_node.dict_word_idx = idx
        self._suffix_link_complete = False

    def _add_suffix_link(self, key: str, child: TrieNode, parent: TrieNode):
        while key not in parent.children and parent != self._trie_root:
            parent = parent.suffix_link

        if key in parent.children:
            child.suffix_link = parent.children[key]
        else:
            child.suffix_link = self._trie_root

    def _add_output_link(self, trie_node: TrieNode):
        if trie_node.suffix_link.dict_word_idx is not None:
            trie_node.output_link = trie_node.suffix_link
        else:
            trie_node.output_link = trie_node.suffix_link.output_link

    def build_tree(self):
        for i, word in enumerate(self._dictionary):
            self._add_to_trie(word, i)

    def _prepare_aho(func):

        @wraps(func)
        def wrapper(self, *args, **kwrgs):
            if not self._tree_build_complete:
                self.build_tree()
                self.build_suffix_output_link()
                self._tree_build_complete = True
                self._suffix_link_complete = True

            if not self._suffix_link_complete:
                self.build_suffix_output_link()
                self._suffix_link_complete = True
            return func(self, *args, **kwrgs)

        return wrapper

    def build_suffix_output_link(self):
        trie_root = self._trie_root
        que = deque()

        for child in trie_root.children.values():
            que.append(child)
            child.suffix_link = trie_root

        while que:
            trie_node: TrieNode = que.popleft()

            for key, child in trie_node.children.items():
                self._add_suffix_link(key, child, trie_node.suffix_link)
                que.append(child)
            self._add_output_link(trie_node)

    def _get_output_link(self, trie_node, *, end_idx):
        while trie_node and trie_node != self._trie_root:
            end_word_idx = trie_node.dict_word_idx
            yield end_idx - len(self._dictionary[end_word_idx]) + 1, end_idx
            trie_node = trie_node.output_link

    @_prepare_aho
    def match(self, text: str, *, full_match: Optional[bool] = False) -> Generator[Tuple[int, int], None, None]:
        trie_node = self._trie_root
        for i, c in enumerate(text):
            if c in trie_node.children:
                trie_node = trie_node.children[c]
            else:
                while c not in trie_node.children and trie_node != self._trie_root:
                    trie_node = trie_node.suffix_link
                if c not in trie_node.children:
                    continue
                else:
                    trie_node = trie_node.children[c]

            end_word_idx = trie_node.dict_word_idx
            if end_word_idx is not None:
                yield i - len(self._dictionary[end_word_idx]) + 1, i
            yield from self._get_output_link(trie_node.output_link, end_idx=i)


def solution(text: str, dictionary: List[str]) -> List[int]:
    aho_corasick = AhoCorasick(dictionary)
    hash_map = {word: i for i, word in enumerate(dictionary)}
    res = [0] * len(dictionary)
    for match in aho_corasick.match(text, full_match=True):
        start_idx, end_idx = match
        word = text[start_idx:end_idx + 1]
        res[hash_map[word]] += 1

    return res


if __name__ == "__main__":
    text = "ababacbabc"
    dictionary = ["aba", "ba", "ac", "a", "abc"]
    for result in solution(text, dictionary):
        print(result)
