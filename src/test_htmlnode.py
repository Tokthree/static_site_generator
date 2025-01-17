import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
	def test_props_to_html(self):
		node = HTMLNode("a", "value", None, {"href":"https://www.google.com", "target":"_blank"})
		expected = ' href="https://www.google.com" target="_blank"'
		self.assertEqual(node.props_to_html(), expected)

	def test_empty_props(self):
		node = HTMLNode("a", "value")
		expected = ""
		self.assertEqual(node.props_to_html(), expected)

	def test_repr(self):
		node = HTMLNode("a", "value", None, {"href":"https://www.google.com", "target":"_blank"})
		expected = "HTMLNode(a, value, None, {'href': 'https://www.google.com', 'target': '_blank'})"
		self.assertEqual(repr(node), expected)
		
class TestLeafNode(unittest.TestCase):
	def test_to_html(self):
		node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
		expected = '<a href="https://www.google.com">Click me!</a>'
		self.assertEqual(node.to_html(), expected)
		
	def test_no_value(self):
		node = LeafNode("a", None, {"href":"https://www.google.com"})
		with self.assertRaises(ValueError):
			node.to_html()
		
	def test_no_tag(self):
		node = LeafNode(None, "Click me!", {"href":"https://www.google.com"})
		expected = "Click me!"
		self.assertEqual(node.to_html(), expected)
		
	def test_no_props(self):
		node = LeafNode("p", "This is a paragraph.", None)
		expected = "<p>This is a paragraph.</p>"
		self.assertEqual(node.to_html(), expected)
		
class TestParentNode(unittest.TestCase):
	def test_to_html(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "Italic text"),
				LeafNode(None, "Normal text")
			]
		)
		node2 = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				ParentNode(
					"p",
					[
						LeafNode("h1", "Header text"),
						LeafNode("a", "Click me!", {"href":"https://www.google.com"})
					]
				),
				LeafNode("i", "Italic text"),
				LeafNode(None, "Normal text")
			]
		)
		expected = "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>"
		expected2 = '<p><b>Bold text</b>Normal text<p><h1>Header text</h1><a href="https://www.google.com">Click me!</a></p><i>Italic text</i>Normal text</p>'
		self.assertEqual(node.to_html(), expected)
		self.assertEqual(node2.to_html(), expected2)

	def test_no_tag(self):
		node = ParentNode(None, [LeafNode("b", "Bold text")])
		node2 = ParentNode("", [LeafNode("b", "Bold text")])
		node3 = ParentNode("p", [ParentNode(None, [LeafNode("b", "Bold text")])])
		with self.assertRaises(ValueError):
			node.to_html()
		with self.assertRaises(ValueError):
			node2.to_html()
		with self.assertRaises(ValueError):
			node3.to_html()
	
	def test_no_children(self):
		node = ParentNode("p", None)
		node2 = ParentNode("p", [])
		node3 = ParentNode("p", [ParentNode("b", None)])
		with self.assertRaises(ValueError):
			node.to_html()
		with self.assertRaises(ValueError):
			node2.to_html()
		with self.assertRaises(ValueError):
			node3.to_html()


if __name__ == "__main__":
    unittest.main()
