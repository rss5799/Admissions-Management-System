def filter_dict(data: dict) -> dict:
    """
    Filters out the 'csrf_token' key from a dictionary.
    
    Returns:
        A function that takes a dictionary and returns a new dictionary without the 'csrf_token' key.
    """
    filtered_data = {k: v for k, v in data.items() if k != 'csrf_token'}

    return filtered_data