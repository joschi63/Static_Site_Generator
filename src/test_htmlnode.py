import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node1 = HTMLNode(tag="div", value="Hello", children=None, props={"class": "container"})
        expected_repr1 = "HTMLNode(tag=div, value=Hello, children=None, props={'class': 'container'})"
        self.assertEqual(repr(node1), expected_repr1)

        node2 = HTMLNode(tag="span")
        expected_repr2 = "HTMLNode(tag=span, value=None, children=None, props=None)"
        self.assertEqual(repr(node2), expected_repr2)

        node3 = HTMLNode(value="Just text", props={"style": "color: red"})
        expected_repr3 = "HTMLNode(tag=None, value=Just text, children=None, props={'style': 'color: red'})"
        self.assertEqual(repr(node3), expected_repr3)

    def test_leaf_to_html(self):
        leaf1 = LeafNode(tag="p", value="This is a paragraph.", props={"class": "text"})
        expected_leaf1 = "<p class=\"text\">This is a paragraph.</p>"
        self.assertEqual(leaf1.to_html(), expected_leaf1)

        leaf2 = LeafNode(tag=None, value="Only text")
        expected_leaf2 = "Only text"
        self.assertEqual(leaf2.to_html(), expected_leaf2)

        leaf3 = LeafNode(tag=None, value=None)
        with self.assertRaises(ValueError):
            leaf3.to_html()
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        html_node1 = TextNode.text_node_to_html_node(node1)
        self.assertEqual(html_node1.tag, None)
        self.assertEqual(html_node1.value, "This is a text node")

        node2 = TextNode("This is bold text", TextType.BOLD)
        html_node2 = TextNode.text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "This is bold text")

        node3 = TextNode("This is a link", TextType.LINK, "http://example.com")
        html_node3 = TextNode.text_node_to_html_node(node3)
        self.assertEqual(html_node3.tag, "a")
        self.assertEqual(html_node3.value, "This is a link")
        

if __name__ == "__main__":
    unittest.main()