import json
import os


def load_test_data(filename: str) -> dict:
    """Load test data from a JSON file in the data/ directory."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    with open(data_path) as f:
        return json.load(f)


def get_user(user_type: str) -> dict:
    """Retrieve user credentials by type from users.json.

    Args:
        user_type: Key in users.json, e.g. 'valid_user', 'invalid_user'.

    Returns:
        Dict with 'username' and 'password' keys.
    """
    return load_test_data("users.json")[user_type]
