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