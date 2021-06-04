class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage

    def __str__(self):
        return "Our beloved car"

    def __repr__(self):
        return f'{self.__class__.__name__}(color={self.color}, mileage={self.mileage})'


car = Car('red', 9876)
car
