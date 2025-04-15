import re
from typing import List, Union
from sqlalchemy.orm import Query


def get_records_by_filter(filter_func, jsonify_results: bool = False) -> Union[List[object], List[dict]]:
    """
    Generic function to search and retrieve records based on a custom filter function.

    Args:
        filter_func (function): A function that returns a SQLAlchemy query object for filtering.
        jsonify_results (bool, optional):
            If True, returns the results as JSON-serializable dictionaries.
            Defaults to False, otherwise returns raw model objects.

    Returns:
        Union[List[object], List[dict]]: 
            - If `jsonify_results` is False, returns a list of model objects (e.g., JobListing instances).
            - If `jsonify_results` is True, returns a list of dictionaries (JSON format).
    """
    # Apply the filter function and execute the query
    records = filter_func()

    return [record.__json__() for record in records] if jsonify_results else records


# Email checking function courtesy https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
def validate_email(email: str) -> bool:
    """
    Checks if a given email is valid.

    Args:
        email (str): The email to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    return True if re.fullmatch(regex, email) else False
