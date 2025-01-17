import unittest
from textwrap import dedent

from textnode import TextNode, TextType
from convert import *


class TestConvert(unittest.TestCase):
	def test_split_nodes_delimiter(self):
		node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
		node2 = TextNode("This is text with a *italicised phrase* in the middle", TextType.TEXT)
		node3 = TextNode("This is text with a `code block` in the middle", TextType.TEXT)
		node4 = TextNode("This is text with a **bolded phrase and nested *italic* text** in the middle", TextType.TEXT)
		node5 = TextNode("This is text with a trailing **bolded phrase**", TextType.TEXT)
		node6 = TextNode("**A bolded phrase** leads this text", TextType.TEXT)
		node7 = TextNode("This is text with an unclosed **bolded phrase in the middle", TextType.TEXT)
		node8 = TextNode("This is text with an incorrectly closed **bolded phrase* in the middle", TextType.TEXT)
		node9 = TextNode("", TextType.TEXT)
		node10 = TextNode("This is just plain text", TextType.TEXT)
		
		expected = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("bolded phrase", TextType.BOLD),
			TextNode(" in the middle", TextType.TEXT)
		]
		expected2 = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("italicised phrase", TextType.ITALIC),
			TextNode(" in the middle", TextType.TEXT)
		]
		expected3 = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" in the middle", TextType.TEXT)
		]
		expected4 = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("bolded phrase and nested *italic* text", TextType.BOLD),
			TextNode(" in the middle", TextType.TEXT)
		]
		expected5 = [
			TextNode("This is text with a trailing ", TextType.TEXT),
			TextNode("bolded phrase", TextType.BOLD)
		]
		expected6 = [
			TextNode("A bolded phrase", TextType.BOLD),
			TextNode(" leads this text", TextType.TEXT)
		]
		expected9 = []
		expected10 = [TextNode("This is just plain text", TextType.TEXT)]
		
		self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)
		self.assertEqual(split_nodes_delimiter([node2], "*", TextType.ITALIC), expected2)
		self.assertEqual(split_nodes_delimiter([node3], "`", TextType.CODE), expected3)
		self.assertEqual(split_nodes_delimiter([node4], "**", TextType.BOLD), expected4)
		self.assertEqual(split_nodes_delimiter([node5], "**", TextType.BOLD), expected5)
		self.assertEqual(split_nodes_delimiter([node6], "**", TextType.BOLD), expected6)
		with self.assertRaises(ValueError):
			split_nodes_delimiter([node7], "**", TextType.BOLD)
		with self.assertRaises(ValueError):
			split_nodes_delimiter([node8], "**", TextType.BOLD)
		self.assertEqual(split_nodes_delimiter([node9], "**", TextType.BOLD), expected9)
		self.assertEqual(split_nodes_delimiter([node10], "**", TextType.BOLD), expected10)
		
	def test_extract_markdown_images(self):
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

		expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
		expected2 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
		
		self.assertEqual(extract_markdown_images(text), expected)
		self.assertEqual(extract_markdown_links(text2), expected2)
	
	def test_split_nodes_image(self):
		node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) in the middle", TextType.TEXT)
		node2 = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) at the start", TextType.TEXT)
		node3 = TextNode("At the end ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
		node4 = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) in the middle", TextType.TEXT)
		node5 = TextNode("", TextType.TEXT)
		node6 = TextNode(" ", TextType.TEXT)
		node7 = TextNode("This is just plain text", TextType.TEXT)
		node8 = TextNode("This is text with a broken ![rick roll]", TextType.TEXT)
		node9 = TextNode("This is text with a broken !(https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
		node10 = TextNode("This is text with a broken ![rick roll)(https://i.imgur.com/aKaOqIh.gif]", TextType.TEXT)
		
		expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" in the middle", TextType.TEXT)]
		expected2 = [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" at the start", TextType.TEXT)]
		expected3 = [TextNode("At the end ", TextType.TEXT), TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")]
		expected4 = [TextNode("This is text with a ", TextType.TEXT), TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", TextType.TEXT), TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" in the middle", TextType.TEXT)]
		expected5 = [TextNode("", TextType.TEXT)]
		expected6 = [TextNode(" ", TextType.TEXT)]
		expected7 = [TextNode("This is just plain text", TextType.TEXT)]
		expected8 = [TextNode("This is text with a broken ![rick roll]", TextType.TEXT)]
		expected9 = [TextNode("This is text with a broken !(https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)]
		expected10 = [TextNode("This is text with a broken ![rick roll)(https://i.imgur.com/aKaOqIh.gif]", TextType.TEXT)]
		
		self.assertEqual(split_nodes_image([node]), expected)
		self.assertEqual(split_nodes_image([node2]), expected2)
		self.assertEqual(split_nodes_image([node3]), expected3)
		self.assertEqual(split_nodes_image([node4]), expected4)
		self.assertEqual(split_nodes_image([node5]), expected5)
		self.assertEqual(split_nodes_image([node6]), expected6)
		self.assertEqual(split_nodes_image([node7]), expected7)
		self.assertEqual(split_nodes_image([node8]), expected8)
		self.assertEqual(split_nodes_image([node9]), expected9)
		self.assertEqual(split_nodes_image([node10]), expected10)
		
	def test_split_nodes_link(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) in the middle", TextType.TEXT)
		node2 = TextNode("[to boot dev](https://www.boot.dev) at the start", TextType.TEXT)
		node3 = TextNode("At the end [to boot dev](https://www.boot.dev)", TextType.TEXT)
		node4 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) in the middle", TextType.TEXT)
		node5 = TextNode("", TextType.TEXT)
		node6 = TextNode(" ", TextType.TEXT)
		node7 = TextNode("This is just plain text", TextType.TEXT)
		node8 = TextNode("This is text with a broken [to boot dev]", TextType.TEXT)
		node9 = TextNode("This is text with a broken (https://www.boot.dev)", TextType.TEXT)
		node10 = TextNode("This is text with a broken [to boot dev)(https://www.boot.dev]", TextType.TEXT)
		
		expected = [TextNode("This is text with a link ", TextType.TEXT), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" in the middle", TextType.TEXT)]
		expected2 = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" at the start", TextType.TEXT)]
		expected3 = [TextNode("At the end ", TextType.TEXT), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
		expected4 = [TextNode("This is text with a link ", TextType.TEXT), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and ", TextType.TEXT), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), TextNode(" in the middle", TextType.TEXT)]
		expected5 = [TextNode("", TextType.TEXT)]
		expected6 = [TextNode(" ", TextType.TEXT)]
		expected7 = [TextNode("This is just plain text", TextType.TEXT)]
		expected8 = [TextNode("This is text with a broken [to boot dev]", TextType.TEXT)]
		expected9 = [TextNode("This is text with a broken (https://www.boot.dev)", TextType.TEXT)]
		expected10 = [TextNode("This is text with a broken [to boot dev)(https://www.boot.dev]", TextType.TEXT)]
		
		self.assertEqual(split_nodes_link([node]), expected)
		self.assertEqual(split_nodes_link([node2]), expected2)
		self.assertEqual(split_nodes_link([node3]), expected3)
		self.assertEqual(split_nodes_link([node4]), expected4)
		self.assertEqual(split_nodes_link([node5]), expected5)
		self.assertEqual(split_nodes_link([node6]), expected6)
		self.assertEqual(split_nodes_link([node7]), expected7)
		self.assertEqual(split_nodes_link([node8]), expected8)
		self.assertEqual(split_nodes_link([node9]), expected9)
		self.assertEqual(split_nodes_link([node10]), expected10)
		
	def test_text_to_textnodes(self):
		node = ""
		node2 = " "
		node3 = "This is plain text"
		node4 = "This is **text** with an *italic* word and a ```code block``` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		
		expected = []
		expected2 = [TextNode(" ", TextType.TEXT)]
		expected3 = [TextNode("This is plain text", TextType.TEXT)]
		expected4 = [TextNode("This is ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word and a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" and an ", TextType.TEXT), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev")]
		
		self.assertEqual(text_to_textnodes(node), expected)
		self.assertEqual(text_to_textnodes(node2), expected2)
		self.assertEqual(text_to_textnodes(node3), expected3)
		self.assertEqual(text_to_textnodes(node4), expected4)
		
	def test_markdown_to_blocks(self):
		node = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
		
		expected = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
		
		self.assertEqual(markdown_to_blocks(node), expected)
		
	def test_block_to_block_type(self):
		node = "# Title"
		node2 = "```\nsome code\n```"
		node3 = "> first line\n>second line"
		node4 = "* first\n* second"
		node5 = "1. first\n2. second"
		node6 = "1. first\n3. second"
		node7 = ">first line\nsecond line"
		
		expected = "heading"
		expected2 = "code"
		expected3 = "quote"
		expected4 = "unordered_list"
		expected5 = "ordered_list"
		expected6 = "paragraph"
		expected7 = "paragraph"
		
		self.assertEqual(block_to_block_type(node), expected)
		self.assertEqual(block_to_block_type(node2), expected2)
		self.assertEqual(block_to_block_type(node3), expected3)
		self.assertEqual(block_to_block_type(node4), expected4)
		self.assertEqual(block_to_block_type(node5), expected5)
		self.assertEqual(block_to_block_type(node6), expected6)
		self.assertEqual(block_to_block_type(node7), expected7)
		
	def test_markdown_to_html_node(self):
		node = markdown_to_html_node("### Title With **Bold** And *Italic* Text")
		node2 = markdown_to_html_node("```code 1```\n```code 2```")
		node3 = markdown_to_html_node(dedent("""
		> First line
		> Second line
		> Third line"""))
		node4 = markdown_to_html_node(dedent("""
		> This is **bold** text
		> This is *italic* text
		> This is ```code``` text"""))
		node5 = markdown_to_html_node(dedent("""
		* List item 1
		- List item 2
		* List item 3"""))
		node6 = markdown_to_html_node(dedent("""
		* **Bold** list item
		- *Italic* list item
		* ```Code``` list item"""))
		node7 = markdown_to_html_node(dedent("""
		1. List item
		2. List item
		3. List item
		4. List item
		5. List item
		6. List item
		7. List item
		8. List item
		9. List item
		10. List item"""))
		node8 = markdown_to_html_node("Just a plain paragraph")
		
		expected = "<div><h3>Title With <b>Bold</b> And <i>Italic</i> Text</h3></div>"
		expected2 = "<div><pre><code>code 1</code><code>code 2</code></pre></div>"
		expected3 = "<div><blockquote><p>First line</p><p>Second line</p><p>Third line</p></blockquote></div>"
		expected4 = "<div><blockquote><p>This is <b>bold</b> text</p><p>This is <i>italic</i> text</p><p>This is <code>code</code> text</p></blockquote></div>"
		expected5 = "<div><ul><li>List item 1</li><li>List item 2</li><li>List item 3</li></ul></div>"
		expected6 = "<div><ul><li><b>Bold</b> list item</li><li><i>Italic</i> list item</li><li><code>Code</code> list item</li></ul></div>"
		expected7 = "<div><ol><li>List item</li><li>List item</li><li>List item</li><li>List item</li><li>List item</li><li>List item</li><li>List item</li><li>List item</li><li>List item</li><li>List item</li></ol></div>"
		expected8 = "<div><p>Just a plain paragraph</p></div>"
		
		self.assertEqual(node.to_html(), expected)
		self.assertEqual(node2.to_html(), expected2)
		self.assertEqual(node3.to_html(), expected3)
		self.assertEqual(node4.to_html(), expected4)
		self.assertEqual(node5.to_html(), expected5)
		self.assertEqual(node6.to_html(), expected6)
		self.assertEqual(node7.to_html(), expected7)
		self.assertEqual(node8.to_html(), expected8)
		with self.assertRaises(ValueError):
			markdown_to_html_node("")
			
	def test_extract_title(self):
		self.assertEqual(extract_title("# Hello"), "Hello")
		with self.assertRaises(Exception):
			extract_title("")
		with self.assertRaises(Exception):
			extract_title("## Hello")
		with self.assertRaises(Exception):
			extract_title("#")
	


if __name__ == "__main__":
	unittest.main()
