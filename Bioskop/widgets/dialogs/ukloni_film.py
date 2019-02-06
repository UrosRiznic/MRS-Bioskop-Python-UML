from PySide2 import QtWidgets, QtCore, QtGui
from ...sqlite_init import konekcija_ka_bazi

class UkloniFilm(QtWidgets.QDialog):
    def __init__(self, parent=None , halaID=None ,proizvodNaziv = None , ProizvodID = None ):

        super().__init__(parent)
        self.this_naziv_proizvoda = proizvodNaziv
        self.this_proizvodID = ProizvodID
        self.this_halaID = halaID


        #iteracija kroz bazu ---------------------------------------------------

        #rashlladne_hale GET
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()
        self.setWindowTitle("UKLONI FILM")
        self.resize(250, 180)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.proizvod_label = QtWidgets.QLabel(self)
        

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.proizvod_label.setText(self.this_naziv_proizvoda)
        self.form_layout.addRow("FILM:", self.proizvod_label)
        


        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def loop_db_get_element_list(self, stringSELECT):
        self._c = self._conn.cursor()
        self._c = self._conn.execute(stringSELECT)
        return list(self._c.fetchall())

    def loop_list_tuple_to_normal_list(self, listFETCH):
        returnLIST = []
        for item in listFETCH:
            returnLIST.append(item[0])
        return returnLIST

    def _on_accept(self):
        #PROVERA TODO
        temp_input = self.kolicina_input.text()
        if self.da_li_je_int(temp_input):
            temp_input = int(temp_input)
            if (temp_input < 0): #if (temp_input <=100) and (temp_input >=-10):
                QtWidgets.QMessageBox.warning(self,
                "Provera količine", "Količina treba biti veća od 0", QtWidgets.QMessageBox.Ok)
                return
        else:
            QtWidgets.QMessageBox.warning(self,
            "Provera količine2", "Morate uneti brojčanu vrednost!", QtWidgets.QMessageBox.Ok)
            return

        if (temp_input > self.this_p_kolicina):
            QtWidgets.QMessageBox.warning(self,
            "Provera količine3", "Unesite validnu količinu!", QtWidgets.QMessageBox.Ok)
            return
        result2 = self._conn.execute("SELECT naziv_filma FROM filmovi WHERE film_id =:halaid" ,{'halaid' : self.this_halaID} )
        brZazuzetihMesta = list(result2.fetchall())
        brZazuzetihMesta = brZazuzetihMesta[0][0]
        self._conn.commit()

        if (temp_input == self.this_p_kolicina):
            self._c = self._conn.execute("DELETE FROM filmovi WHERE film_id =:pID " ,{'pID' : self.this_proizvodID} )
            self._conn.commit()

        self.accept()

    def get_data(self):
        return ""

    def da_li_je_int(self, input):
        try:
            num = int(input)
        except ValueError:
            return False
        return True
