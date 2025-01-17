import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)
        
	def test_text_node_to_html_node(self):
		node = text_node_to_html_node(TextNode("Normal text", TextType.TEXT))
		node2 = text_node_to_html_node(TextNode("Bold text", TextType.BOLD))
		node3 = text_node_to_html_node(TextNode("Italic text", TextType.ITALIC))
		node4 = text_node_to_html_node(TextNode("Code text", TextType.CODE))
		node5 = text_node_to_html_node(TextNode("Link text", TextType.LINK, "https://www.google.com"))
		node6 = text_node_to_html_node(TextNode("Image text", TextType.IMAGE, "https://www.imgur.com"))

		expected = "Normal text"
		expected2 = "<b>Bold text</b>"
		expected3 = "<i>Italic text</i>"
		expected4 = "<code>Code text</code>"
		expected5 = '<a href="https://www.google.com">Link text</a>'
		expected6 = '<img src="https://www.imgur.com" alt="Image text" />'
		
		self.assertEqual(node.to_html(), expected)
		self.assertEqual(node2.to_html(), expected2)
		self.assertEqual(node3.to_html(), expected3)
		self.assertEqual(node4.to_html(), expected4)
		self.assertEqual(node5.to_html(), expected5)
		self.assertEqual(node6.to_html(), expected6)
		with self.assertRaises(Exception):
			text_node_to_html_node(TextNode("Fake text", TextType.FAKE))


if __name__ == "__main__":
	unittest.main()
