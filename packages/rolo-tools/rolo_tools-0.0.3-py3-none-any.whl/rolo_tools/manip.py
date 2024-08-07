"""Functions for manipulating data."""
def truncate(string, char_limit):
    """truncate string to provided character limit"""
    length = char_limit - 3 # 3 for the ellipsis
    if len(string) > length:
        return string[:length] + "..."
    else:
        return string