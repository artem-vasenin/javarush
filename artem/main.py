import math

foo = {
    'квадрат': lambda x: x**2,
    'куб': lambda x: x**3,
    'корень': lambda x: math.sqrt(x),
    'модуль': lambda x: abs(x),
    'синус': lambda x: math.sin(x),
}
n, name = int(input()), input()
print(foo[name](n))