from the_app import app
from the_app.forms import ProductForm
from flask import Flask, render_template, request, redirect, json, url_for
import sqlite3
from main import todos_los_datos, inversion, valortotal, monedasvalor, isfloat

BASE_DATOS = app.config['BASE_DATOS']


@app.route("/")
def index():
    conn = sqlite3.connect(BASE_DATOS)
    cur = conn.cursor()

    query = "SELECT * FROM movimientos;"
    resultado = cur.execute(query).fetchall()
    conn.close()
    if len(resultado) == 0:
        return render_template('index_inicial.html') 
    else:
        return render_template('index.html', resultado=resultado)   
        

 

@app.route("/nuevatransaccion", methods=['GET','POST'])
def nuevatransaccion():
    form = ProductForm()
    if request.method == 'GET':
        return render_template('nuevatransaccion.html',form=form)
    else:
        try:
            datos = (request.values['from'],request.values['cantidad'],request.values['To'], request.values['PUV'], request.values['monedafromhidden'],request.values['monedatohidden'])
            cantidad = datos[1]
            monedafrom = []
            monedafrom.append(datos[0])
            monedato = []
            monedato.append(datos[2])
            PUV = datos[3]
            monedafromhidden = datos[4]
            monedatohidden = datos[5]
            validacionfrom = monedasvalor()
            localsinif = todos_los_datos(datos[1],datos[0],datos[2])
            preciounitariosinif = '{}'.format(localsinif[1])
            if (float(PUV) - float(preciounitariosinif)) >= 0.00000001 and str(monedafromhidden) == str(datos[0]) and str(monedatohidden) == str(datos[2]) :
                textoerror = []
                textoerror.append("Precio ha cambiado, comprar de nuevo")
                return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
            else:
                if datos[0] == 'EUR':
                    if isfloat(cantidad) == True and float(cantidad) > 0 and datos[2] != 'EUR':
                        local = todos_los_datos(datos[1],datos[0],datos[2])
                        tocantidad = '{}'.format(local[0])
                        preciounitario = '{}'.format(local[1])
                        conn = sqlite3.connect(BASE_DATOS)
                        datos = (request.values['from'],request.values['cantidad'],request.values['To'],tocantidad,preciounitario)
                        cur = conn.cursor()
                        query = "INSERT INTO movimientos ('Fecha','Hora','From','From-Q','To','To-Q','P.U.') VALUES (date('now'),time('now'),?,?,?,?,?)"
                        cur.execute(query,datos)
                        conn.commit()
                        conn.close()
                        return redirect("/")
                    elif isfloat(cantidad) == True and float(cantidad) > 0 and datos[2] == 'EUR':
                        textoerror = []
                        textoerror.append("No se puede convertir la misma moneda")
                        return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
                    else:
                        textoerror = []
                        textoerror.append("Valor no válido")
                        return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)

                else:
                    if  isfloat(cantidad) == True and float(cantidad) <= float(validacionfrom[datos[0]]) and float(cantidad) > 0 and datos[0] != datos[2]:
                        local = todos_los_datos(datos[1],datos[0],datos[2])
                        tocantidad = '{}'.format(local[0])
                        preciounitario = '{}'.format(local[1])
                        conn = sqlite3.connect(BASE_DATOS)
                        datos = (request.values['from'],request.values['cantidad'],request.values['To'],tocantidad,preciounitario)
                        cur = conn.cursor()
                        query = "INSERT INTO movimientos ('Fecha','Hora','From','From-Q','To','To-Q','P.U.') VALUES (date('now'),time('now'),?,?,?,?,?)"
                        cur.execute(query,datos)
                        conn.commit()
                        conn.close()
                        return redirect("/")
                    elif datos[0] == datos[2] and isfloat(cantidad) == True and float(cantidad) <= float(validacionfrom[datos[0]]) and float(cantidad) > 0:
                        textoerror = []
                        textoerror.append("No se puede convertir la misma moneda")
                        return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
                    elif isfloat(cantidad) == True and float(cantidad) > float(validacionfrom[datos[0]]) and float(cantidad) > 0 and datos[0] != datos[2]:
                        textoerror = []
                        textoerror.append("No tienes suficientes monedas de {} \n Tienes: {}".format(monedafrom[0], validacionfrom[datos[0]]))
                        return render_template('nuevatransaccion.html', form=form, textoerror=textoerror)
                    else:
                        textoerror = []
                        textoerror.append("Valor/Cantidad no válida")
                        return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
        except:
            datos = (request.values['from'],request.values['cantidad'],request.values['To'])
            cantidad = datos[1]
            monedafrom = []
            monedafrom.append(datos[0])
            monedato = []
            monedato.append(datos[2])
            validacionfrom = monedasvalor() 
            if datos[0] == 'EUR':
                if isfloat(cantidad) == True and float(cantidad) > 0 and datos[2] != 'EUR':
                    local = todos_los_datos(datos[1],datos[0],datos[2])
                    tocantidad = '{}'.format(local[0])
                    preciounitario = '{}'.format(local[1])
                    conn = sqlite3.connect(BASE_DATOS)
                    datos = (request.values['from'],request.values['cantidad'],request.values['To'],tocantidad,preciounitario)
                    cur = conn.cursor()
                    query = "INSERT INTO movimientos ('Fecha','Hora','From','From-Q','To','To-Q','P.U.') VALUES (date('now'),time('now'),?,?,?,?,?)"
                    cur.execute(query,datos)
                    conn.commit()
                    conn.close()
                    return redirect("/")
                elif isfloat(cantidad) == True and float(cantidad) > 0 and datos[2] == 'EUR':
                    textoerror = []
                    textoerror.append("No se puede convertir la misma moneda")
                    return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
                else:
                    textoerror = []
                    textoerror.append("Valor no válido")
                    return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)

            else:
                if  isfloat(cantidad) == True and float(cantidad) <= float(validacionfrom[datos[0]]) and float(cantidad) > 0 and datos[0] != datos[2]:
                    local = todos_los_datos(datos[1],datos[0],datos[2])
                    tocantidad = '{}'.format(local[0])
                    preciounitario = '{}'.format(local[1])
                    conn = sqlite3.connect(BASE_DATOS)
                    datos = (request.values['from'],request.values['cantidad'],request.values['To'],tocantidad,preciounitario)
                    cur = conn.cursor()
                    query = "INSERT INTO movimientos ('Fecha','Hora','From','From-Q','To','To-Q','P.U.') VALUES (date('now'),time('now'),?,?,?,?,?)"
                    cur.execute(query,datos)
                    conn.commit()
                    conn.close()
                    return redirect("/")
                elif datos[0] == datos[2] and isfloat(cantidad) == True and float(cantidad) <= float(validacionfrom[datos[0]]) and float(cantidad) > 0:
                    textoerror = []
                    textoerror.append("No se puede convertir la misma moneda")
                    return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
                elif isfloat(cantidad) == True and float(cantidad) > float(validacionfrom[datos[0]]) and float(cantidad) > 0 and datos[0] != datos[2]:
                    textoerror = []
                    textoerror.append("No tienes suficientes monedas de {} \n Tienes: {}".format(monedafrom[0], validacionfrom[datos[0]]))
                    return render_template('nuevatransaccion.html', form=form, textoerror=textoerror)
                else:
                    textoerror = []
                    textoerror.append("Valor/Cantidad no válida")
                    return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
                


