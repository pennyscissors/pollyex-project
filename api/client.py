import json
import re
import requests
import sys

from pydantic import ValidationError
from schemas import LoanDetails

def parse_validate_user_input(user_input: str) -> LoanDetails:
    """Parses and validates user input, and populates LoanDetails object.

    An input string (user input from stdin) is taken in to be parsed 
    and validated. The parsed data is then used to populate a LoanDetails
    object.

    Args:
        user_input (str): User input taken from stdin
    
    Returns:
        LoanDetails: Pydantic model object populated with the data that
            was parsed and validated.
    
    Raises:
        ValueError: Raised when the user input doesn't follow the format
            amount: xx.xx
            interest: x.x
            downpayment: xx.xx
            term: xx
        
        ValidationError: When the given data doesn't match the types
            of the Pydantic model.

    """
    # Clean up whitespace and unnecessary characters
    user_input = re.sub(r'[^a-zA-Z0-9\n:.]','', user_input).strip()

    # Convert clean string to list of strings representing key value pairs
    # Ex. "A:1\nB:1\nC:1" -> ['A:1', 'B:2', 'C:3']
    input_list = user_input.split('\n')

    data = {}
    for elem in input_list:
        split_elem = elem.split(':')
        if len(split_elem) != 2:
            raise ValueError("Input cannot be parsed, invalid key value pair")
        else:
            key, value = split_elem
            key = key.lower()
            data[key] = int(value) if key == 'term' else float(value)
    loan_details = LoanDetails(**data)

    return loan_details

def main():
    print("Enter loan details followed by Ctrl+D to signal end of input (press Ctrl+C to quit):")
    user_input = ''.join(sys.stdin.readlines())
    loan_details = parse_validate_user_input(user_input)
    response = requests.get(url="http://localhost:80/payment-details", params=loan_details.dict())
    data = json.loads(response.content)
    print(f"\nResponse (status code: {response.status_code}):\n{json.dumps(data, indent=2)}\n")

if __name__ == "__main__":
    while True:
        try:
            main()
        except (ValueError, ValidationError) as e:
            print(e, '\n')
            continue
        except KeyboardInterrupt:
            break
