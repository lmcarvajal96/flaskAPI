from flask import Flask, render_template, request, redirect
from the_app import app
import requests
import sqlite3

BASE_DATOS = app.config['BASE_DATOS']

def todos_los_datos(amount,symbol,convert):
    URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=fb774f8c-16a5-43a8-9f31-8646b426bc3e"
    respuesta = requests.get(URL.format(amount,symbol,convert))
    mijson = respuesta.json()
    price = mijson.get('data')['quote'].get(convert).get("price")
    price = float(price)
    price = round(price,8)
    amount = float(amount)
    preciounitario = amount/price
    preciounitario = round(preciounitario,8)
    print("{} {} son {} {} a un PU de {}".format(amount, symbol, round(price,8),convert,preciounitario))
    return price, preciounitario


def inversion():
    conn = sqlite3.connect(BASE_DATOS)
    cur = conn.cursor()
    query = "SELECT * FROM movimientos;"
    resultado = cur.execute(query).fetchall()
    conn.close()
    invertidosuma = 0
    EURentrada = []
    EURsalida = []
    for linea in resultado:
        if linea[5] == 'EUR' and linea[3] == 'EUR':
            pass
        elif linea[5] == 'EUR':
            EURentrada.append(float(linea[6]))
        elif linea[3] == 'EUR':
            EURsalida.append(float(linea[4]))           
    EURentrada = sum(EURentrada)
    EURsalida = sum(EURsalida)
    EURtotal = EURsalida - EURentrada
    invertido = round(EURtotal,2)
    return invertido
    
def valortotal():
    conn = sqlite3.connect(BASE_DATOS)
    cur = conn.cursor()
    query = "SELECT * FROM movimientos;"
    resultado = cur.execute(query).fetchall()
    conn.close()
    listamonedas = ['BTC', 'ETH', 'XRP','LTC','BNB','USDT', 'BCH','EOS','BSV','XLM','ADA','TRX']
    monedasvalor = {}
    for moneda in listamonedas:
        funcionentrada = []
        funcionsalida = []
        funciontotal = []
        for linea in resultado:
            if linea[5] == moneda and linea[3] == moneda:
                pass
            elif linea[5] == moneda:
                funcionentrada.append(float(linea[6]))
            elif linea[3] == moneda:
                funcionsalida.append(float(linea[4])) 
        funcionentrada = sum(funcionentrada)
        funcionsalida = sum(funcionsalida)
        funciontotal = funcionentrada - funcionsalida 
        monedasvalor[moneda] = funciontotal
    URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=fb774f8c-16a5-43a8-9f31-8646b426bc3e"
    valortotal = 0
    for key, value in monedasvalor.items():
        if value > 0:
            respuesta = requests.get(URL.format(value,key,'EUR'))
            mijson = respuesta.json()
            price = mijson.get('data')['quote'].get('EUR').get("price")
            valortotal += price
    valortotal = round(valortotal,2)
    return valortotal

def monedasvalor():
    conn = sqlite3.connect(BASE_DATOS)
    cur = conn.cursor()
    query = "SELECT * FROM movimientos;"
    resultado = cur.execute(query).fetchall()
    conn.close()
    listamonedas = ['BTC', 'ETH', 'XRP','LTC','BNB','USDT', 'BCH','EOS','BSV','XLM','ADA','TRX']
    monedasvalor = {}
    for moneda in listamonedas:
        funcionentrada = []
        funcionsalida = []
        funciontotal = []
        for linea in resultado:
            if linea[5] == moneda and linea[3] == moneda:
                pass
            elif linea[5] == moneda:
                funcionentrada.append(float(linea[6]))
            elif linea[3] == moneda:
                funcionsalida.append(float(linea[4])) 
        funcionentrada = sum(funcionentrada)
        funcionsalida = sum(funcionsalida)
        funciontotal = funcionentrada - funcionsalida 
        monedasvalor[moneda] = funciontotal
    return monedasvalor

def isfloat(item):
    try:
        item == float(item)
        return True
    except:
        return False

#required oninvalid="this.setCustomValidity('Tienes que rellenar este campo')"