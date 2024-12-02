class Identification:
    def __init__(self, identification):
        if not self.is_identification_valid(identification):
            raise ValueError("Invalid identification")
        self.identification = identification

    def get_raw_identification(self):
        return int(self.identification.replace('-', '').replace('.', '')[:-1])

    @staticmethod
    def is_identification_valid(identification):
        identification = identification.replace('-', '').replace('.', '')
        if identification.count('K') + identification.count('k') > 1 or len(identification) < 2 or not identification.replace('K', '').replace('k', '').isnumeric():
            return False
        buffer = 0
        multiplier = 2
        for character in identification[-2::-1]:
            if multiplier > 7:
                multiplier = 2
            buffer += int(character) * multiplier
            multiplier += 1
        buffer = 11 - buffer % 11
        if buffer == 10:
            return identification[-1] == 'K' or identification[-1] == 'k'
        if buffer == 11:
            return identification[-1] == '0'
        return identification[-1] == str(buffer)
