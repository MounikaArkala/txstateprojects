#!/usr/local/bin/python
import MySQLdb
from sqlobject import table, db
"""
conn = MySQLdb.connect(host = "rabidpoobear.db",
                       user = 'rabidpoobear',
                       passwd = 'ice1288!!zZ',
                       db = 'musicanalysis')
print conn

"""
d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")
table_name = d.tables()[0]
t = d.table('user')
t.search('first_name="Nico"')
print t[0]