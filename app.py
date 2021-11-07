from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sympy import *
import math
import os


app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
x = Symbol('x')
y = Symbol('y')
y1 = Symbol('y1')
y2 = Symbol('y2')
fun = vars(math)
@app.route('/')
def index():
    return '<h1>Bienvenido</h1>'

@app.route('/cuarto_orden', methods=['POST'])
def cuarto_orden():
    h = float((request.json['h']))
    n = int((request.json['xf']-request.json['xi'])/h)
    xi = request.json['x']
    yi = request.json['y']
    xsol = [request.json['x']]
    ysol = [request.json['y']]
    f = request.json['funcion']
    for i in range(n):
        k1 = eval(f, fun, {'x': xi, 'y': yi})
        k2 = eval(f, fun, {'x': xi + (1/2) * h, 'y': yi+(1/2)*k1*h})
        k3 = eval(f, fun, {'x': xi + (1/2) * h,
                           'y': yi+(1/2)*k2*h})
        k4 = eval(f, fun, {'x': xi + h, 'y': yi + k3*h})
        xn = xi + h
        yn = yi + (1/6)*(k1 + 2*k2 + 2*k3 + k4)*h
        xsol.append(xn)
        ysol.append(yn)
        xi = xn
        yi = yn
    return jsonify({'x': xsol, 'y': ysol})


@app.route('/orden_superior', methods=['POST'])
def butcher():
    h = float((request.json['h']))
    n = int((request.json['xf']-request.json['xi'])/h)
    xi = request.json['x']
    yi = request.json['y']
    xsol = [request.json['x']]
    ysol = [request.json['y']]
    f = request.json['funcion']
    for i in range(n):
        k1 = eval(f, fun, {'x': xi, 'y': yi})
        k2 = eval(f, fun, {'x': xi + (1/4) * h, 'y': yi+(1/4)*k1*h})
        k3 = eval(f, fun, {'x': xi + (1/4) * h,
                           'y': yi+(1/8)*k1*h + (1/8)*k2*h})
        k4 = eval(f, fun, {'x': xi + (1/2) * h, 'y': yi - (1/2)*k2*h + k3*h})
        k5 = eval(f, fun, {'x': xi + (3/4)*h,
                           'y': yi - (3/16)*k1*h + (9/16)*k4*h})
        k6 = eval(f, fun, {'x': xi + h, 'y': yi - (3/7)
                           * k1*h + (12/7)*k3*h + (8/7)*k5*h})
        xn = xi + h
        yn = yi + (1/90)*(7*k1 + 32*k3 + 12*k4 + 32*k5 + 7*k6)*h
        xsol.append(xn)
        ysol.append(yn)
        xi = xn
        yi = yn
    return jsonify({'x': xsol, 'y': ysol})


@app.route('/cuarto_orden_edo', methods=['POST'])
def rk4_EDO():
    h = float((request.json['h']))
    n = int((request.json['xf']-request.json['xi'])/h)
    ci = request.json['ci']
    funciones = request.json['funciones']
    xsol = [ci[0][0]]
    y1sol = [ci[0][1]]
    y2sol = [ci[1][1]]
    for i in range(n):
        fun1 = funciones[0]
        fun2 = funciones[1]
        k11 = eval(fun1, fun, {'x': xsol[i], 'y1': y1sol[i], 'y2': y2sol[i]})
        k12 = eval(fun2, fun, {'x': xsol[i], 'y1': y1sol[i], 'y2': y2sol[i]})
        k21 = eval(fun1, fun, {
                   'x': xsol[i] + (1/2)*h, 'y1': y1sol[i] + (1/2) * k11*h, 'y2': y2sol[i] + (1/2)*k12*h})
        k22 = eval(fun2, fun, {
                   'x': xsol[i] + (1/2)*h, 'y1': y1sol[i] + (1/2) * k11*h, 'y2': y2sol[i] + (1/2)*k12*h})
        k31 = eval(fun1, fun, {'x': xsol[i] + (1/2)*h, 'y1': y1sol[i]+(1/2)
                               * k21*h, 'y2': y2sol[i]+(1/2)*k22*h})
        k32 = eval(fun2, fun, {'x': xsol[i] + (1/2)*h, 'y1': y1sol[i]+(1/2)
                               * k21*h, 'y2': y2sol[i]+(1/2)*k22*h})
        k41 = eval(
            fun1, fun, {'x': xsol[i]+h, 'y1': y1sol[i]+k31*h, 'y2': y2sol[i]+k32*h})
        k42 = eval(
            fun2, fun, {'x': xsol[i]+h, 'y1': y1sol[i]+k31*h, 'y2': y2sol[i]+k32*h})
        yn1 = y1sol[i] + (1/6)*(k11 + 2*k21 + 2*k31 + k41)*h
        yn2 = y2sol[i] + (1/6)*(k12 + 2*k22 + 2*k32 + k42)*h
        y1sol.append(yn1)
        y2sol.append(yn2)
        xsol.append(xsol[i] + h)

    return jsonify({'x': xsol, 'y1': y1sol, 'y2': y2sol})


@app.route('/simpson_13', methods=['POST'])
def simpson13_multiple():
    a = request.json['a']
    b = request.json['b']
    f = request.json['funcion']
    n = request.json['n']
    if n % 2 != 0:
        raise Exception("N par")
    h = (b-a)/n
    x = np.linspace(a, b, n + 1)
    I = 0
    term_imp = 0
    term_par = 0
    for i in range(1, len(x)-1):
        if i % 2 == 0:
            term_par += eval(f, fun, {'x': x[i]})
        else:
            term_imp += eval(f, fun, {'x': x[i]})

    I = (b-a)*((eval(f, fun, {'x': a}) + 4*term_imp +
                2*term_par+eval(f, fun, {'x': b})) / (3*n))
    return jsonify({'res': I})


@app.route('/simpson_38', methods=['POST'])
def simpson38():
    x0 = request.json['x0']
    xn = request.json['xn']
    f = request.json['funcion']
    h = (xn-x0)/3
    x1 = x0 + h
    x2 = x1 + h
    I = (3*h/8) * (eval(f, fun, {'x': x0}) + 3*eval(f, fun, {'x': x1}
                                                    ) + 3*eval(f, fun, {'x': x2}) + eval(f, fun, {'x': xn}))
    return jsonify({'res': I})


@app.route('/simpson_38_list', methods=['POST'])
def simpson38_list():
    x = request.json['x']
    fx = request.json['fx']
    h = (x[-1]-x[0])/3
    I = (3/8)*h*(fx[0] + 3*fx[1] + 3*fx[2] + fx[-1])
    return jsonify({'res': I})

@app.route('/simpson_13_list', methods=['POST'])
def simpson13_multiple_list():
    x = request.json['x']
    fx = request.json['fx']
    n = len(x)-1    
    termImpar = 0
    termPar = 0
    
    if n%2 != 0:
        return(print("n tiene que ser par"))
    for i in range(1, len(x)-1):
        if i%2 == 0:
            termPar += fx[i]
        else:
            termImpar += fx[i]
    
    I = (x[-1]-x[0])*((fx[0] + 4*termImpar+2*termPar + fx[-1])/(3*n))
    return jsonify({'res': I})

if __name__ == "__main__":
    app.run(port=5000)
