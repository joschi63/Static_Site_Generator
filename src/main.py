from textnode import TextNode, TextType
import os
import shutil

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "http://boot.dev")
    
    copy_content()

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
            


if __name__ == "__main__":
    main()