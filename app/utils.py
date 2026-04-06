def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_get_contact(name, search_fn):
    try:
        return search_fn(name)
    except Exception as e:
        print(f"Error searching contact: {e}")
        return None
