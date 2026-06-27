from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store

class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select s.*
                    from stores s """
        cursor.execute(query)
        for row in cursor:
            results.append(Store(**row))
        cursor.close()
        conn.close()
        return results



    @staticmethod
    def getNodes(store_id):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct o.*
                from orders o 
                where o.store_id = %s
        """
        cursor.execute(query, (store_id,))
        for row in cursor:
            results.append(Order(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getOrdini(store_id):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select o.order_id , o.order_date , sum(oi.quantity ) as numProdotti
                from orders o , order_items oi 
                where o.order_id = oi.order_id 
                and o.store_id = %s
                group by o.order_id , o.order_date
           """
        cursor.execute(query, (store_id,))
        for row in cursor:
            results.append((row["order_id"], row["order_date"], int(row["numProdotti"])))
        cursor.close()
        conn.close()
        return results