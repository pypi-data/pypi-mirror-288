import os

def create_env(paths: list[str]) -> None:
    """
    Creates the paths provided. (list)
    
    :param paths: The paths to create.
    """
    for path in list(paths):
        if not os.path.exists(path):
            os.makedirs(path)

def create_standard_env() -> None:
    """
    Creates the standard paths for the project.
    (env, env/logs, env/data, env/images)
    """
    paths = [
        "env",
        "env/logs",
        "env/data",
        "env/images",
    ]

    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)