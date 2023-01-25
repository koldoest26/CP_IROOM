#!/usr/bin/python
# -*- coding: utf-8 -*- 

from flask import Flask, url_for, session, render_template, Response, request, flash, redirect, abort, jsonify
from flaskext.mysql import MySQL
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth
import os
import pathlib
import json
import time

mysql = MySQL()
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('IROOM_SETTINGS', silent=True)
mysql.init_app(app)
last_value = [0,0,0,0,0,0,0,0]

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
 



def event_sensor():
	while True:		   
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute ("select valor from sensors where nombre='temperature' order by time desc")
		temperatura = int(cursor.fetchone()[0])
		if temperatura != last_value[0]:
			sensor = {"tipo":"temperatura", "valor":temperatura}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[0] = temperatura
			#flash('Actualizado sensor de temperatura')
			 
		
		"""PARTE 2: ARRIBA TIENE UN EJEMPLO DE ATUALIZACIÓN DEL SENSOR DE TEMPERATURA POR SSE CUANDO
		SE HA ACTUALIZADO EL VALOR EN LA BASE DE DATOS
		ESCRIBA LE CODIGO PARA EL RESTO DE SENSORES """
		cursor.execute ("select valor from sensors where nombre='light' order by time desc")
		luz = int(cursor.fetchone()[0])
		if luz != last_value[1]:
			sensor = {"tipo":"luz", "valor":luz}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[0] = iluminacion
			#flash('Actualizado sensor de luz')

		cursor.execute ("select valor from sensors where nombre='humidity' order by time desc")
		humedad = int(cursor.fetchone()[0])
		if humedad != last_value[2]:
			sensor = {"tipo":"humedad", "valor":humedad}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[0] = humedad
			#flash('Actualizado sensor de humedad')

		cursor.execute ("select valor from sensors where nombre='sound' order by time desc")
		sonido = int(cursor.fetchone()[0])
		if sonido != last_value[3]:
			sensor = {"tipo":"sonido", "valor":sonido}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[0] = sonido
			#flash('Actualizado sensor de sonido')

		cursor.execute ("select valor from sensors where nombre='motion' order by time desc")
		movimiento = int(cursor.fetchone()[0])
		if movimiento != last_value[4]:
			sensor = {"tipo":"movimiento", "valor":movimiento}
			data_json = json.dumps(sensor)
			print (sensor)
			yield 'data: %s\n\n' % str(data_json)
			last_value[0] = movimiento
			#flash('Actualizado sensor de movimiento')

	   
@app.route('/update_sensor')
def sse_request():	  
	return Response(event_sensor(), mimetype='text/event-stream')
	  
@app.route('/')
def main(): 
	return render_template('index.html')

	
"""
	PARTE 2: INSERTE AQUÍ EL CÓDIGO DE LA FUNCION SENSORS PARA REDIRIGIR A LA VISTA sensors.html 
	CUANDO SE RECIBE UN GET A /sensors
""" 


@app.route('/sensors' , methods=['GET'])
def sensors(): 
	return render_template('sensors.html')


@app.route('/URL/<codigo>')
def web(codigo):
	conn = mysql.connect()
	cursor=conn.cursor()
	cursor.execute("SELECT enlace FROM url WHERE codigo={}".format(codigo))
	recuperar = cursor.fetchone()[0]
	if recuperar is not None:
		return redirect(recuperar)
	else:
		return redirect('/')
	cursor.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('Has entrado en la sesion')
			return redirect(url_for('sensors'))
	return render_template('login.html', error=error)



@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Has salido de la sesion')
	return redirect(url_for('main'))


@app.route('/iluminacion')
def iluminacion():
	return render_template('iluminacion.html')
	

@app.route('/setcolor', methods=['GET'])
def setcolor():
	color=request.args.get('color')
	red = int('0x'+color[1:3], 16)
	green = int('0x'+color[3:5], 16)
	blue = int('0x'+color[5:7], 16)
	conn = mysql.connect()
	cursor=conn.cursor()
	cursor.execute ("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)", ('red', red))
	cursor.execute ("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)", ('green', green))
	cursor.execute ("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)", ('blue', blue))
	conn.commit()
	return '<p>Valores enviados</p>'
	"""
		PARTE 3: INSERTE AQUI EL CÓDIGO PARA GUARDAR EL COLOR DE LA BASE DE DATOS 
		CUANDO SE RECIBE DESDE EL CLIENTE POR AJAX
	""" 


@app.route('/acortador')
def shorturl():
	return render_template('acortador.html')

@app.route('/enviarurl', methods=['GET'])
def acorta():
	url=request.args.get('url')
	conn = mysql.connect()
	cursor=conn.cursor()
	cursor.execute ("INSERT INTO url (enlace)" "VALUES(%s)", (url))
	conn.commit()
	return '<p>Valores enviados</p>'




if __name__=='__main__':
	with app.test_request_context():
		app.debug = True
		app.run(host ='0.0.0.0')
		
