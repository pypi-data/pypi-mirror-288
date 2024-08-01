import subprocess

def read_data(data: str, pass_exception: bool) -> str:
    """
    'Inputs' the data into the therminal and reads the output.

    :param pass_exception: If the code should skip the line, if it can't be read.
    :return: The output.
    """
    result: str = ""
    line: bytes = b""
    process: subprocess.Popen = subprocess.Popen(str(data), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    for line in iter(process.stdout.readline, b''): #type:ignore
        try: decoded_line = line.decode("utf-8").strip()
        except Exception as e:
            if pass_exception: pass
            else: raise Exception(f"Error while reading the line in '{data}'!")
        
    result += f"{decoded_line}\n"

    process.stdout.close() #type:ignore
    process.wait()

    return result