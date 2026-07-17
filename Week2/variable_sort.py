"""Peter Saracino"""

class VariableSort:
    """strings (list): Stores strings containing only upper- and lower-case letters.
    floats (list): Stores floating-point numbers.
    integers (list): Stores integer numbers."""

    def __init__(self):
        """Initializes empty lists for each supported data type."""
        self.strings = []
        self.floats = []
        self.integers = []

    def validate_and_sort(self, raw_value: str) -> str:
        """
        Validates the raw string input, determines its true data type, 
        and appends it to the correct list.

        Args:
            raw_value (str): The raw string input from the user.

        Returns:
            str: A message indicating which list the value was added to.

        Raises:
            ValueError: If the input contains invalid characters for a string,
                        or fails to parse as a valid number.
        """
        # Strip trailing/leading whitespace for cleaner evaluation
        cleaned = raw_value.strip()

        if not cleaned:
            raise ValueError("Input cannot be empty or just spaces.")

        # Step 1: Check if it's an Integer
        try:
            # int() handles negative signs automatically (e.g., "-5")
            int_val = int(cleaned)
            self.integers.append(int_val)
            return f"Successfully added '{int_val}' to Integers."
        except ValueError:
            # Not an integer, move to next check
            pass

        # Step 2: Check if it's a Float
        try:
            # float() handles decimals and negatives (e.g., "-5.5")
            float_val = float(cleaned)
            self.floats.append(float_val)
            return f"Successfully added '{float_val}' to Floats."
        except ValueError:
            # Not a float, move to next check
            pass

        # Step 3: Check if it's a valid Alphabetic String
        # isalpha() ensures ONLY A-Z and a-z characters are present (no numbers, punctuation, spaces)
        if cleaned.isalpha():
            self.strings.append(cleaned)
            return f"Successfully added '{cleaned}' to Strings."
            
        # If it fails all three criteria, it's an invalid/mixed format
        raise ValueError(
            f"'{cleaned}' is invalid. Strings must only contain upper- and lower-case letters (no spaces/symbols)."
        )

    def get_summary(self) -> dict:
        """Returns a dictionary containing all the current sorted lists."""
        return {
            "Strings": self.strings,
            "Floats": self.floats,
            "Integers": self.integers
        }