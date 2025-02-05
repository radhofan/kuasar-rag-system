import os

def clear_pyc_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pyc"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    clear_pyc_files(project_root)
    print("All .pyc files have been removed.")
