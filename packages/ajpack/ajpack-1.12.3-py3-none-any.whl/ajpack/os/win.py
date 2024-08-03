import subprocess

def get_terminal_output(command: str) -> str:
    """
    Executes a given command in the terminal and returns its output as a string.

    Parameters:
    command (str): The command to execute.

    Returns:
    str: The output from the command execution.
    """
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='replace')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Handle errors and return the error output
        raise ValueError(e.stderr.strip())

# Test
if __name__ == "__main__":
    print(get_terminal_output("s"))