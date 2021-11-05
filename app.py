from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sympy import *
import math


app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
x = Symbol('x')
y = Symbol('y')
y1 = Symbol('y1')
y2 = Symbol('y2')
fun = vars(math)


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


if __name__ == "__main__":
    app.run(debug=True)
