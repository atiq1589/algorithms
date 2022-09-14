from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class End:
    value: Optional[int] = -1


@dataclass
class TreeNode:
    start_idx: int
    end_idx: End
    suffix_link: "TreeNode"
    children: Dict[str, "TreeNode"] = field(default_factory=dict)


class SuffixTree:
    # _TEXT_STOPPER = chr(0)
    _TEXT_STOPPER = '$'

    def __init__(self, text: str):
        text += self._TEXT_STOPPER
        self.global_end = End()

        self._tree_root: TreeNode = TreeNode(start_idx=-1, end_idx=self.global_end, suffix_link=None)
        self._tree_root.suffix_link = self._tree_root

        self._text = text

        self._active_node: TreeNode = self._tree_root
        self._active_edge = -1
        self._active_length = 0

    def _ukkonen(self):
        remaining_chars = 0
        for i, char in enumerate(self._text):
            self.global_end.value = i
            remaining_chars += 1
            last_tree_node: TreeNode = None

            while remaining_chars:
                if self._active_length == 0:
                    if char in self._active_node.children:
                        self._active_edge = self._active_node.children[char].start_idx
                        self._active_length += 1
                        break
                    new_created_node = TreeNode(start_idx=i, suffix_link=self._tree_root, end_idx=self.global_end)
                    self._active_node.children[char] = new_created_node
                    remaining_chars -= 1
                else:
                    edge_start_char = self._text[self._active_edge]
                    edge_ = self._active_node.children[edge_start_char]
                    start = edge_.start_idx
                    end = edge_.end_idx.value
                    while self._active_length > end - start + 1:
                        for child in edge_.children.values():
                            if self._text[child.start_idx] == self._text[i - self._active_length + end - start + 1]:
                                self._active_node = edge_
                                self._active_edge = child.start_idx
                                self._active_length -= (end - start + 1)
                                break
                        else:
                            raise Exception("Must be here")
                        edge_start_char = self._text[self._active_edge]
                        edge_ = self._active_node.children[edge_start_char]
                        start = edge_.start_idx
                        end = edge_.end_idx.value

                    if end - start + 1 == self._active_length:
                        edge_.children[char] = TreeNode(start_idx=i,
                                                        end_idx=self.global_end,
                                                        suffix_link=self._tree_root)
                        if last_tree_node:
                            last_tree_node.suffix_link = edge_
                        last_tree_node = edge_
                        remaining_chars -= 1

                        if self._active_node != self._tree_root:
                            self._active_node = self._active_node.suffix_link
                        else:
                            self._active_edge += 1
                            self._active_length -= 1
                    else:
                        if char == self._text[start + self._active_length]:
                            self._active_length += 1
                            break

                        new_split_node = TreeNode(start_idx=start + self._active_length,
                                                  end_idx=edge_.end_idx,
                                                  suffix_link=self._tree_root)

                        new_split_node.children = edge_.children
                        edge_.children = dict()

                        edge_.children[self._text[new_split_node.start_idx]] = new_split_node

                        edge_.end_idx = End(start + self._active_length - 1)

                        new_created_node = TreeNode(start_idx=i, suffix_link=self._tree_root, end_idx=self.global_end)

                        edge_.children[char] = new_created_node

                        remaining_chars -= 1
                        if last_tree_node:
                            last_tree_node.suffix_link = edge_
                        last_tree_node = edge_

                        if self._active_node != self._tree_root:
                            self._active_node = self._active_node.suffix_link
                        else:
                            self._active_edge += 1
                            self._active_length -= 1

    def search(self, word: str) -> bool:
        _active_edge_start = -1
        _active_node: TreeNode = self._tree_root
        _active_length = 0
        for c in word:
            if _active_length == 0:
                if c not in _active_node.children:
                    return False
                else:
                    _active_node = _active_node.children[c]
                    _active_edge_start = _active_node.start_idx
                    _active_length += 1
            else:
                if self._text[_active_edge_start + _active_length] == c:
                    _active_length += 1
                else:
                    return False
            if _active_edge_start != -1 and _active_edge_start + _active_length - 1 == _active_node.end_idx.value:
                _active_length = 0
        return True

    def printTree(self):
        queue = [(self._tree_root, 0, "Start")]
        print("root")
        prev_level = 0
        while queue:
            node, level, parent = queue.pop(0)
            if prev_level != level:
                prev_level = level
                print()
                print('-' * 100)
            print(parent, end=" => ")
            print("(", node.start_idx, ", ", node.end_idx.value, end=" ) ")
            print(self._text[node.start_idx:node.end_idx.value + 1], end=" " * 4 + "|" * 2 + " " * 4)
            for child in node.children.values():
                queue.append((child, level + 1, node.start_idx))


def solution(words):
    words.sort(key=len, reverse=True)
    suffix_tree_1 = SuffixTree(words[0])
    suffix_tree_2 = SuffixTree(words[1])
    suffix_tree_1._ukkonen()
    suffix_tree_2._ukkonen()
    for i in range(len(words[-1])):
        for j in range(i + 1):
            if suffix_tree_1.search(words[-1][j:i + 1]) and suffix_tree_2.search(words[-1][j:i + 1]):
                print(words[-1][j:i + 1], len(words[-1][j:i + 1]))
    print(suffix_tree_1.search("cvscxggb"), words[0])
    print(suffix_tree_2.search("cvscxggb"), words[1])


if __name__ == "__main__":
    # solution = SuffixTree("xyzxyaxyb")
    solution = SuffixTree("mississi")
    # solution = SuffixTree("banana")
    # solution = SuffixTree("aaaaa")
    # solution = SuffixTree("abcdef")
    # solution = SuffixTree("aladdinaddingdinner")
    # solution = SuffixTree("fnqduxcvscxggb")
    # solution = SuffixTree("rfvvrivuly")
    solution._ukkonen()
    print(solution.search("l"))
    solution.printTree()
    # solution(["fnqduxcvscxggb", "nfcvscxggb", "vsrcvscxggbt"])
    # solution(["aladdin", "adding", "dinner"])
