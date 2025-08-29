from textnode import TextNode, TextType
from markdown import markdown_to_html_node, extract_title
import os
import shutil
from pathlib import Path

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "http://boot.dev")
    
    copy_content()
    generate_page(("content/index.md"), ("template.html"), ("public/index.html"))

def copy_content(from_p = "./static", destination = "./public", first = True, files = []):
    destination_path = os.path.join(destination)
    from_path = os.path.join(from_p)
    if first and os.path.exists(destination_path):
        print(f"removing {destination_path} if it exists")
        shutil.rmtree(destination_path, ignore_errors=True)
        print(f"recreating {destination_path}")
        os.mkdir(destination_path)
    if os.path.exists(from_path):
        list_of_files = os.listdir(from_path)
        for list_file in list_of_files:
            if os.path.isfile(os.path.join(from_path, list_file)):
                print(f"copying {list_file} to {destination_path}")
                shutil.copy(os.path.join(from_path, list_file), destination_path)
            else:
                dir = os.path.join(destination_path, list_file)
                print(f"creating {dir}")
                os.mkdir(dir)
                copy_content(from_p=from_p + "/" + list_file, destination=dir, first = False, files=files)
            
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    from_path_f = open(from_path, "r")
    template_path_f = open(template_path, "r")
    dest_path_f = open(dest_path, "w")
    
    content_from_path = from_path_f.read()
    html = markdown_to_html_node(content_from_path).to_html()

    title = extract_title(content_from_path)

    template_from_path = template_path_f.read()
    template_from_path = template_from_path.replace("{{ Content }}", html)
    template_from_path = template_from_path.replace("{{ Title }}", title)
    
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
        dest_path_f.write(template_from_path)
    else:
        dest_path_f.write(template_from_path)

if __name__ == "__main__":
    main()