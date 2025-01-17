import re
from textnode import *
from htmlnode import *
		
def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	
def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
			
		split_results = node.text.split(delimiter)
		if len(split_results) % 2 == 0:
			raise ValueError(f"Unclosed markdown syntax: unbalanced delimiter '{delimiter}' found in text '{node.text}'.")
			
		for i, text in enumerate(split_results):
			if text:
				if i % 2 == 0:
					new_nodes.append(TextNode(text, TextType.TEXT))
				else:
					new_nodes.append(TextNode(text, text_type))
	
	return new_nodes
	
def split_nodes_image(old_nodes):
	new_nodes = []
	
	for node in old_nodes:
		if node.text_type != TextType.TEXT or not extract_markdown_images(node.text):
			new_nodes.append(node)
			continue
		
		current_text = node.text
		for image_tuple in extract_markdown_images(node.text):
			before, after = current_text.split(f"![{image_tuple[0]}]({image_tuple[1]})", 1)
			
			if before:
				new_nodes.append(TextNode(before, TextType.TEXT))
				
			new_nodes.append(TextNode(image_tuple[0], TextType.IMAGE, image_tuple[1]))
			current_text = after
			
		if current_text:
			new_nodes.append(TextNode(current_text, TextType.TEXT))
		
	return new_nodes
	
def split_nodes_link(old_nodes):
	new_nodes = []
	
	for node in old_nodes:
		if node.text_type != TextType.TEXT or not extract_markdown_links(node.text):
			new_nodes.append(node)
			continue
		
		current_text = node.text
		for link_tuple in extract_markdown_links(node.text):
			before, after = current_text.split(f"[{link_tuple[0]}]({link_tuple[1]})", 1)
			
			if before:
				new_nodes.append(TextNode(before, TextType.TEXT))
				
			new_nodes.append(TextNode(link_tuple[0], TextType.LINK, link_tuple[1]))
			current_text = after
			
		if current_text:
			new_nodes.append(TextNode(current_text, TextType.TEXT))
		
	return new_nodes
	
def text_to_textnodes(text):
	nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	
	return nodes
	
def markdown_to_blocks(markdown):
	blocks = []
	
	for block in markdown.split('\n\n'):
		if block:
			blocks.append(block.strip())
	
	return blocks
	
def block_to_block_type(markdown):
	block_types = {
		"heading":r'^#{1,6} ',
		"code":r'(?s)^`{3}.*?`{3}(?=\n|[^\n]|$)',
		"quote":r'^>',
		"unordered_list":r'^[\*-] ',
		"ordered_list":r'^1. '
	}
	
	assumed_type = None
	
	for block_type, pattern in block_types.items():
		if re.match(pattern, markdown):
			assumed_type = block_type
			break
	
	if not assumed_type:
		return "paragraph"
		
	if assumed_type in ["quote", "unordered_list", "ordered_list"]:
		expected_index = 1
		for line in markdown.splitlines():
			if assumed_type in ["quote", "unordered_list"] and not re.match(block_types[assumed_type], line):
				return "paragraph"
			elif assumed_type == "ordered_list" and not line.startswith(f"{expected_index}. "):
				return "paragraph"
				
			expected_index += 1
	
	return assumed_type

def paragraph_constructor(markdown):
	text_nodes = text_to_textnodes(markdown)
	leaf_nodes = []
	
	for text_node in text_nodes:
		leaf_nodes.append(text_node_to_html_node(text_node))
		
	return ParentNode("p", leaf_nodes)
	
def heading_constructor(markdown):
	regex_string = r'^#{1,6} '
	heading_level = len(re.findall(regex_string, markdown)[0].strip())
	
	text_nodes = text_to_textnodes(re.sub(regex_string, "", markdown))
	leaf_nodes = []
	
	for text_node in text_nodes:
		leaf_nodes.append(text_node_to_html_node(text_node))
		
	return ParentNode(f"h{heading_level}", leaf_nodes)
	
def code_constructor(markdown):
	blocks = [match.group(1) for match in re.finditer(r'(```[\s\S]*?```)', markdown)]
	
	text_nodes = []
	leaf_nodes = []
	
	for block in blocks:
		content = re.match(r'```\n?([\s\S]*?)\n?```', block).group(1).strip()
		text_nodes += text_to_textnodes(content)
		
	for text_node in text_nodes:
		leaf_nodes.append(text_node_to_html_node(text_node))
	
	return ParentNode("pre", [ParentNode("code", leaf_nodes)])

def quote_constructor(markdown):
	markdown_lines = markdown.splitlines()
	
	text_nodes = []
	leaf_nodes = []
	
	for line in markdown_lines:
		text_nodes += text_to_textnodes(line.strip("> "))
	
	for text_node in text_nodes:
		leaf_nodes.append(text_node_to_html_node(text_node))
	
	return ParentNode("blockquote", leaf_nodes)
	
def list_item_constructor(markdown):
	text_nodes = text_to_textnodes(markdown)
	leaf_nodes = []

	for text_node in text_nodes:
		leaf_nodes.append(text_node_to_html_node(text_node))
		
	return ParentNode("li", leaf_nodes)
	
def list_constructor(markdown, tag):
	markdown_lines = markdown.splitlines()

	leaf_nodes = []

	for line in markdown_lines:
		if tag == "ul":
			leaf_nodes.append(list_item_constructor(re.sub(r'^[\*-] ', "", line)))
		elif tag == "ol":
			leaf_nodes.append(list_item_constructor(re.sub(r'^\d+\. ', "", line)))
		else:
			raise ValueError("Invalid tag parameter passed")
		
	return ParentNode(tag, leaf_nodes)

def ul_constructor(markdown):
	return list_constructor(markdown, "ul")
	
def ol_constructor(markdown):
	return list_constructor(markdown, "ol")
	
def markdown_to_html_node(markdown):
	if not markdown:
		raise ValueError("Empty document passed as markdown parameter")
		
	blocks = markdown_to_blocks(markdown)
	
	block_handlers = {
		"heading": heading_constructor,
		"code": code_constructor,
		"quote": quote_constructor,
		"unordered_list": ul_constructor,
		"ordered_list": ol_constructor
	}
	
	html_nodes = []
	
	for block in blocks:
		block_type = block_to_block_type(block)
		constructor = block_handlers.get(block_type, paragraph_constructor)
		
		html_nodes.append(constructor(block))
	
	return ParentNode("div", html_nodes)
	
def extract_title(markdown):
	match = re.search(r'^# .*$', markdown, re.MULTILINE)
	
	if not match:
		raise Exception("Valid title not found")
		
	return match.group().lstrip("# ")
	
	
	
	
	
	
