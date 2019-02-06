import sqlite3
def konekcija_ka_bazi():
    return sqlite3.connect('plugins/Bioskop/bioskopBaza.db')
