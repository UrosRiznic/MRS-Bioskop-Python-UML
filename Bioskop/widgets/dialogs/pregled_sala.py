from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from ...modeli.pregled_sala import SveSale
from .ukloni_film import UkloniFilm
from ...sqlite_init import konekcija_ka_bazi

class AddPregledSala(QtWidgets.QDialog): # ova klasa ne bi trebala da postoji. Jer kada se klikne na dugme "Pregled Sala" , nema nikakvih dugmića osim dugmeta "Back"

    def __init__(self, parent=None, salaID=None):
        super().__init__(parent)
        self.this_salaID = salaID
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()
        result = self._conn.execute("SELECT naziv_sale FROM sale WHERE id_sale =:salaid" ,{'salaid' : self.this_salaID} )
        self.hala_naziv = list(result.fetchall())
        self.hala_naziv = self.hala_naziv[0]
        self._conn.commit()



        self.setWindowTitle("Pregled Proizvoda iz [ " + self.hala_naziv[0]+ " ]")
        self.resize(700, 550)

        self.sale_options_layout = QtWidgets.QHBoxLayout()

        self.plugin_sale_layout = QtWidgets.QVBoxLayout()

        self.table_view = QtWidgets.QTableView(self)
        self._prikaz_proizvoda_iz_sale_baza()
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.on_accept)

        self.plugin_sale_layout.addLayout(self.sale_options_layout)
        self.plugin_sale_layout.addWidget(self.table_view)
        self.plugin_sale_layout.addWidget(self.button_box)

        self.setLayout(self.plugin_sale_layout)

    def on_accept(self):

        return self.accept()

    def _prikaz_proizvoda_iz_sale_baza(self):

        self.set_model(SveSale(self.this_salaID))
        return

    def set_model(self, model):

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        return
    def get_data(self):
        return {}
