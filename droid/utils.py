"""
Utility methods module for PyDroid. 

This code is MIT licensed.
"""

def int_to_hex(num: int) -> str:
    """
    Converts an integer to a hexadecimal string.

    Args:
        num (int): The integer to be converted to a hexadecimal string.

    Returns:
        str: The hexadecimal string representation of the integer.
    """

    hex_str = hex(num)[2:]  # Get the hex string without the '0x' prefix
    if len(hex_str) % 2 != 0:
        hex_str = "0" + hex_str
    
    return hex_str

def hex_to_int(hex_str: str) -> int:
    """
    Converts a hexadecimal string to an integer.

    Args:
        hex_str (str): The hexadecimal string to be converted to an integer.

    Returns:
        int: The integer representation of the hexadecimal string.
    """
    
    return int(hex_str, 16)
