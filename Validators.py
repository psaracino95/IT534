"""Validation module for input fields.

Contains validation rules for fields according to specifications.
"""


def validate_book_data(title, author, isbn, purchased, available, price):
    """Validate input fields according to assignment requirements.

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    # 1. Check required fields (Title, Author, ISBN, Purchased, Available)
    if not title.strip():
        return False, "Book Title cannot be empty."

    # 2. Author: Letters and spaces only
    # Removes spaces before checking alpha to allow multi-word names like "George Orwell"
    if not author.replace(" ", "").isalpha():
        return False, "Author name must contain letters only."

    # 3. ISBN: Numbers only
    if not isbn.isdigit():
        return False, "ISBN must contain numbers only."

    # 4. Number of copies purchased: Integer
    try:
        purchased_val = int(purchased)
        if purchased_val < 0:
            return False, "Copies purchased must be a non-negative integer."
    except ValueError:
        return False, "Copies purchased must be a valid integer."

    # 5. Number of copies not checked out: Integer
    try:
        available_val = int(available)
        if available_val < 0:
            return False, "Copies available must be a non-negative integer."
    except ValueError:
        return False, "Copies available must be a valid integer."

    # Logical check: Available cannot exceed purchased
    if available_val > purchased_val:
        return (
            False,
            "Copies available cannot be greater than copies purchased.",
        )

    # 6. Retail price: Optional, but must be float if provided
    parsed_price = None
    if price.strip():
        try:
            parsed_price = float(price)
            if parsed_price < 0:
                return False, "Retail price cannot be negative."
        except ValueError:
            return False, "Retail price must be a valid decimal/float number."

    return True, ""