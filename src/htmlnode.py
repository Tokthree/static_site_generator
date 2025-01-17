class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props or {}
	
	def to_html(self):
		raise NotImplementedError
		
	def props_to_html(self):
		output = ""
		for x in self.props:
			output += f' {x}="{self.props[x]}"'
		return output
		
	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
		
class LeafNode(HTMLNode):
	def __init__(self, tag, value, props = None):
		super().__init__(tag, value, None, props)
		
	def to_html(self):
		if not self.value and self.tag != "img":
			raise ValueError("The value parameter must be passed.")
		if not self.tag:
			return self.value
			
		if self.tag == "img":
			return f"<{self.tag}{self.props_to_html()} />"
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
		
class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)
		
	def to_html(self):
		output = ""
	
		if not self.tag:
			raise ValueError("The tag parameter must be passed.")
		if not self.children:
			raise ValueError("The children parameter must be passed.")
		
		output += f"<{self.tag}>"
		for x in self.children:
			output += x.to_html()
		output += f"</{self.tag}>"
		
		return output
			
		
		
		
		
		
		
		
