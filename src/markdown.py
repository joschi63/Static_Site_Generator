from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from splitter import text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "UnorderedList"
    ORDERED_LIST = "OrderedList"

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return "No Title Found"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_children = []

        if block_type == BlockType.CODE:
            code = block.strip("```").strip()
            code = "\n".join(line.lstrip() for line in code.splitlines())
            if not code.endswith("\n"):
                code += "\n"
            children.append(ParentNode(tag="pre", children=[LeafNode(tag="code", value=code)]))
            continue
        elif block_type == BlockType.PARAGRAPH:
        # Zeilen zusammenfügen und überflüssige Leerzeichen entfernen
            block = " ".join(line.strip() for line in block.split("\n"))
            block_children.extend(text_to_children(block, block_type_to_tag(block_type, block)))
        else:
            for text in block.split("\n"):
                block_children.extend(text_to_children(text, block_type_to_tag(block_type, block)))
        children.append(ParentNode(tag=block_type_to_tag(block_type, block), children=block_children))
    new_node = ParentNode(tag="div", children=children)
    
    return new_node

def block_to_block_type(block):
    if block.startswith("#") or block.startswith("##") or block.startswith("###") or block.startswith("####") or block.startswith("#####") or block.startswith("######"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block[0].isdigit() and block[1] == "." and block[2] == " ":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")

    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
        if not blocks[i]:
            blocks.remove(blocks[i])
    return blocks

def block_type_to_tag(block_type, block): 
    if block_type == BlockType.PARAGRAPH:
        return "p"
    elif block_type == BlockType.HEADING:
        if block.startswith("######"):
            return "h6"
        elif block.startswith("#####"):
            return "h5"
        elif block.startswith("####"):
            return "h4"
        elif block.startswith("###"):
            return "h3"
        elif block.startswith("##"):
            return "h2"
        elif block.startswith("#"):
            return "h1"
    elif block_type == BlockType.CODE:
        return "code"
    elif block_type == BlockType.QUOTE:
        return "blockquote"
    elif block_type == BlockType.UNORDERED_LIST:
        return "ul"
    elif block_type == BlockType.ORDERED_LIST:
        return "ol"
    else:
        raise ValueError(f"Unknown block type: {block_type}")

def block_tag_to_sign(block_tag):
    if block_tag == "h1":
        return "#"
    elif block_tag == "h2":
        return "##"
    elif block_tag == "h3":
        return "###"
    elif block_tag == "h4":
        return "####"
    elif block_tag == "h5":
        return "#####"
    elif block_tag == "h6":
        return "######"
    elif block_tag == "blockquote":
        return ">"
    elif block_tag == "ul":
        return "- "
    else:
        return ""

def text_to_children(text, parent_tag):
    
    if parent_tag == "ol":
        text = text.remove(text[0:text.index(".")+2])
    else:
        text = text.strip(block_tag_to_sign(parent_tag))

    text = TextNode(text, TextType.TEXT)
    nodes = text_to_textnodes(text)
    children = []


    for node in nodes:
        children.append(TextNode.text_node_to_html_node(node))
        #print(children)
    #print(children)
    if parent_tag == "ul" or parent_tag == "ol":
        children = [ParentNode(tag="li", children=children)]
    return children

if __name__ == "__main__":
    md = md = """
This is **bolded** paragraph 

- text in a p 
- tag here 

This is another paragraph with _italic_ text and `code` here

"""
    print(markdown_to_html_node(md).to_html())