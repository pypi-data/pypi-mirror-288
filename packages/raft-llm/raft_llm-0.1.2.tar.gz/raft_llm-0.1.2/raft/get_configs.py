import argparse
import shutil
import os
from importlib import resources

def generate_config():
    parser = argparse.ArgumentParser(description='Generate config files')
    parser.add_argument('--output', default='.', help='Output directory')
    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(args.output, exist_ok=True)

    # Access the config directory within the package
    with resources.path('raft_llm.config', '') as template_path:
        for template in os.listdir(template_path):
            src = template_path / template
            dst = os.path.join(args.output, template)
            if src.is_file():
                shutil.copy(src, dst)
                print(f"Generated {dst}")

if __name__ == "__main__":
    generate_config()