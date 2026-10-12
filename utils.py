# Helper functions for data conversion
def hex_to_bin(hex_string):
    binary = ""
    for char in hex_string:
        binary += bin(int(char, 16))[2:].zfill(4)
    return binary

def bin_to_hex(binary):
    hex_string = ""
    for i in range(0, len(binary), 4):
        hex_string += hex(int(binary[i:i+4], 2))[2:]
    return hex_string

def string_to_hex(text):
    return ''.join([hex(ord(c))[2:].zfill(2) for c in text])

def hex_to_string(hex_string):
    return ''.join([chr(int(hex_string[i:i+2], 16)) for i in range(0, len(hex_string), 2)])

def pad_text(text):
    """Pad the text to make its length a multiple of 16 (for hex representation)."""
    padding_len = 16 - (len(text) % 16)
    if padding_len == 16:
        return text
    return text + "0" * padding_len

def str_to_hex_key(key_str):
    """Convert an 8-character key to a 16-character hex key."""
    key_str = key_str[:8].ljust(8, '!')  
    hex_key = string_to_hex(key_str)
    return hex_key

def hex_to_latin1(hex_string):
    """Convert a hex string to Latin-1 (ISO 8859-1) encoded text."""
    byte_array = bytearray()
    for i in range(0, len(hex_string), 2):
        if i + 1 < len(hex_string):
            byte_value = int(hex_string[i:i+2], 16)
            byte_array.append(byte_value)
    try:
        return byte_array.decode('latin-1')
    except UnicodeDecodeError:
        return "".join(chr(b) if b < 256 else '?' for b in byte_array)