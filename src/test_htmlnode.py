import unittest

from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()