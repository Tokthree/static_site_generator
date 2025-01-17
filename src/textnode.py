from enum import Enum
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
	TEXT = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"
	FAKE = "fake"
	

class TextNode:
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url
		
	def __eq__(self, target):
		return self.text == target.text and self.text_type == target.text_type and self.url == target.url
		
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})" 
		
def text_node_to_html_node(text_node):
	TEXT_TYPE_TO_HTML = {
		TextType.TEXT: LeafNode(None, text_node.text),
		TextType.BOLD: LeafNode("b", text_node.text),
		TextType.ITALIC: LeafNode("i", text_node.text),
		TextType.CODE: LeafNode("code", text_node.text),
		TextType.LINK: LeafNode("a", text_node.text, {"href":text_node.url}),
		TextType.IMAGE: LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
	}

	if text_node.text_type not in TEXT_TYPE_TO_HTML:
		raise Exception("Invalid text_type parameter.")
	return TEXT_TYPE_TO_HTML.get(text_node.text_type)
