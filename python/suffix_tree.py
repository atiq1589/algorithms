from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, Optional


@dataclass
class End:
    value: Optional[int] = -1


global_end = End()


@dataclass
class TreeNode:
    children: DefaultDict[str, "TreeNode"] = field(default_factory=lambda: defaultdict(TreeNode))
    suffix_link: Optional["TreeNode"] = None
    start_idx: Optional[int] = None
    end_idx: Optional[End] = global_end


class SuffixTree:
    # _TEXT_STOPPER = chr(0)
    _TEXT_STOPPER = '$'

    def __init__(self, text: str):
        text += self._TEXT_STOPPER
        self._tree_root: TreeNode = TreeNode()
        self._tree_root.suffix_link = self._tree_root

        self._text = text

        self.global_end = global_end

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
                    new_created_node = TreeNode(start_idx=i, suffix_link=self._tree_root)
                    self._active_node.children[char] = new_created_node
                    remaining_chars -= 1
                    if last_tree_node:
                        last_tree_node.suffix_link = self._active_node
                    last_tree_node = self._active_node
                    if self._active_node != self._tree_root:
                        self._active_node = self._active_node.suffix_link
                    elif self._active_length > 0:
                        self._active_edge += 1
                        self._active_length -= 1
                else:
                    edge_start_char = self._text[self._active_edge]
                    edge_char_node = self._active_node.children[edge_start_char]
                    start = edge_char_node.start_idx
                    end = edge_char_node.end_idx.value

                    while self._active_length > end - start + 1:
                        rem = self._active_length - (end - start + 1)
                        for child in edge_char_node.children.values():
                            if self._text[child.start_idx] == self._text[i - rem]:
                                self._active_node = edge_char_node
                                self._active_edge = child.start_idx
                                self._active_length = rem
                        edge_start_char = self._text[self._active_edge]
                        edge_char_node = self._active_node.children[edge_start_char]
                        start = edge_char_node.start_idx
                        end = edge_char_node.end_idx.value

                    if end - start + 1 == self._active_length:
                        self._active_node = edge_char_node
                        self._active_edge = -1
                        self._active_length = 0
                    else:
                        if char == self._text[start + self._active_length]:
                            self._active_length += 1
                            break
                        new_split_node = TreeNode(start_idx=start + self._active_length,
                                                  end_idx=edge_char_node.end_idx,
                                                  suffix_link=self._tree_root)

                        new_split_node.children = edge_char_node.children
                        edge_char_node.children = defaultdict(lambda: TreeNode())

                        edge_char_node.children[self._text[new_split_node.start_idx]] = new_split_node

                        edge_char_node.end_idx = End(start + self._active_length - 1)

                        new_created_node = TreeNode(start_idx=i, suffix_link=self._tree_root)
                        edge_char_node.children[char] = new_created_node
                        remaining_chars -= 1
                        if last_tree_node:
                            last_tree_node.suffix_link = edge_char_node
                        last_tree_node = edge_char_node

                        if self._active_node != self._tree_root:
                            self._active_node = self._active_node.suffix_link
                        else:
                            self._active_edge += 1
                            self._active_length -= 1

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


if __name__ == "__main__":
    # solution = SuffixTree("xyzxyaxyb")
    solution = SuffixTree("mississi")
    # solution = SuffixTree("banana")
    solution._ukkonen()
    solution.printTree()
