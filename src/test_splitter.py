import unittest
from splitter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitter(unittest.TestCase):
    def test_split_nodes(self):
        node1 = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes1 = split_nodes_delimiter(node1, "**", TextType.BOLD)
        expected_nodes1 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes1, expected_nodes1)

        node2 = TextNode("An *italic* word", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter(node2, "*", TextType.ITALIC)
        expected_nodes2 = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes2, expected_nodes2)

        node3 = TextNode("No formatting here", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter(node3, "**", TextType.BOLD)
        expected_nodes3 = [TextNode("No formatting here", TextType.TEXT)]
        self.assertEqual(new_nodes3, expected_nodes3)

        node4 = TextNode("Unmatched **bold text", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(node4, "**", TextType.BOLD)
        self.assertTrue("End-Delimiter not found" in str(context.exception))

