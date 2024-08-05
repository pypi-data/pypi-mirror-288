#    This file is part of CruscoPoetry.
#
#    CruscoPoetry is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CruscoPoetry is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CruscoPoetry.  If not, see <http://www.gnu.org/licenses/>.
import os
from typing import List


class HtmlElement:

	_INDENT_STRING = "  "

	@property
	def is_not_null(self):
		return True
	
	@property
	def indent_string(self):
		return self.__class__._INDENT_STRING
		
	def join(self, nodes: list):
		"""Takes a list of HtmlElement instances and returns another list where between each pair of two adjacent items of the old list node has been inserted"""
		ret_list = []
		if len(nodes) > 0:
			ret_list.append(nodes[0])
		if len(nodes) > 1:
			for i in range(1, len(nodes)):
				ret_list.append(self)
				ret_list.append(nodes[i])
		return ret_list


class NullNode(HtmlElement):
	"""Utility class to be used instead of the None pointer. It indicates a non-existent HtmlNode and will be rendered as an empty string."""

	def __init__(self):
		self.text = ''

	@property
	def is_not_null(self):
		return False

	def __str__(self):
		return self.text

	def __repr__(self):
		return "NullNode()"
	
	def pretty_print(self, indent: int):
		return ""


class TextNode(HtmlElement):

	def __init__(self, text):
		self.text = text

	def __str__(self):
		return self.text

	def __repr__(self):
		return "TextNode(%s)"%self.text
	
	def pretty_print(self, indent: int):
		return self.indent_string*indent + self.text


