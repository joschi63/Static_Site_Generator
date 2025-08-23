class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def prop_to_html(self):
        if not self.props:
            return ""
        return " ".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
        if self.props:
            key = list(self.props.keys())[0]
            value = self.props[key]
            return f"<{self.tag}{self.prop_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        self.tag = tag
        self.children = children
        self.props = props
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        for child in self.children:
            if child.children is not None:
                child.to_html()
            return f"<{self.tag}>{child.to_html()}</{self.tag}>"

        
        