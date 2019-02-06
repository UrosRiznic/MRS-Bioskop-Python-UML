from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from ...modeli.pregled_filmova import SviFilmovi
from ...sqlite_init import konekcija_ka_bazi

class AddPregledSvihFilmova(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        #konekcija ka bazi podataka - sqlite #####################################
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()
        ###########################################################################
        self.setWindowTitle("PREGLED SVIH FILMOVA")
        self.resize(700, 550)

        self.plugin_proizvodi_layout = QtWidgets.QVBoxLayout()

        self.table_view = QtWidgets.QTableView(self)
        self._prikaz_svih_proizvoda_iz_baze()
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.on_accept)
        #self.button_box.rejected.connect(self.on_reject)


        #self._populate_table()

        self.plugin_proizvodi_layout.addWidget(self.table_view)
        self.plugin_proizvodi_layout.addWidget(self.button_box)

        self.setLayout(self.plugin_proizvodi_layout)

    def on_accept(self):

        return self.accept()

    def _prikaz_svih_proizvoda_iz_baze(self):

        self.set_model(SviFilmovi())
        return

    def set_model(self, model):

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
    def get_data(self):
        return{}
