import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self.idMap = {}
    def getStores(self):
        return DAO.getAllStores()


    def buildGraph(self, store_id,k):
        self._grafo.clear()
        self.idMap = {}
        nodi = []
        for o in DAO.getNodes(store_id):
            nodi.append(o)
        self._grafo.add_nodes_from(nodi)
        for n in self._grafo.nodes:
            if n not in self.idMap:
                self.idMap[n.order_id] = n
        self.addEdges(store_id,k)

    def addEdges(self, store_id,k):
        ordini = DAO.getOrdini(store_id)
        print(ordini[:5])  # aggiungi questa riga
        diz = {}
        for orderID, data, numProd in ordini:
            if orderID in self.idMap: # se è un nodo del grafo
                if (orderID, data) not in diz:
                    diz[(orderID, data)] = 0
                diz[(orderID, data)] = numProd


        nodi = list(self._grafo.nodes)
        for i in range(len(nodi)):
            for j in range(i+1, len(nodi)):   # evito coppie di nodi duplicati
                data1 = None
                data2 = None

                order_id1 = nodi[i].order_id
                order_id2 = nodi[j].order_id
                for order, data in diz.keys():
                    if order == order_id1:
                        data1 = data
                    if order == order_id2:
                        data2 = data


                if abs((data1 - data2).days) <= k and abs((data1 - data2).days) > 0:
                    # differenza di GIORNI!!!
                    giorni = abs((data1 - data2).days)
                    peso = (diz[(order_id1,data1)]+ diz[(order_id2, data2)])/ giorni
                    if data1 < data2:
                        self._grafo.add_edge(nodi[i], nodi[j], weight=peso)
                    if data2 < data1:
                        self._grafo.add_edge(nodi[j], nodi[i], weight=peso)




    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)


    def archiPesoMaggiore(self):
        res=[]
        for u,v,d in self._grafo.edges(data=True):
            res.append((u,v,d['weight']))
        res.sort(key=lambda x: x[2], reverse=True)
        return res[:5]



# SOLUZIONE CON DFS --> CAMMINO PIU LUNGO DA UN NODO
    def cercaPercorsoMassimo(self, nodo_partenza):
        # visita in profondità: segue un cammino fino in fondo
        percorso = list(nx.dfs_preorder_nodes(self._grafo, source=nodo_partenza))
        return percorso

    def cercaPercorsoMassimo(self, nodo_partenza):
        self._bestPath= []
        self._ricorsione(nodo_partenza, [nodo_partenza], set([nodo_partenza]))
        return self._bestPath

    def _ricorsione(self, nodoCorrente, parziale, visitati):
        if len(parziale) > len(self._bestPath):
            self._bestPath = list(parziale)

        # esploro successori
        for vicino in self._grafo.successors(nodoCorrente):
            if vicino not in visitati:
                visitati.add(vicino)
                parziale.append(vicino)
                self._ricorsione(vicino, parziale, visitati)
                parziale.pop()
                visitati.remove(vicino)


    # BFS --> percorso minimo tra due nodi
    def  percorsoMinimo(self, nodo_start, nodo_end):
        try:
            # shortest_path usa BFS internamente per grafi non pesati
            percorso = nx.shortest_path(self._grafo,
                                        source=nodo_start,
                                        target=nodo_end)
            return percorso
        except nx.NetworkXNoPath:
            return []


    # ========= RICORSIONE ===============
    def percorsoPesoMassimo(self, nodo_start):
        self._bestPath = []
        self.bestWeight = 0
        self._ricorsione1(nodo_start, [nodo_start], 0, -1)
        return self._bestPath

    def _ricorsione1(self, nodocorrente , parziale, pesoTOT,ultimoPeso):
        # salva solo se hai raggiunto il nodo di destinazione
        #if nodocorrente == nodo_end:                  e aggiungo nodo end come parametro
        if pesoTOT > self.bestWeight:
            self.bestWeight = pesoTOT
            self._bestPath = list(parziale)

        for vicino in self._grafo.successors(nodocorrente):
            if vicino not in parziale:
                peso = self._grafo[nodocorrente][vicino]["weight"]
                if peso < ultimoPeso: # peso strett decrescente degli archi
                    parziale.append(vicino)
                    self._ricorsione1(vicino, parziale, peso+pesoTOT)
                    parziale.pop()