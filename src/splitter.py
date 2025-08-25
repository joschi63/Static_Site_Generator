from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    if old_nodes.text_type != TextType.TEXT:
        new_nodes.append(old_nodes)

    limited_text = ""
    start = 0
    end = 0

    for i in range(len(old_nodes.text)):
        node = old_nodes.text
        if node[i:i+(len(delimiter))] == delimiter:
            if start == 0:
                start = i + len(delimiter)
            elif end == 0:
                end = i
    
    
    if end == 0 and start == 0:
        return [old_nodes]
    
    if end == 0:
        raise Exception("End-Delimiter not found")
    
    limited_text = old_nodes.text[start:end]

    splitted_nodes = old_nodes.text.split(delimiter)

    for split in splitted_nodes:
        if split == limited_text:
            new_nodes.append(TextNode(split, text_type))
        else:
            new_nodes.append(TextNode(split, TextType.TEXT))    
    return new_nodes
            
    

if __name__ == "__main__":
    print(split_nodes_delimiter(TextNode("This is **bold** text", TextType.TEXT), "**", TextType.BOLD))
   