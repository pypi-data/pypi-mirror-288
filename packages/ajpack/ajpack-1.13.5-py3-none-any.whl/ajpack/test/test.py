from typing import Any

def simple_test(txt: Any) -> bool:
    """
    Test that the function works as expected.

    :param txt: Any additional message to show.
    :return: bool --> If the function works.
    """
    green: str = "\033[92m"
    
    print(f"{green}The function works! --> {str(txt)}")
    return True