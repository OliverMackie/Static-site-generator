from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node has no value")
        if not self.tag:
            return f"{self.value}"
        elif not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            prop = self.props_to_html()
            return f"<{self.tag}{prop}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return (f"LeafNode({self.tag}, {self.value}, {self.props})")