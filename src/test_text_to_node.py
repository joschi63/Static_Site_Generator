import unittest
from textnode import TextNode, TextType
from splitter import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        node1 = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes1 = text_to_textnodes(node1)
        expected_nodes1 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes1, expected_nodes1)

        node2 = TextNode("this is a **fake bold text, with a link [to boot dev](https://www.boot.dev) and an italic _word_", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            text_to_textnodes(node2)
        self.assertTrue("End-Delimiter not found" in str(context.exception))

        node3 = TextNode("An _italic_ word", TextType.TEXT)
        new_nodes3 = text_to_textnodes(node3)
        expected_nodes3 = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes3, expected_nodes3)

        node4 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes4 = text_to_textnodes(node4)
        expected_nodes4 = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(new_nodes4, expected_nodes4)

        node5 = TextNode("This is some `code` with a little bit of other `code`", TextType.TEXT)
        new_nodes5 = text_to_textnodes(node5)
        expected_nodes5 = [
            TextNode("This is some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with a little bit of other ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(new_nodes5, expected_nodes5)

if __name__ == "__main__":
    unittest.main()




