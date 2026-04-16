import secrets
import string
from typing import Tuple

class PasswordGenerator:
    DEFAULT_SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    AMBIGUOUS_CHARS = "0O1lI"

    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = self.DEFAULT_SPECIAL_CHARS

    def generate(
        self,
        length: int,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        if length > 1024:
            raise ValueError("Password length cannot exceed 1024 characters")

        if not any([use_lowercase, use_uppercase, use_digits, use_special]):
            raise ValueError("At least one character type must be enabled")

        character_sets = []
        mandatory_chars = []

        if use_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS_CHARS)
            character_sets.append(chars)
            mandatory_chars.append(secrets.choice(chars))

        if use_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS_CHARS)
            character_sets.append(chars)
            mandatory_chars.append(secrets.choice(chars))

        if use_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS_CHARS)
            character_sets.append(chars)
            mandatory_chars.append(secrets.choice(chars))

        if use_special:
            chars = self.special
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS_CHARS)
            character_sets.append(chars)
            mandatory_chars.append(secrets.choice(chars))

        all_chars = ''.join(character_sets)
        password_list = mandatory_chars[:]

        while len(password_list) < length:
            password_list.append(secrets.choice(all_chars))

        secrets.SystemRandom().shuffle(password_list)
        return ''.join(password_list)

    def calculate_strength(self, password: str, length_override: int = None) -> Tuple[int, str]:
        length = length_override or len(password)
        score = 0

        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_special = any(c in self.special for c in password)

        char_types = sum([has_lower, has_upper, has_digit, has_special])

        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        if length >= 20:
            score += 1

        score += char_types

        if score <= 2:
            return 1, "Weak"
        elif score <= 4:
            return 2, "Fair"
        elif score <= 6:
            return 3, "Strong"
        else:
            return 4, "Very Strong"
