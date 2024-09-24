# explanations for member functions are provided in requirements.py
# each file that uses a skip list should import it from this file.

from typing import List, TypeVar
import random
from zip_tree import ZipNode, ZipTree

KeyType = TypeVar("KeyType")
ValType = TypeVar("ValType")


class SkipListNode:
    def __init__(self, key: KeyType, val: ValType, level: int):
        self.key: KeyType = key
        self.val: ValType = val
        self.next: List[SkipListNode] = [None] * (
            level + 1
        )  

class SkipList:
    def __init__(self):
        self.max_level: int = 20  
        self.head: SkipListNode = SkipListNode(
            None, None, self.max_level
        )  

    def get_random_level(self, key: KeyType) -> int:
        # Do not change this function. Use this function to determine what level each key should be at. Assume levels start at 0 (i.e. the bottom-most list is at level 0)
        # e.g. for some key x, if get_random_level(x) = 5, then x should be in the lists on levels 0, 1, 2, 3, 4 and 5 in the skip list.
        random.seed(str(key))
        level = 0
        while random.random() < 0.5 and level < 20:
            level += 1
        return level

    def insert(self, key: KeyType, val: ValType, level: int = -1):
        update_info = [None] * (
            self.max_level + 1
        )  
        current = self.head
        
        for i in range(self.max_level, -1, -1):
            while current.next[i] and current.next[i].key < key:
                current = current.next[i]
            update_info[i] = (
                current  
            )
        if level == -1:
            level = self.get_random_level(key)
        newNode = SkipListNode(key, val, level)
        for i in range(level + 1):
            newNode.next[i] = update_info[i].next[i]
            update_info[i].next[i] = newNode

    def remove(self, key: KeyType):
        update_info = [None] * (self.max_level + 1)
        current = self.head
        for i in range(self.max_level, -1, -1):
            while current.next[i] and current.next[i].key < key:
                current = current.next[i]
            update_info[i] = current
        target = current.next[0]  
        if target and target.key == key:
            for i in range(len(target.next)):
                if update_info[i].next[i] != target:
                    break
                update_info[i].next[i] = target.next[i]

    def find(self, key: KeyType) -> ValType:
        current = self.head
        for i in range(self.max_level, -1, -1):
            while current.next[i] and current.next[i].key < key:
                current = current.next[i]
        current = current.next[0] 
        if current and current.key == key:
            return current.val
        return None

    def get_list_size_at_level(self, level: int):
        count = 0
        current = self.head.next[level]
        while current:
            count += 1
            current = current.next[level]
        return count

    def from_zip_tree(self, zip_tree: ZipTree) -> None:
        if not zip_tree.root:
            return
        self.zip_tree_traversal(zip_tree, zip_tree.root)

    def zip_tree_traversal(self, zip_tree: ZipTree, current: ZipNode) -> None:
        if not current:
            return
        self.insert(current.key, current.val, current.rank)
        if current.left:
            self.zip_tree_traversal(zip_tree, current.left)
        if current.right:
            self.zip_tree_traversal(zip_tree, current.right)


# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
