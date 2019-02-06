from PySide2 import QtWidgets, QtCore, QtGui
from ...sqlite_init import konekcija_ka_bazi

import re

class DodajFilm(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        
        #iteracija kroz tipove hala iz baze za potrebe izbora korisnika --------
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()
        self._c = self._conn.execute("SELECT id_sale, tip_sale, naziv_sale FROM sale" )
        self.lista_sala_db = list(self._c.fetchall())
        self._conn.commit()
        tmpList = []
        for item in self.lista_sala_db:
            tmpList.append("tip sale: " +item[1] + "   naziv: "+ item[2])
        self.salaID  = "" 
        #kraj iteracije kroz bazu ----------------------------------------------

        self.setWindowTitle("DODAJ FILM NA REPERTOAR")

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.naziv_filma_input = QtWidgets.QLineEdit(self)
        self.zanr_input = QtWidgets.QLineEdit(self) # zanr je input. ovde nema comboboxa
        self.vreme_trajanja_input = QtWidgets.QLineEdit(self)
        self.tip_sale_combobox = QtWidgets.QComboBox(self)


        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

    
        self.tip_sale_combobox.addItems(tmpList)
        self.form_layout.addRow("NAZIV FILMA:", self.naziv_filma_input)
        self.form_layout.addRow("ŽANR:", self.zanr_input)
        self.form_layout.addRow("VREME TRAJANJA:", self.vreme_trajanja_input)
        self.form_layout.addRow("Izaberite Salu: " , self.tip_sale_combobox)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self): # ova metoda je modifikovana u odnosu na original

        if self.naziv_filma_input.text() == "":
            QtWidgets.QMessageBox.warning(self,
            "Provera naziva Filma", "Morate popuniti naziv filma", QtWidgets.QMessageBox.Ok)
            return
        if self.vreme_trajanja_input.text() == "":
            QtWidgets.QMessageBox.warning(self,
            "Provera vremena trajanja filma", "Morate uneti vreme trajanja filma", QtWidgets.QMessageBox.Ok)
            return
        if not re.search("^[0-9]+$", self.vreme_trajanja_input.text())  :
            QtWidgets.QMessageBox.warning(self,
            "Provera vremena trajanja filma", "Morate uneti vreme trajanja filma i MORA BITI BROJ", QtWidgets.QMessageBox.Ok)
            return
        
        self.accept()

    def get_data(self):
        izabranINDEX = self.tip_sale_combobox.currentIndex()
        self.salaID  = self.lista_sala_db[izabranINDEX][0]
        nazivS = self.lista_sala_db[izabranINDEX][1]

        return {
            "nazivFilma": self.naziv_filma_input.text(),
            "za" : self.zanr_input.text(),
            "salaID": self.salaID, 
            "vremeTrajanja": self.vreme_trajanja_input.text(),
            "nazivSala" : nazivS
        }
