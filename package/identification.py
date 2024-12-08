"""Provides the Identification class to interact with identifications."""


class Identification:
    """Class to interact with identifications."""
    def __init__(self, identification: str):
        if not self._is_identification_valid(identification):
            raise ValueError("Invalid identification")
        self._identification = int(identification.replace('-', '').replace('.', '')[:-1])

    @staticmethod
    def get_pretty_identification(identification: int):
        """
        Returns a pretty identification.
        :return: Human-readable identification
        """
        return f"{identification:,}-{Identification._get_verification_digit(identification)}".replace(',', '.')

    @staticmethod
    def _get_verification_digit(identification: int):
        multiplier = 2
        result = 0
        for character in str(identification)[::-1]:
            if multiplier > 7:
                multiplier = 2
            result += int(character) * multiplier
            multiplier += 1
        result = 11 - result % 11
        if result == 10:
            return 'K'
        if result == 11:
            return '0'
        return str(result)

    @property
    def identification(self):
        """
        Returns the raw identification.
        :return: Identification with no verification digit
        """
        return self._identification

    @staticmethod
    def _is_identification_valid(identification: str):
        identification = identification.replace('-', '').replace('.', '').replace('k', 'K')
        if identification.count('K') > 1 or len(identification) < 2 or not identification.replace('K', '').isnumeric():
            return False
        return identification[-1] == Identification._get_verification_digit(int(identification[:-1]))
