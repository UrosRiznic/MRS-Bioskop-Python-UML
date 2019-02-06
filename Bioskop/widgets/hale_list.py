from PySide2 import QtWidgets
from PySide2 import QtGui
from ..modeli.glavna_tabela import GlavniMeni
from .dialogs.dodaj_film import DodajFilm
from .dialogs.pregled_svih_filmova import AddPregledSvihFilmova
from .dialogs.pregled_sala import AddPregledSala
from ..sqlite_init import konekcija_ka_bazi



class HaleListWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        self._conn = konekcija_ka_bazi()
        self._c = self._conn.cursor()

        super().__init__(parent)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.hbox_layout2 = QtWidgets.QHBoxLayout()
        self.dodaj_film = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "DODAJ FILM", self)
        self.ukloni_film = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "UKLONI FILM", self)
        self.pregled_svih_filmova = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/binocular-small.png"), "PREGLED SVIH FILMOVA", self)
        self.pregled_sala = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/box.png"), "PREGLED SALA", self)

        self.hbox_layout.addWidget(self.pregled_svih_filmova)

        self.hbox_layout2.addWidget(self.dodaj_film)
        self.hbox_layout2.addWidget(self.ukloni_film)
        self.hbox_layout2.addWidget(self.pregled_sala)

        self.table_view = QtWidgets.QTableView(self)

        self._show_hale_from_db()
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.dodaj_film.clicked.connect(self._on_dodaj_film)
        self.ukloni_film.clicked.connect(self._on_ukloni_film)
        self.pregled_svih_filmova.clicked.connect(self._on_pregled_svih_filmova)
        self.pregled_sala.clicked.connect(self._on_pregled_sala)



        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addLayout(self.hbox_layout2)
        self.vbox_layout.addWidget(self.table_view)

        self.setLayout(self.vbox_layout)

    def set_model(self, model):
        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def _show_hale_from_db(self):
        self.set_model(GlavniMeni())
        return

    def _on_dodaj_film(self):
        dialog = DodajFilm(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            tmpL = dialog.get_data()

            result = self._c.execute("INSERT INTO repertoar (ime_filma, zanr , sala_id, pocetak_projekcije) VALUES (:im , :za , :sa , :pp)" ,{'im' : tmpL['nazivFilma'], 'za' : tmpL['za'], 'sa' : tmpL['salaID'], 'pp' : tmpL['vremeTrajanja']} )
            lastID = self._c.lastrowid # zadnji uneti id
            tmpL['rID'] = lastID
            self._conn.commit()
            self.table_view.model().add(tmpL)


    def _on_ukloni_film(self):
        self.table_view.model().remove(self.table_view.selectedIndexes())

    def _on_pregled_svih_filmova(self):
        dialog = AddPregledSvihFilmova(self.parent())

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            dialog.get_data()

    def _on_pregled_sala(self):
        rows = sorted(set(index.row() for index in
                      self.table_view.selectedIndexes())) #dobijamo redni br reda koji je izabrao korisnik
        if len(rows) == 0:
            return
        selected_halaID = self.table_view.model().get_sala_id_f(rows[0])


        dialog = AddPregledSala(self.parent(), selected_halaID)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            dialog.get_data()
            self._show_hale_from_db()
