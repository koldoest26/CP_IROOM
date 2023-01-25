#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import mysql.connector

db = mysql.connector.connect(host = "localhost", user = "adroom", passwd = "adminroom", db = "iroom1")
sensor = sys.argv[1]
valor = sys.argv[2]
cursor=db.cursor(buffered=True)
try:
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", (sensor, str(valor)))
except:
	print ('Error al escribir en la base de datos')
db.commit()
cursor.close()
db.close()

