"""
"""

def int_to_hex(num: int) -> str:
    """
    """

    hex_str = hex(num)[2:]  # Get the hex string without the '0x' prefix
    if len(hex_str) % 2 != 0:
        hex_str = "0" + hex_str
    
    return hex_str

def hex_to_int(hex_str: str) -> int:
    """
    """
    
    return int(hex_str, 16)
