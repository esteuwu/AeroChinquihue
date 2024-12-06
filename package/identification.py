"""Provides the Identification class to interact with identifications."""
# pylint: disable=R0903


class Identification:
    """Class to interact with identifications."""
    def __init__(self, identification: str):
        if not self._is_identification_valid(identification):
            raise ValueError("Invalid identification")
        self.identification = identification

    def get_raw_identification(self):
        """
        Returns the raw identification.
        :return: Identification with no verification digit
        """
        return int(self.identification.replace('-', '').replace('.', '')[:-1])

    @staticmethod
    def _is_identification_valid(identification: str):
        identification = identification.replace('-', '').replace('.', '')
        if identification.count('K') + identification.count('k') > 1 or len(identification) < 2 or not identification.replace('K', '').replace('k', '').isnumeric():
            return False
        multiplier = 2
        result = 0
        for character in identification[-2::-1]:
            if multiplier > 7:
                multiplier = 2
            result += int(character) * multiplier
            multiplier += 1
        result = 11 - result % 11
        if result == 10:
            return identification[-1] == 'K' or identification[-1] == 'k'
        if result == 11:
            return identification[-1] == '0'
        return identification[-1] == str(result)
