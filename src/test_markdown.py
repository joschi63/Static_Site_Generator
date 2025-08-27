import unittest
from markdown import markdown_to_blocks
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