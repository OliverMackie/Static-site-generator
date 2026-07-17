import os
import shutil
from blocktype import markdown_to_html_node

def copy_content(dest, source):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    if os.path.exists(source):
        source_list = os.listdir(source)
        for file in source_list:
            path = os.path.join(source, file)
            new_dest = os.path.join(dest, file)
            if os.path.isfile(path):
                if not os.path.exists(dest):
                    os.mkdir(dest)
                shutil.copy(path, new_dest)
            else:
                copy_content(new_dest, path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]

def generate_page(from_path, template_path, dest_path, base):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown_file = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    title = extract_title(markdown_file)
    node = markdown_to_html_node(markdown_file)
    html = node.to_html()
    template2 = template.replace("{{ Title }}", title)
    template3 = template2.replace("{{ Content }}", html)
    template4 = template3.replace(f'href="/', f'href="{base}')
    final_html = template4.replace(f'src="/', f'src="{base}')
    dir = os.path.dirname(dest_path)
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
    with open(dest_path, "w+") as file:
        file.write(final_html)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base):
    dirs = os.listdir(dir_path_content)
    for dir in dirs:
        curr_path = os.path.join(dir_path_content, dir)
        curr_dest = os.path.join(dest_dir_path, dir.replace(".md", ".html"))
        if os.path.isfile(curr_path):
            generate_page(curr_path, template_path, curr_dest, base)
        else:
            generate_page_recursive(curr_path, template_path, curr_dest, base)