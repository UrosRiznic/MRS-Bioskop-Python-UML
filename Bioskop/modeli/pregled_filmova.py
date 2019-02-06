from PySide2 import QtCore
import os
import sqlite3
from ..sqlite_init import konekcija_ka_bazi

class SviFilmovi(QtCore.QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()
        self._data = []
        self.ucitaj_podatke_iz_baze()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 6 #fiksan br vracamo

    def data(self, index, role):
        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element

    def headerData(self, section, orientation, role):
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "ID"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "NAZIV FILMA"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "ŽANR"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "PRODUCENT"
            elif (section == 4) and (role == QtCore.Qt.DisplayRole):
                return "OCENA"
            elif (section == 5) and (role == QtCore.Qt.DisplayRole):
                return "VREME TRAJANJA"

    def get_element(self, index : QtCore.QModelIndex):
        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def ucitaj_podatke_iz_baze(self):
        result = self._conn.execute(""" SELECT film_id, naziv_filma, zanr, producent, ocena, vreme_trajanja FROM filmovi;""")
        self._data = list(result.fetchall())
        self._conn.commit()
