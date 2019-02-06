from PySide2 import QtCore
import os
import sqlite3
from ..sqlite_init import konekcija_ka_bazi


class SveSale(QtCore.QAbstractTableModel):

    def __init__(self, salaID):
        super().__init__()
        self.this_salaID = salaID
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o korisniku iz imenika
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()
        self._data = []
        self.ucitaj_podatke_iz_baze()

    def rowCount(self, index):

        return len(self._data)

    def columnCount(self, index):
        return 4 #fiksan br vracamo

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
                return "NAZIV SALE"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "TIP SALE"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "BROJ MESTA"

    def setData(self, index, value, role):

        try:
            if value == "":
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged()
            return True
        except:
            return False

    def flags(self, index):

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def get_element(self, index : QtCore.QModelIndex):

        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None


    def ucitaj_podatke_iz_baze(self):
        result = self._conn.execute("""
        SELECT id_sale , naziv_sale , tip_sale , ukupan_br_mesta FROM sale WHERE id_sale = :salaID """ ,{'salaID' : self.this_salaID})
        self._data = list(result.fetchall())
        self._conn.commit()
        self._conn.close()
