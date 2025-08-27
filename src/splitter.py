from textnode import TextNode, TextType

import re

def text_to_textnodes(text):
    nodes = [text]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        limited_text = ""
        start = 0
        end = 0

        for i in range(len(old_node.text)):
            node = old_node.text
            if node[i:i+(len(delimiter))] == delimiter:
                if start == 0:
                    start = i + len(delimiter)
                elif end == 0:
                    end = i
        
        if end == 0 and start == 0:
            new_nodes.append(old_node)
            continue
        
        if end == 0:
            raise Exception("End-Delimiter not found")
        
        limited_text = old_node.text[start:end]

        splitted_nodes = old_node.text.split(delimiter)

        for split in splitted_nodes:
            if split == limited_text:
                new_nodes.append(TextNode(split, text_type))
            elif split == "":
                continue
            else:
                new_nodes.append(TextNode(split, TextType.TEXT))    
    if not new_nodes:
        return old_nodes
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        matches = extract_markdown_images(old_node.text)

        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        start = 0
        for j in range(len(matches)):
            alt_text = f"![{matches[j][0]}]"
            
            link = matches[j][1]
    
        
            for i in range(len(old_node.text)):
                if old_node.text[i:i+len(alt_text)] == alt_text:
                    if i > 0:
                        
                        new_nodes.append(TextNode(old_node.text[start:i], TextType.TEXT))
                        new_nodes.append(TextNode(matches[j][0], TextType.IMAGE, link))
                        i = i + len(alt_text) + len(link) + 2
                        start = i
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        start = 0
        for j in range(len(matches)):
            alt_text = f"[{matches[j][0]}]"
            link = matches[j][1]
        
            for i in range(len(old_node.text)):
                if old_node.text[i:i+len(alt_text)] == alt_text:
                    if i > 0:
                        new_nodes.append(TextNode(old_node.text[start:i], TextType.TEXT))
                        new_nodes.append(TextNode(matches[j][0], TextType.LINK, link))
                        i = i + len(alt_text) + len(link) + 2
                        start = i
               
    if not new_nodes:
        return old_nodes
    return new_nodes
        

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

if __name__ == "__main__":
    #print(split_nodes_delimiter(TextNode("This is **bold** text", TextType.TEXT), "**", TextType.BOLD))
    #extract_markdown_images("![rick roll](https://i.imgur.com/aKaOqIh.gif)")
    #extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
    print(text_to_textnodes(TextNode("This is **bold** text with a link [to boot dev](https://www.boot.dev) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and some `code`", TextType.TEXT)))