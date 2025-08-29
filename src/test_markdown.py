import unittest
from markdown import markdown_to_blocks, markdown_to_html_node
from markdown import block_to_block_type, BlockType

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """ This is **bolded** paragraph 

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        
    def test_block_to_block_type(self):
        

        md = """ This is **bolded** paragraph 

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)

        for block in blocks:
            if block == "This is **bolded** paragraph":
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
            elif block == "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line":
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
            elif block == "- This is a list\n- with items":
                self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
            else:
                self.fail(f"Unexpected block: {block}")
    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph 
    text in a p 
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )