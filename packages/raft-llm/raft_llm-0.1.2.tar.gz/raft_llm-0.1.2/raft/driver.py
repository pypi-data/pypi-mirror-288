import subprocess

def run_generation_process(config_path):
    # Define the command to run generate.py with the YAML configuration file
    command = f'python generate.py --config {config_path}'
    
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        # Print the standard output from generate.py
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # Print any errors that occur during the execution of generate.py
        print(f"Error running generate.py: {e.stderr}")

if __name__ == "__main__":
    # Path to the YAML configuration file
    config_path = 'config/sample.yaml'
    
    # Run the generation process
    run_generation_process(config_path)