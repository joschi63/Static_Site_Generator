from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "UnorderedList"
    ORDERED_LIST = "OrderedList"

def block_to_block_type(block):
    if block.startswith("#") or block.startswith("##") or block.startswith("###") or block.startswith("####") or block.startswith("#####") or block.startswith("######"):
        return BlockType.HEADING
    elif block.startswith(">>>") and block.endswith("<<<"):
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



if __name__ == "__main__":
    md = """This is **bolded** paragraph """
    print(markdown_to_blocks(md))