from textnode import TextNode, TextType
from markdown import markdown_to_html_node, extract_title
import os
import shutil
import sys
from pathlib import Path

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "http://boot.dev")
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_content()
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

def copy_content(from_p = "./static", destination = "./docs", first = True, files = []):
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_path_content = os.path.join(dir_path_content)

    if os.path.exists(dir_path_content):
        print(f"Reading directory {dir_path_content}")

        list_of_files = os.listdir(dir_path_content)

        for list_file in list_of_files:
            full_path = os.path.join(dir_path_content, list_file)
            if os.path.isfile(full_path):
                print(f"Generating page for {full_path}")
                full_path_f = open(full_path, "r")
                
                template_path_f = open(template_path, "r")
                dest_dir_path_f = open(os.path.join(dest_dir_path, list_file.replace(".md", ".html")), "w")
                content_md = full_path_f.read()

                title = extract_title(content_md)
                html = markdown_to_html_node(content_md).to_html()
               
                template_from_path = template_path_f.read()
                template_from_path = template_from_path.replace("{{ Content }}", html)
                template_from_path = template_from_path.replace("{{ Title }}", title)
                template_from_path = template_from_path.replace('href="/', f'href="{basepath}')
                template_from_path = template_from_path.replace('src="/', f'src="{basepath}')

                dest_dir_path_f.write(template_from_path)
            elif os.path.isdir(full_path):
                print
                new_dest_dir_path = os.path.join(dest_dir_path, list_file)
                if not os.path.exists(new_dest_dir_path):
                    os.makedirs(new_dest_dir_path)
                generate_pages_recursive(full_path, template_path, new_dest_dir_path)

if __name__ == "__main__":
    main()