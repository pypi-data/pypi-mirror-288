import os
import shutil
from importlib import resources


def get_configs(output_dir):
    """
    Copy configuration files from the package data to the specified output directory.

    Args:
    output_dir (str): The directory where config files should be copied.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Access the config directory within the package
        with resources.path("raft.config", "") as config_path:
            for config_file in os.listdir(config_path):
                src = config_path / config_file
                dst = os.path.join(output_dir, config_file)
                if src.is_file():
                    shutil.copy2(src, dst)
                    print(f"Copied {config_file} to {dst}")
    except ImportError:
        print(
            "Error: Unable to access raft.config. Make sure the package is installed correctly."
        )
    except FileNotFoundError:
        print("Error: Config directory not found. Check your package installation.")