class HtmlNode(HtmlElement):

	def __init__(self, tag_name: str, attribs: dict = None, sub_elements: list = None):
		self.tag_name = tag_name
		self.attribs = attribs if attribs != None else {}
		sub_elements = sub_elements if sub_elements != None else []
		

		if type(sub_elements) == list:
			self.sub_elements = sub_elements

		#sub_elements should be passed as a list. However, if a string has been passed, we will assume it is the only text subnode of this node, so we will build a list of one item from it:
		elif type(sub_elements) == str:
			self.sub_elements = [sub_elements,]
		
		#the same happens if a single HtmlElement instance has been passed:
		elif issubclass(sub_elements.__class__, HtmlElement):
			self.sub_elements = [sub_elements,]

		#if instead we have a tuple we will convert it to a list:
		elif type(sub_elements) == tuple:
			self.sub_elements = list(sub_elements)

		else:
			raise RuntimeError("Unallowed type '%s' for sub_elements: %s", type(sub_elements).__name__, sub_elements)

		for i in range(len(self.sub_elements)):
			if type(self.sub_elements[i]) == str:
				self.sub_elements[i] = TextNode(self.sub_elements[i])
		
	def add_class(self, class_name):
		"""Adds a value to the attribute `class` of the node. If the attribute does not exist, creates it."""
		if "class" not in self.attribs.keys():
			self.attribs["class"] = class_name
		else:
			self.attribs["class"] = self.attribs["class"] + " " + class_name
	
	def remove_class(self, class_name: str):
		"""Removes a value from the attribute `class` of the node. If the attribute does not exist, or the argument is not among its values, nothing happens."""
		if "class" in self.attribs.keys():
			classes = self.attribs["class"].split(" ")
			if class_name in classes:
				classes.remove(class_name)
			self.attribs["class"] = ' '.join(classes)
			
	def __getitem__(self, index):
		return self.sub_elements[index]

	def __len__(self):
		return len(self.sub_elements)
		
	def append(self, node):
		"""Appends `node` to the children list of this Node. sub_element can be a string, an instance of HtmlElement or of TextNode"""
		if type(node) == str:
			self.sub_elements.append(TextNode(node))
		elif issubclass(node.__class__, HtmlElement):
			self.sub_elements.append(node)
		else:
			raise RuntimeError("Unallowed type for sub_element: '%s'"%type(node).__name__)
		
	def extend(self, nodes: List[HtmlElement]):
		"""Extends the children list of this Node with the items in `nodes` (which must be either strings or instances of HtmlElement)"""
		for node in nodes:
			self.append(node)
		
	def insert(self, index: int, node):
		"""Inserts `node` at index `index` in the children list of this Node. sub_element can be a string, an instance of HtmlNode or of TextNode"""
		if type(node) == str:
			self.sub_elements.insert(index, TextNode(node))
		elif node.__class__ in (TextNode, self.__class__):
			self.sub_elements.insert(index, node)
		else:
			raise RuntimeError("Unallowed type for sub_element: '%s'"%type(sub_element).__name__)
			
	def pop(self, index: int):
		"""Remove the item at index `index` from the childnodes list and returns it"""
		child = self.sub_elements.pop(index)
		return child

	@classmethod
	def root_node(cls):
		"""Returns a 'html' tagged root node."""
		return cls("html")

	@classmethod
	def head_node(cls):
		"""Returns a 'head' tagged node."""
		return cls("head")

	@classmethod
	def body_node(cls):
		"""Returns a 'body' tagged node."""
		return cls("body")

	@property
	def opening_tag(self):
		ret_str = "<" + self.tag_name
		for key, value in self.attribs.items():
			ret_str += " "
			ret_str += key
			if value != None:
				ret_str += '="%s"'%value
		ret_str += ">"
		return ret_str
	
	@property
	def closing_tag(self):
		return "</%s>"%self.tag_name
	
	def __str__(self):
		ret_str = self.opening_tag
		if len(self.sub_elements) > 0:
			for sub_element in self.sub_elements:
				ret_str += str(sub_element)
			ret_str += self.closing_tag
		return ret_str
		
	def __repr__(self):
		return "HtmlNode(%s, %r, %r)"%(self.tag_name, self.attribs, [sub.__repr__() for sub in self.sub_elements])
	
	def pretty_print(self, indent: int = 0) -> str:
		ret_str = self.indent_string*indent + self.opening_tag
		if len(self.sub_elements) > 0:
			for sub_element in self.sub_elements:
				ret_str += os.linesep
				ret_str += sub_element.pretty_print(indent+1)
			ret_str += os.linesep + self.indent_string*indent + self.closing_tag
		return ret_str
	
	def find_children_by_tag(self, tag: str) -> list:
		html_node_sub_elements = [sub_element for sub_element in self.sub_elements if isinstance(sub_element, HtmlNode)]
		return [sub_element for sub_element in html_node_sub_elements if sub_element.tag_name == tag]


class HtmlDocument:

	def __init__(self, root: HtmlNode):
		if not isinstance(root, HtmlNode):
			raise RuntimeError("HtmlDocument must be initialized by a 'html'-tagged HtmlNode instance.")
		if root.tag_name != 'html':
			raise RuntimeError("HtmlDocument must be initialized by a 'html'-tagged HtmlNode instance.")
		if len(root) != 2:
			raise RuntimeError("Root node must have only two children - 'head' and 'body'.")
		if root[0].tag_name != 'head':
			raise RuntimeError("Root node must have a 'head'-tagged node as first child.")
		if root[1].tag_name != 'body':
			raise RuntimeError("Root node must have a 'body'-tagged node as second child.")
		
		self._root = root
	
	@property
	def root(self):
		return self._root
	
	@property
	def head(self):
		return self._root[0]
	
	@property
	def body(self):
		return self._root[1]
	
	@classmethod
	def create_empty(cls):
		node = HtmlNode.root_node()
		node.append(HtmlNode.head_node())
		node.append(HtmlNode.body_node())
		return cls(node)
	
	def __str__(self):
		ret_str = ''
		ret_str += "<!DOCTPYE html>"
		ret_str += str(self.root)
		return ret_str
	
	def pretty_print(self) -> str:
		ret_str = ''
		ret_str += "<!DOCTPYE html>"
		ret_str += os.linesep
		ret_str += self.root.pretty_print()
		return ret_str

