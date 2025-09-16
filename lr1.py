from flask import Flask
import math
app = Flask(__name__)

@app.route('/1')
def task1():
    c = 5
    x = 10
    S = math.log((c*math.exp(-2.5*c+x)+pow(math.atan(abs(c-x)),2))/(abs(pow(-1, -2.5*c)+math.sqrt(abs(math.log(abs(x))+math.log10(abs(c)))))),c)
    return "Result: " + str(S)

@app.route('/2')
def task2():
    a = 3
    b = 0
    result = (6.4 < math.sqrt(a)) and (b < 2*a and 2*a <= 8)
    return "Result: " + str(result)
    
@app.route('/3')
def task3():
    a = -2.004
    b = 0.87
    y = pow(math.atan(1/b),3)
    x = pow((a**2 + b**2),-4.1)
    p = (math.exp(-x*y)+17.4)/(pow(pow(math.sin(x*y),2),1/3))
    return "Result: " + str(p)