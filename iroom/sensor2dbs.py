#!/usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Value
import os
import time
import json
import urllib3
import mysql.connector

db = mysql.connector.connect(host = "localhost", user = "adroom", passwd = "adminroom", db = "iroom1")
cursor=db.cursor()


type_sensor = ['temperature', 'humidity', 'light', 'sound', 'motion']
last_value = [0,0,0,0,0,0,0,0]

#PONER LA IP DE LA MÁQUINA VIRTUAL EN LA QUE ESTÉ CORRIENDO EL EMULADOR
server = 'http://192.168.110.128:8000'
#server = 'http://10.0.21.132:8000/'
http = urllib3.PoolManager()
def updateSensor(code):
	value = 0
	try:
		response = http.request('GET', 'http://192.168.110.128:8000/'+type_sensor[code])
		data = json.loads(response.data)
		value = data[type_sensor[code]]

		if value!=last_value[code]:
			last_value[code]=value
			cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", (type_sensor[code], value))
			db.commit()

	except ValueError:
		print ('Error al recibir datos') 
	""" PARTE 1:COMPLETAR AQUÍ EL CÓDIGO PARA LLEER EL VALOR DE UN SENSOR CON API REST"""
	


def controlLightColor():
	try:
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='red' order by time desc""")
		red = int(cursor.fetchone()[0])
		if (red != last_value[5]):
			last_value[5] = red
			print ("red:" + str(red))
			response = http.request('PUT', server+'red/'+str(red))
	except ValueError:
		print ('Error al consultar de base de datos o conectar con iroom')

	try:
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='green' order by time desc""")
		green = int(cursor.fetchone()[0])
		if (green != last_value[6]):
			last_value[6] = green
			print ("green:" + str(green))
			response = http.request('PUT', server+'green/'+str(green))
	except ValueError:
		print ('Error al consultar de base de datos o conectar con iroom')

	try:
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='blue' order by time desc""")
		blue = int(cursor.fetchone()[0])
		if (blue != last_value[7]):
			last_value[7] = blue
			print ("blue:" + str(blue))
			response = http.request('PUT', server+'blue/'+str(blue))
	except ValueError:
		print ('Error al consultar de base de datos o conectar con iroom')

		""" PARTE 1: COMPLETAR AQUI EL RESTO DE CÓDIGO PARA PROCESAR EL COLOR VERDE Y AZUL"""


if __name__ == "__main__":
	cursor=db.cursor(buffered=True)
	cursor.execute ("""DROP table sensors""")
	cursor.execute ("""create table sensors( time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, nombre VARCHAR(15), valor INTEGER)""")
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('temperature', 20))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('humidity', 40))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('light', 30))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('sound', 10))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('motion', 0))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('red', 20))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('blue', 20))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('green', 20))
	db.commit()
	print ('Base de datos creada, comienza la consulta de sensores')
	while True:
		for code in range(0, 5):
			updateSensor(code)
			time.sleep(1)
		controlLightColor()
