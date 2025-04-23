from security.input_sanitizer import InputSanitizer
import pytest

def test_sanitize_valid_input():
    sanitizer = InputSanitizer()
    assert sanitizer.sanitize("Valid input 123") == "Valid input 123"

def test_sanitize_invalid_input():
    sanitizer = InputSanitizer()
    with pytest.raises(ValueError, match="potencialmente malicioso"):
        sanitizer.sanitize("Invalid <script>alert('xss')</script>")