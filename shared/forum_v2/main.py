class Animal:
    def __init__(self, name, age, area):
        self.name = name
        self.age = age
        self.area = area

class Cat(Animal):
    def __init__(self, name, age, area, c_type, weight):
        super().__init__(name, age, area)
        self.c_type = c_type
        self.weight = weight

    def __str__(self):
        return f'Name: {self.name}, Age: {self.age}, Type: {self.c_type}, Weight: {self.weight}, Area: {self.area}'

cat = Cat(name='Loki', age=5, c_type='skotland', weight=6, area='pet')

print(cat.__dict__)