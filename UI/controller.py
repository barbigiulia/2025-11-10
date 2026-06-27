import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def readStores(self):
        res = []
        for s in self._model.getStores():
            res.append(ft.dropdown.Option(text=s.store_name,
                                          key= s.store_id))
        return res

    def handleCreaGrafo(self, e):
        store = self._view._ddStore.value
        k = self._view._txtIntK.value
        if store is None or k is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare uno store e un numero intero", color="red"))
            self._view.update_page()
            return
        try:
            k= int(k)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore intero positivo >0", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(int(store), k)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()} ", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}", color="green"))

        self._view.txt_result.controls.append(ft.Text("Cinque archi di peso maggiore", color="orange"))
        lista = self._model.archiPesoMaggiore()
        for u, v, peso in lista:  # è una lista di tuple
            self._view.txt_result.controls.append(ft.Text(f"Arco: {u} --> {v} - peso: {peso}", color="blue"))

        self._view._btnCerca.disabled= False
        self._view._btnRicorsione.disables = False

        self._view.update_page()

    def handleCerca(self, e):

        self._view.update_page()


    def handleRicorsione(self, e):
        pass