import json
import os


def load_test_data(filename: str) -> dict:
    """Load test data from a JSON file in the data/ directory."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    with open(data_path) as f:
        return json.load(f)


def get_test_data(filename: str, *keys: str):
    """Retrieve any value from any JSON file by following a chain of keys.

    Args:
        filename: JSON file name in the data/ directory, e.g. 'users.json'.
        *keys:    One or more keys to drill into the JSON structure.

    Returns:
        The value found at the given key path — dict, list, str, int, etc.

    Examples:
        get_test_data("users.json", "valid_user")
        get_test_data("users.json", "valid_user", "email")
        get_test_data("search_terms.json", "valid_searches")
    """
    data = load_test_data(filename)
    for key in keys:
        data = data[key]
    return data
