import flet as ft
from pygments.lexers.css import common_sass_tokens


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))

        #disabilito gli altri pulsanti finchè non schiaccio quello
        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()

    def handleCompConnessa(self,e):
        txtIdOggetto = self._view._txtIdOggetto.value #recupero l'input dell'utente

        #FACCIO DEI CONTROLLI
        #1) CONTROLLO SE è VUOTO
        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, inserire un valore nel campo id.", color="red"))
            self._view.update_page()
            return

        #2) CONTROLLO CHE VENGA INSERITO UN INTERO
        try:
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione, inserire un valore numerico nel campo id.", color="red"))
            self._view.update_page()
            return

        #3) CONTROLLO CHE L'ID AGIUNTO SIA PRESENTE NEL GRAFO
        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione, l'id inserito non è presente nel grafo.", color="orange"))
            self._view.update_page()
            return

        #4) SE ARRIVO QUI VA TUTTO BENE E POSSO RECUPERARE getInfoCompConnessa
        sizeCompConn = self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(
                f"La componente connessa contenente l'oggetto con id {idOggetto} è composta di {sizeCompConn} nodi.",
                color="green"))

        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        lunValues = range(2, sizeCompConn)
        for v in lunValues:
            self._view._ddLun.options.append(ft.dropdown.Option(v))
            #ciclo su tutti i possibili valori di lunghezza e li aggiungp uno a uno

        '''posso fare la stessa cosa col metodo map: gli passo una funzione e una lista.
        Mi rida una nuova lista dove a tutti gli elementi della lista vecchia è stata applicata la funzione'''
        lunValuesDD = (lambda x: ft.dropdown.Option(x), lunValues )


        self._view.update_page()

    def handleCerca(self, e):
        self._model.getNodeFromId(int(self._view.txtIdOggetto.value))
        lun = self._view._ddLun.value
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare un valore di lunghezza tra le scelte proposte",
                                                          color="red"))
            self._view.update_page()
            return

        lunInt= int(lun)
        path, cost= self._model.getOptPath(source, lun)
