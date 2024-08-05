import os
import shutil
import sys

def create_project(project_name):
    src_dir = os.path.join(os.path.dirname(__file__), 'templates', 'project')
    dst_dir = os.path.join(os.getcwd(), project_name)

    if os.path.exists(dst_dir):
        print(f"Directory {dst_dir} already exists")
        sys.exit(1)

    shutil.copytree(src_dir, dst_dir)
    print(f"Project {project_name} created at {dst_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: silit create-project <project_name>")
        sys.exit(1)

    create_project(sys.argv[1])
