class CelsiusToFahrenheit:
    def __init__(self, temp_string):
        self.exact = int(temp_string) * 9 / 5 + 32
        self.to_tenth = round(self.exact, 1)
