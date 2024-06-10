from conn import connect

from models_northwind import OrderDetail

class OrderDao:    
    def __init__(self):
        self.connection = connect()

    def add_order(self, customer_id, employee_id, order_details):
        cursor = self.connection.cursor()
        lastid = cursor.execute("SELECT MAX(orderid) FROM northwind.orders")
        lastid = cursor.fetchone()[0]
        newid = lastid+1
        cursor.execute("INSERT INTO northwind.orders (orderid, customerid, employeeid, orderdate, requireddate, shippeddate, freight, shipname, shipaddress, shipcity, shipregion, shippostalcode, shipcountry, shipperid) VALUES (%s, %s, %s, now(), null, null, null, null, null, null, null, null, null, null) RETURNING orderid", (newid, customer_id, employee_id))
        
        for item in order_details:
            order_detail = OrderDetail()
            order_detail.productid = item['productid']
            order_detail.unitprice = item['unitprice']
            order_detail.quantity = item['quantity']
            order_detail.discount = item['discount']
            
            self.add_products(cursor, order_detail, newid)

        self.connection.commit()
        cursor.close()

    def add_products(self, cursor, product: OrderDetail, orderid):
        cursor.execute("INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity, discount) VALUES (%s, %s, %s, %s, %s)", (orderid, product.productid, product.unitprice, product.quantity, product.discount))

    def get_order(self, orderid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT o.orderid, o.orderdate, cust.contactname, e.firstname FROM northwind.orders o INNER JOIN northwind.customers cust ON cust.customerid = o.customerid INNER JOIN northwind.employees e ON e.employeeid = o.employeeid WHERE o.orderid = %s", (orderid,))
        return cursor.fetchone()

    def close(self):
        self.connection.close()

class Order_detailDao:
    def __init__(self):
        self.connection = connect()

    def add_products(self, product, orderid):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity, discount) VALUES (%s, %s, %s, %s, %s)", (orderid, product.productid, product.unitprice, product.quantity, product.discount))

    def get_order_detail(self, orderid):
        cursor = self.connection.cursor()
        cursor.execute("SELECT prod.productname, od.unitprice, od.quantity, od.discount FROM northwind.order_details od INNER JOIN northwind.orders o ON od.orderid = o.orderid INNER JOIN northwind.products prod ON od.productid = prod.productid WHERE o.orderid = %s", (orderid,))
        return cursor.fetchall()
    
class EmployeesDao:
    def __init__(self):
        self.connection = connect()
    
    def get_ranking(self, dateStart, dateEnd):
        cursor = self.connection.cursor()
        cursor.execute("SELECT e.firstname || ' ' || e.lastname AS employee_name, COUNT(o.orderid) AS total_orders, SUM(od.unitprice * od.quantity * (1 - od.discount)) AS total_sales FROM northwind.employees e JOIN northwind.orders o ON e.employeeid = o.employeeid JOIN northwind.order_details od ON o.orderid = od.orderid WHERE o.orderdate BETWEEN %s AND %s GROUP BY e.employeeid, e.firstname, e.lastname ORDER BY total_sales DESC", (dateStart, dateEnd))
        return cursor.fetchall()