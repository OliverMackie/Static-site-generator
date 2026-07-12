class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("function to_html not implemented")
    
    def props_to_html(self):
        return_string = ""
        if (self.props == None) or (self.props == {}):
            return ""
        for key in self.props:
            return_string += f' {key}="{self.props[key]}"'
        return return_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"