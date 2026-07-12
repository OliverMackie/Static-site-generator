from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        result = ""
        child_res = ""
        if not self.tag:
            raise ValueError("Parent node has no tag")
        if not self.children:
            raise ValueError("Parent node has no children")
        result += f"<{self.tag}>"
        for node in self.children:
            child_res += node.to_html()
        result += f"{child_res}</{self.tag}>"
        return result