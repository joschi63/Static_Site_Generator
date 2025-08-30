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
            
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

if __name__ == "__main__":
    main()