@app.route("/estado")
def estado():
    invertido1 = inversion()
    valortotal1 = valortotal()
    invertido2 = str(invertido1)
    valortotal2 = str(valortotal1)
    invertidoamount = []
    invertidoamount.append(invertido2)
    valoractualamount = []
    valoractualamount.append(valortotal2)
    return render_template('estado.html', invertido=invertidoamount, valoractual=valoractualamount)

@app.route("/nuevatransaccion-validacion", methods=['GET','POST'])
def calculadora():
    form = ProductForm()
    datos = (request.values['from'],request.values['cantidad'],request.values['To'])
    monedafrom = []
    monedafrom.append(datos[0])
    cantidad = (datos[1])
    monedato = []
    monedato.append(datos[2])
    validacionfrom = monedasvalor()
    monedafromhidden = []
    monedatohidden = []
    monedafromhidden.append('{}'.format(datos[0]))
    monedatohidden.append('{}'.format(datos[2]))
    if datos[0] == 'EUR':
        if isfloat(cantidad) == True and float(cantidad) > 0 and datos[2] != 'EUR':
            local = todos_los_datos(datos[1],datos[0],datos[2])
            preciounitario = []
            preciounitarioanterior = []
            tocantidad = []
            cantidadamount = []
            cantidadamount.append('{}'.format(cantidad))
            tocantidad.append('{}'.format(local[0]))
            preciounitario.append('{}'.format(local[1]))
            preciounitarioanterior.append('{}'.format(local[1]))
            return render_template('transaccion-validada.html',  preciounitario=preciounitario, tocantidad=tocantidad,cantidadamount=cantidadamount,monedafrom=monedafrom,monedato=monedato,form=form, preciounitarioanterior=preciounitarioanterior, monedafromhidden=monedafromhidden,monedatohidden=monedatohidden)
        elif isfloat(cantidad) == True and float(cantidad) > 0 and datos[2] == 'EUR':
            textoerror = []
            textoerror.append("No se puede convertir la misma moneda")
            return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
        else:
            textoerror = []
            textoerror.append("Valor no válido")
            return render_template('nuevatransaccion.html', textoerror=textoerror,form=form)


    else:
        if isfloat(cantidad) == True and float(cantidad) <= float(validacionfrom[datos[0]]) and float(cantidad) > 0 and datos[0] != datos[2]:
            local = todos_los_datos(datos[1],datos[0],datos[2])
            preciounitario = []
            tocantidad = []
            cantidadamount = []
            preciounitarioanterior = []
            cantidadamount.append('{}'.format(cantidad))
            tocantidad.append('{}'.format(local[0]))
            preciounitario.append('{}'.format(local[1]))
            preciounitarioanterior.append('{}'.format(local[1]))
            return render_template('transaccion-validada.html', form=form, preciounitario=preciounitario, tocantidad=tocantidad,cantidadamount=cantidadamount,monedafrom=monedafrom,monedato=monedato,preciounitarioanterior=preciounitarioanterior,monedafromhidden=monedafromhidden,monedatohidden=monedatohidden)
    
        elif datos[0] == datos[2] and isfloat(cantidad) == True and float(cantidad) <= float(validacionfrom[datos[0]]) and float(cantidad) > 0:
            textoerror = []
            textoerror.append("No se puede convertir la misma moneda")
            return render_template('nuevatransaccion.html', textoerror=textoerror, form=form)
        elif isfloat(cantidad) == True and float(cantidad) > float(validacionfrom[datos[0]]) and float(cantidad) > 0:
            textoerror = []
            textoerror.append("No tienes suficientes monedas de {} \n Tienes: {}".format(monedafrom[0], validacionfrom[datos[0]]))
            return render_template('nuevatransaccion.html', form=form, textoerror=textoerror)
        else:
            textoerror = []
            textoerror.append("Valor no válido")
            return render_template('nuevatransaccion.html', form=form, textoerror=textoerror)
    


