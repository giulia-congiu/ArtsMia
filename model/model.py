import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {} #idMapAO:  chiavi: object_id , valori: artObject
        for n in self._nodes: #n= artObject
            self._idMapAO[n.object_id] = n

    def buildGraph(self):
        # aggiunge i nodi
        self._graph.add_nodes_from(self._nodes)

        # aggiunge gli archi
        self.addEdgesV2()

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def addEdges(self):
        '''cicla su tutte le coppie di nodi, vede il peso dell'arco,
        se non è nullo lo recupera.FUNZIONA MA CI METTE TROPPO TEMPO!
        LO faccio direttamente con la query, prendendomi tutti gli archi'''
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)
                    print(f"Aggiunto arco fra {u} e {v} con peso {peso}")

    def addEdgesV2(self):
        #più semplice e veloce di quello di prima
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getInfoCompConnessa(self, id_oggetto):
        # cercare la componente connessa che contiene l'id_oggetto passato

        #ATTENZIONE CONTROLLA CHE id_oggetto sia contenuto nel grafo.
        if not self.hasNode(id_oggetto):
            return None

        source = self._idMapAO[id_oggetto]

        # Strategia 1: dfs converge= mi rida tutti i nodi collegati al nodo da cui parto a esplorare
        dfsTree = nx.dfs_tree(self._graph, source)
        print("size connessa con dfs_tree", len(dfsTree.nodes())) #prendo tutti i nodi e li conto
        #source è il nodo da cui parto

        # Strategia 2: esplorare albero di visita e restituire i predecessori
        #mi rida un dizionario di predecessori
        dfsPred = nx.dfs_predecessors(self._graph, source)
        print("size connessa con dfs_predecessors", len(dfsPred.values()))
        #conto i valori del dizionario per sapere quanti nodi ci sono, OCCHIO CHE NON CONTA IL NODO SOURCE

        # Strategia 3: USARE I METODI APPOSTI DELLA LIBRERIA
        conn = nx.node_connected_component(self._graph, source)
        #Mi conto la lunghezza di questa componente connessa
        print("size connessa con node_connected_component", len(conn))

        return len(conn)

    def hasNode(self, id_oggetto):
        '''metodo per vedere se un oggetto è contenuto nel grafo
        se c'è rido true altrimenti false'''
        return id_oggetto in self._idMapAO
