from PySide2 import QtCore
import os
import sqlite3
from ..sqlite_init import konekcija_ka_bazi
# glavna stranica
# prikaz bioskopskog repertoara
class GlavniMeni(QtCore.QAbstractTableModel):

    def __init__(self):
        super().__init__()
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o korisniku iz imenika
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()
        self._data = []
        self.ucitaj_podatke_iz_baze()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 5 #fiksan br vracamo

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
                return "SALA"
            elif (section == 4) and (role == QtCore.Qt.DisplayRole):
                return "POCETAK PROJEKCIJE"

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

    def remove(self, indices):
        indices = sorted(set(map(lambda x: x.row(), indices)), reverse=True)
        for i in indices:
            #### remove from DB
            temp_id = self.get_f(i)
            result = self._conn.execute("""DELETE FROM repertoar WHERE repertoar_id = :ID""" , {'ID' : temp_id} )
            self._conn.commit()
            result = self._conn.execute("""DELETE FROM repertoar WHERE repertoar_id = :ID""" , {'ID' : temp_id} )
            self._conn.commit()
			
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self._data[i]
            self.endRemoveRows()

    def add(self, data : dict):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        self._data.append([data['rID'], data['nazivFilma'], data['za'], data['nazivSala'], data['vremeTrajanja'], data['salaID']])
        self.endInsertRows()

    def ucitaj_podatke_iz_baze(self):
        result = self._conn.execute(""" SELECT repertoar_id, ime_filma, zanr, tip_sale, pocetak_projekcije , sala_id FROM repertoar INNER JOIN sale ON sala_id = id_sale ; """)
        self._data = list(result.fetchall())
        self._conn.commit()

    def get_f(self, index):
        return self._data[index][0]

    def get_sala_id_f(self, index):
        return self._data[index][5]
