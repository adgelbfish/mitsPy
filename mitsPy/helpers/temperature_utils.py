class CelsiusToFahrenheit:
    def __init__(self, temp_string):
        self.exact = float(temp_string) * 9 / 5 + 32
        self.to_tenth = round(self.exact, 1)
        self.to_degree = round(self.exact)


class FahrenheitToCelsius:
    def __init__(self, temp_string):
        self.exact = (float(temp_string) - 32) * 5 / 9
        self.to_tenth = round(self.exact, 1)
        self.to_half_degree = round(self.exact * 2) / 2
        self.to_degree = round(self.exact)
