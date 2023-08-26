"""
Copyright (c) Jordan Maxwell, All Rights Reserved.
See LICENSE file in the project root for full license information.

Utility methods module for PyDroidDepot. 
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

def dbm_to_hex(dbm_val: int) -> str:
    """
    Convert a dBm value to its corresponding hex integer string.

    Args:
        dbm_val (int): The dBm value to convert.

    Returns:
        str: The hex integer string corresponding to the input dBm value.
    """
        
    dbm_val = int((dbm_val - 0x80) / -1)
    return int_to_hex(dbm_val)

def hex_to_dbm(hex_str: str) -> float:
    """
    Convert a hex integer string to its corresponding dBm value.

    Args:
        hex_str (str): The hex integer string to convert.

    Returns:
        float: The dBm value corresponding to the input hex integer string.
    """

    # Convert the hex integer string to an integer value
    hex_int = int(hex_str, 16)

    # Calculate the dBm value based on the provided range
    dbm_val = (hex_int - 0x80) * -1

    return dbm_val