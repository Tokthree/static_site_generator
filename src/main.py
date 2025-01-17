from os import path, listdir, mkdir, makedirs
from os.path import exists, join, isfile, dirname
from shutil import copy, rmtree, SameFileError
from pathlib import Path

from convert import markdown_to_html_node, extract_title

def copy_folder(source, destination):
	dir_list = listdir(source)
	
	for item in dir_list:
		source_path = join(source, item)
		destination_path = join(destination, item)
		
		if isfile(source_path):
			try:
				copy(source_path, destination_path)
				print(f"Copied file '{source_path}' to '{destination_path}'")
			except SameFileError:
				print(f"Source file '{source_path}' and destination file '{destination_path}' are the same")
			except PermissionError:
				print(f"Permission denied. Check read permission on '{source_path}', and write permission on '{destination_path}'")
			except:
				print(f"Unhandled error occurred while copying file '{source_path}' to '{destination_path}'")
		else:
			mkdir(destination_path)
			print(f"Created directory '{source_path}' at '{destination_path}'")
			copy_folder(source_path, destination_path)

def copy_static():
	static_path = "./static"
	public_path = "./public"
	
	if not exists(static_path) or len(listdir(static_path)) == 0:
		raise Exception("Static directory not found or is empty")
	
	if exists(public_path):
		rmtree(public_path)
		print(f"Cleaned up '{public_path}'")
	mkdir(public_path)
	print(f"Created public directory at '{public_path}'")
	
	copy_folder(static_path, public_path)	
	
def generate_page(from_path, template_path, dest_path):
	if not exists(from_path):
		raise Exception(f"Source file '{from_path}' not found")
	if not exists(template_path):
		raise Exception(f"Template file '{template_path}' not found")
	print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")
	    
	with open(from_path) as markdown_file:
		markdown_raw = markdown_file.read()
		
	with open(template_path) as template_file:
		template_raw = template_file.read()
	
	html_string = markdown_to_html_node(markdown_raw).to_html()
	title_string = extract_title(markdown_raw)
	
	template_new = template_raw.replace("{{ Title }}", title_string).replace("{{ Content }}", html_string)
	
	with open(dest_path, "w") as destination_file:
		destination_file.write(template_new)
		
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	if not exists(dir_path_content):
		raise Exception(f"Source path '{dir_path_content}' does not exist")
	if not exists(template_path):
		raise Exception(f"Template file '{template_path}' not found")
	print(f"Searching for markdown files in '{dir_path_content}'")
	
	dir_list = listdir(dir_path_content)
	
	for item in dir_list:
		source_path = join(dir_path_content, item)
		destination_path = join(dest_dir_path, item)
		
		if isfile(source_path):
			if Path(item).suffix == '.md':
				generate_page(source_path, template_path, join(dest_dir_path, "index.html"))
				print(f"Generating 'index.html' file from '{source_path}' at '{destination_path}' with '{template_path}'")
		else:
			mkdir(destination_path)
			print(f"Created directory '{source_path}' at '{destination_path}'")
			generate_pages_recursive(source_path, template_path, destination_path)
	
	
def main():
	copy_static()
	#generate_page("./content/index.md", "./template.html", "./public/index.html")
	generate_pages_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
	main()
