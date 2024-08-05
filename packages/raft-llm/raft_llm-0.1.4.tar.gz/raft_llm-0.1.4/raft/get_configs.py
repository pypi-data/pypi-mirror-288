import os
import shutil
from importlib import resources
import importlib.util


def get_configs(output_dir):
    """
    Copy configuration files from the package data to the specified output directory.

    Args:
    output_dir (str): The directory where config files should be copied.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Check if we're running from the source directory
        raft_spec = importlib.util.find_spec("raft")
        if raft_spec and os.path.isdir(
            os.path.join(os.path.dirname(raft_spec.origin), "config")
        ):
            config_path = os.path.join(os.path.dirname(raft_spec.origin), "config")
            for config_file in os.listdir(config_path):
                if config_file.endswith(".yaml"):
                    src = os.path.join(config_path, config_file)
                    dst = os.path.join(output_dir, config_file)
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                        print(f"Copied {config_file} to {dst}")
        else:
            # We're running from an installed package
            with resources.path("raft.config", "") as config_path:
                for config_file in os.listdir(config_path):
                    if config_file.endswith(".yaml"):
                        src = config_path / config_file
                        dst = os.path.join(output_dir, config_file)
                        if src.is_file():
                            shutil.copy2(src, dst)
                            print(f"Copied {config_file} to {dst}")
    except Exception as e:
        print(f"Error: Unable to access or copy config files. {str(e)}")
        print(
            "Make sure the package is installed correctly and the config files exist."
        )
