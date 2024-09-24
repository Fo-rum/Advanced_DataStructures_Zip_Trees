# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

from typing import TypeVar
import math
import random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class ZipNode:
    def __init__(self, key: KeyType, val: ValType, rank: int):
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.rank = rank

class ZipTree:
	def __init__(self):
		self.root = None
		self.number_of_nodes = 0

	@staticmethod
	def get_random_rank() -> int:
		u = random.random()
		rank = int(math.log(1-u)/ math.log(0.5))
		return rank

	def insert(self, key: KeyType, val: ValType, rank: int = -1):
			if rank == -1:
				rank: int = self.get_random_rank()
			node_x = ZipNode(key, val, rank)

			node_y = self.insert_node_recursive(node_x, self.root)
			if node_y is not None:
				self.root = node_y
			self.number_of_nodes = self.number_of_nodes + 1

	def remove(self, key: KeyType):

			self.number_of_nodes = self.number_of_nodes - 1

			curr_node = self.root
			prev = None
			prev_dir = None
			while curr_node is not None and curr_node.key != key:
				prev = curr_node
				prev_dir = "left" if curr_node.key > key else "right"
				curr_node = curr_node.left if curr_node.key > key else curr_node.right
			zip_top = self.zip(curr_node)
			if prev is None:
				self.root = zip_top
				return
			if prev_dir == "left":
				prev.left = zip_top
			else:
				prev.right = zip_top

	def find(self, key: KeyType) -> ValType:
		return self.delete_node_recursive(self.root, key)
	
	def get_size(self) -> int:
		return self.number_of_nodes
	
	def get_height(self) -> int:
		return self.calculate_max_depth(self.root)

	def get_depth(self, key: KeyType):
		return self.calculate_depth(self.root, key)
	
	def insert_node_recursive(self, node: ZipNode, root: ZipNode):
			if root is None:
				return node
			if node.key < root.key:
				if self.insert_node_recursive(node, root.left) is node:
					if node.rank < root.rank:
						root.left = node
					else:
						root.left = node.right
						node.right = root
						return node

			else:
				if self.insert_node_recursive(node, root.right) is node:
					if node.rank <= root.rank:
						root.right = node
					else:
						root.right = node.left
						node.left = root
						return node

	def delete_node_recursive(self, node: ZipNode, target: KeyType):
			if node is not None:
				if node.key is target:
					return node.val
				elif node.key > target:
					return self.delete_node_recursive(node.left, target)
				else:
					return self.delete_node_recursive(node.right, target)

	def zipup(self, x: ZipNode, y: ZipNode):
			if x is None:
				return y
			if y is None:
				return x
			if x.rank < y.rank:
				y.left = self.zipup(x, y.left)
				return y
			else:
				x.right = self.zipup(x.right, y)
				return x

	def zip(self, x):
			if x is None:
				return None
			if x.left is not None and x.right is not None:
				return self.zipup(x.left, x.right)
			if x.left is None:
				return x.right
			if x.right is None:
				return x.left

	def calculate_max_depth(self, node: ZipNode):
			if node is None:
				return -1
			else:
				# Compute the depth of each subtree
				lDepth = self.calculate_max_depth(node.left)
				rDepth = self.calculate_max_depth(node.right)

				# Use the larger one
				if lDepth > rDepth:
					return lDepth + 1
				else:
					return rDepth + 1

	def calculate_depth(self, root: ZipNode, x):
			# Base case
			if root is None:
				return -1

			# Initialize distance as -1
			dist = -1

			# Check if x is current node=
			if root.key == x:
				return dist + 1

			dist = self.calculate_depth(root.left, x)
			if dist >= 0:
				return dist + 1
			dist = self.calculate_depth(root.right, x)
			if dist >= 0:
				return dist + 1
			return dist

	def delete(self, x: KeyType, root: ZipNode):
			if x is root.key:
				return self.zipup(root.left, root.right)
			if x < root.key:
				if root.key is root.left.key:
					root.left = self.zipup(root.left.left, root.left.right)
				else:
					self.delete(x, root.left)
			else:
				if x is root.right.key:
					root.right = self.zipup(root.right, root.right.right)
				else:
					self.delete(x, root.right)
			return root
# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
