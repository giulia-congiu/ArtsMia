from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """SELECT * from objects o """

        cursor.execute(query)

        for row in cursor:
            #row = dizionario
            #il modo più semplice per impacchettare i dati è creare un dto corrispondente alle righe che leggo
            res.append(ArtObject(**row)) #faccio unpack del dizionario e ottengo lista di artObject
            '''**row fa questo = 
            res.append(ArtObject(object_id (NOME PROPRIETà DTO) = 
             row["object_id (NOME COLONNA DATABASE"], ...)) e cosi via '''

        cursor.close()
        conn.close()
        return res

    def testopermegetEdgePeso(self):
        pass
        '''se una coppia di oggetti è stata mostrata nella stessa exibition più di una volta
        devo poter contare queste occorrenze.
        Nel dao prendo due istanze della stessa tabella perchè devo leggere due istanze, 
        ovvero due ID. Le due tabelle le joino uguagliando l'exibition ID che deve essere uguale:
        where eo.exhibition_id = eo2.exhibition_id 

        Devo stare attenta ai selfLoop ovvero gli archi che vengono mostrati con se stessi:
        ovvero partono e arrivano allo stesso objId
        exhibition_id|object_id|exhibition_id|object_id|
        -------------+---------+-------------+---------+
                    2|       44|            2|       44|

        INOLTRE avro anche gli archi 'doppi' andata e ritorno:
        1223|       46|         1223|      219|
        1223|       219|         1223|      46|   

        per risolvere queste cose filtro nel where: 
        and eo.object_id < eo2.object_id 
        
        Prendo nella select i campi che cambiano e li conto
        select eo.object_id  as o1, eo2.object_id  as eo2, count(*)
        
        Infine raggruppo quello che c'è nella count
         '''

    @staticmethod
    def getEdgePeso(v1, v2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """SELECT eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                   FROM exhibition_objects eo, exhibition_objects eo2
                   WHERE eo.exhibition_id = eo2.exhibition_id
                     and eo.object_id < eo2.object_id
                     and eo.object_id = %s  and eo2.object_id = %s
                   group by eo.object_id, eo2.object_id"""

        #questa query dati due nodi mi rida il peso ovvero quante volte
        #sono stati presentati insieme in un exibition
        cursor.execute(query, (v1.object_id, v2.object_id)) #ricordati di dare gli id alla query
        ''' o1|eo2|count(*)|
            --+---+--------+
            46|267|       2|'''

        for row in cursor:
            res.append(row["peso"])

        #CHIUDO PRIMA LA CONNESSIONE POI FACCIO IL CONTROLLO
        cursor.close()
        conn.close()

        #PUO' SUCCEDERE CHE PESO NON ESISTA, devo gestirlo!!!!
        #Perchè quegli oggetti non sono mai mostrati assieme
        if len(res) == 0:
            return None
        return res

    @staticmethod
    def getAllEdges(idMapAO):
        '''idMapAO:
        chiavi: object_id
        valori: artObject'''
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """SELECT eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                   FROM exhibition_objects eo, exhibition_objects eo2
                   WHERE eo.exhibition_id = eo2.exhibition_id
                     and eo.object_id < eo2.object_id
                   group by eo.object_id, eo2.object_id
                   order by peso desc """

        cursor.execute(query)

        for row in cursor:
            # res.append((o1, o2, peso))
            res.append(Arco(idMapAO[row["o1"]], idMapAO[row["o2"]], row["peso"]))
            #recupero gli artObject per oggetto di partenza e arrivo e il peso.

        cursor.close()
        conn.close()
        return res