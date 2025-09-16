from flask import Flask
import math
app = Flask(__name__)

@app.route('/lab2')
def tasks():
    result = f"Task 3.1: {task31()}<br>\
        Task 4.1a: {task41a()}<br>\
        Task 4.1b: {task41b()}<br>\
        Task 5.1: s={task51()[0]}, y={task51()[1]}<br>\
        Task 7.2: {task72()}"
    return result

def task31():
    x = 4
    y = 0
    if x > 1:
        y = math.exp(-x) + abs(x**2 - 1)
    elif -math.pi < x <= 1:
        y = math.log10(math.sqrt(abs(1 - x)))
    else:
        y = "No expression"
    return y

def task41a():
    t = 2.3
    step = 0.8
    while 2.3 <= t <= 7.2:
        y = (math.cos(t ** 2) ** 3) / (1.5 * t + 2)
        t += step
    return y

def task41b():
    t = 0
    step = 0.3
    n = 5
    for t in range(n):
        y = (math.cos(t ** 2) ** 3) / (1.5 * t + 2)
        t += step
    return y

def task51():
    m = 4
    l = 12
    s = 0
    y = 1
    for i in range(4, 17):
        s += (i ** 3 - 2 * i + 3) / (i + 4)

    for j in range(n := m, l + 1):
        y *= (n ** 2 * n + 3) / (n + 3)
    return s, y

def task72():
    b = [5.0, -2.3, -6.9, -1.1, 2.0, 6.6]
    positive_count = (len([num for num in b if num > 0]))
    return positive_count