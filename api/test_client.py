import client
import pytest

from schemas import LoanDetails
from pydantic import ValidationError


class TestClientUserInput:
    expected = LoanDetails(
        amount=100000,
        interest=5.5,
        downpayment=20000,
        term=30
    )

    def test_parse_validate_user_input(self):
        user_input = """\namount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n\n"""
        result = client.parse_validate_user_input(user_input)
        assert result == self.expected

    def test_parse_validate_user_input_with_quotes(self):
        user_input = '''"""\namount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n\n"""'''
        result = client.parse_validate_user_input(user_input)
        assert result == self.expected

    def test_parse_validate_user_input_extra_spaces(self):
        user_input ="""\n  amount : 100000\ninterest:5.5 %\ndownpayment :20000\nterm: 30\n  \n\n"""
        result = client.parse_validate_user_input(user_input)
        assert result == self.expected

    def test_parse_validate_user_input_no_percent_sign(self):
        user_input = """\namount: 100000\ninterest: 5.5\ndownpayment: 20000\nterm: 30\n\n"""
        result = client.parse_validate_user_input(user_input)
        assert result == self.expected

    def test_parse_validate_user_input_wrong_signs(self):
        user_input = """\n amount: 100000\ninterest: 5.5&^$#@!()%+=_-\ndownpayment: 20000\nterm: 30\n\n"""
        result = client.parse_validate_user_input(user_input)
        assert result == self.expected

    def test_parse_validate_user_input_bad_input_string(self):
        user_input = """amount100000interest5.5downpayment20000term30"""
        with pytest.raises(ValueError):
            client.parse_validate_user_input(user_input)

    def test_parse_validate_user_input_bad_input_missing_value(self):
        user_input = """\namount: 100000\ninterest: 5.5%\ndownpayment: 20000\n\n"""
        with pytest.raises(ValidationError):
            client.parse_validate_user_input(user_input)

    def test_parse_validate_user_input_bad_input_type_1(self):
        user_input = """\namount: 100000\ninterest: five\ndownpayment: 20000\nterm: 30\n\n"""
        with pytest.raises(ValueError):
            client.parse_validate_user_input(user_input)

    def test_parse_validate_user_input_bad_input_type_2(self):
        # term should be an interger, so right now is set to see any other type as a bad request.
        # If support for input including a floating point is needed, it can easily be implemented by 
        # updating the parser to cast the string to float then to int so it doesn't throw an error
        user_input = """\namount: 100000\ninterest: 5.5\ndownpayment: 20000\nterm: 30.0\n\n"""
        with pytest.raises(ValueError):
            client.parse_validate_user_input(user_input)
