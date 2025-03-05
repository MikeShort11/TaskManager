from pathlib import Path

def print_directory_tree(start_path, indent=""):
    start_path = Path(start_path)
    for item in sorted(start_path.iterdir()):
        if item.is_dir():
            print(f"{indent}{item.name}/")
            print_directory_tree(item, indent + "  ")
        else:
            print(f"{indent}{item.name}")

if __name__ == "__main__":
    current_dir = Path.cwd()
    print(f"Directory structure of {current_dir}:")
    print_directory_tree(current_dir)