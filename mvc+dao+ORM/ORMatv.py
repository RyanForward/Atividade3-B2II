from sqlalchemy import create_engine, Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, func, desc, select, Sequence
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from datetime import datetime

Base = declarative_base(metadata=MetaData(schema='northwind'))

# Definição das classes de modelo
class Category(Base):
    __tablename__ = 'categories'

    categoryid = Column(Integer, primary_key=True)
    categoryname = Column(String(50))
    description = Column(String(100))

class Customer(Base):
    __tablename__ = 'customers'

    customerid = Column(String(5), primary_key=True)
    companyname = Column(String(50))
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(15))
    postalcode = Column(String(9))
    country = Column(String(15))
    phone = Column(String(17))
    fax = Column(String(17))

class Employee(Base):
    __tablename__ = 'employees'

    employeeid = Column(Integer, primary_key=True)
    lastname = Column(String(20))
    firstname = Column(String(10))
    title = Column(String(25))
    titleofcourtesy = Column(String(8))
    birthdate = Column(DateTime)
    hiredate = Column(DateTime)
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(2))
    postalcode = Column(String(9))
    country = Column(String(15))
    homephone = Column(String(14))
    extension = Column(String(4))
    reportsto = Column(Integer)
    notes = Column(Text)

class Product(Base):
    __tablename__ = 'products'

    productid = Column(Integer, primary_key=True)
    productname = Column(String(35))
    supplierid = Column(Integer, nullable=False)
    categoryid = Column(Integer, ForeignKey('categories.categoryid'), nullable=False)
    quantityperunit = Column(String(20))
    unitprice = Column(Numeric(13, 4))
    unitsinstock = Column(SmallInteger)
    unitsonorder = Column(SmallInteger)
    reorderlevel = Column(SmallInteger)
    discontinued = Column(String(1))

class Shipper(Base):
    __tablename__ = 'shippers'

    shipperid = Column(Integer, primary_key=True)
    companyname = Column(String(20))
    phone = Column(String(14))

class Supplier(Base):
    __tablename__ = 'suppliers'

    supplierid = Column(Integer, primary_key=True)
    companyname = Column(String(50))
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(15))
    postalcode = Column(String(8))
    country = Column(String(15))
    phone = Column(String(15))
    fax = Column(String(15))
    homepage = Column(String(100))

class Order(Base):
    __tablename__ = 'orders'

    orderid = Column(Integer, primary_key=True, autoincrement=True)
    customerid = Column(ForeignKey('customers.customerid', ondelete='RESTRICT', onupdate='CASCADE', name='orders_customerid_fkey'), nullable=False)
    employeeid = Column(ForeignKey('employees.employeeid', ondelete='RESTRICT', onupdate='CASCADE', name='employee_id'), nullable=False)
    orderdate = Column(DateTime)
    requireddate = Column(DateTime)
    shippeddate = Column(DateTime)
    freight = Column(Numeric(15, 4))
    shipname = Column(String(35))
    shipaddress = Column(String(50))
    shipcity = Column(String(15))
    shipregion = Column(String(15))
    shippostalcode = Column(String(9))
    shipcountry = Column(String(15))
    shipperid = Column(ForeignKey('shippers.shipperid'))

    customer = relationship('Customer')
    employee = relationship('Employee')

class OrderDetail(Base):
    __tablename__ = 'order_details'

    orderid = Column(ForeignKey('orders.orderid', ondelete='RESTRICT', onupdate='CASCADE', name='order_details_orderid_fkey'), primary_key=True, nullable=False)
    productid = Column(ForeignKey('products.productid', ondelete='RESTRICT', onupdate='CASCADE', name='order_details_productid_fkey'), primary_key=True, nullable=False)
    unitprice = Column(Numeric(13, 4))
    quantity = Column(SmallInteger)
    discount = Column(Numeric(10, 4))

    order = relationship('Order')
    product = relationship('Product')

# Configuração da conexão com banco
DATABASE_URL = 'postgresql+psycopg2://postgres:123@localhost:5432/northwind'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# DAOs
class CategoryDAO:
    def __init__(self, session):
        self.session = session

    def create(self, category):
        self.session.add(category)
        self.session.commit()

class OrderDAO:
    def __init__(self, session):
        self.session = session

    def create(self, order):
        self.session.add(order)
        self.session.commit()

    def get_order_details(self, order_id):
        order = self.session.query(Order).filter(Order.orderid == order_id).first()
        order_details = self.session.query(OrderDetail).filter(OrderDetail.orderid == order_id).all()
        return order, order_details

    def get_employee_ranking(self, start_date, end_date):
        result = self.session.query(
            Employee.firstname, Employee.lastname, 
            func.count(Order.orderid).label('total_orders'), 
            func.sum(OrderDetail.unitprice * OrderDetail.quantity).label('total_sales')
        ).join(Order, Employee.employeeid == Order.employeeid
        ).join(OrderDetail, Order.orderid == OrderDetail.orderid
        ).filter(Order.orderdate.between(start_date, end_date)
        ).group_by(Employee.employeeid, Employee.firstname, Employee.lastname
        ).order_by(desc('total_sales')).all()
        return result

class OrderDetailDAO:
    def __init__(self, session):
        self.session = session

    def create(self, order_detail):
        self.session.add(order_detail)
        self.session.commit()

# Funções de verificação
def customer_exists(session, customer_id):
    return session.query(Customer).filter_by(customerid=customer_id).first() is not None

def employee_exists(session, employee_id):
    return session.query(Employee).filter_by(employeeid=employee_id).first() is not None

def shipper_exists(session, shipper_id):
    return session.query(Shipper).filter_by(shipperid=shipper_id).first() is not None

# Controlador
class OrderController:
    def __init__(self, order_dao, order_detail_dao, session):
        self.order_dao = order_dao
        self.order_detail_dao = order_detail_dao
        self.session = session

    def create_order(self, customer_id, employee_id, shipper_id, order_details):
        if not customer_exists(self.session, customer_id):
            print(f"Customer ID {customer_id} does not exist.")
            return
        if not employee_exists(self.session, employee_id):
            print(f"Employee ID {employee_id} does not exist.")
            return
        if not shipper_exists(self.session, shipper_id):
            print(f"Shipper ID {shipper_id} does not exist.")
            return

        order = Order(
            customerid=customer_id,
            employeeid=employee_id,
            shipperid=shipper_id,
            orderdate=datetime.now()
        )
        self.order_dao.create(order)

        for detail in order_details:
            order_detail = OrderDetail(
                orderid=order.orderid,
                productid=detail['productid'],
                unitprice=detail['unitprice'],
                quantity=detail['quantity'],
                discount=detail['discount']
            )
            self.order_detail_dao.create(order_detail)

    def generate_order_report(self, order_id):
        order, order_details = self.order_dao.get_order_details(order_id)
        report = {
            'order_id': order.orderid,
            'order_date': order.orderdate,
            'customer_name': order.customer.companyname,
            'employee_name': f"{order.employee.firstname} {order.employee.lastname}",
            'order_details': [
                {
                    'product_name': detail.product.productname,
                    'quantity': detail.quantity,
                    'unit_price': detail.unitprice
                } for detail in order_details
            ]
        }
        return report
    
    def generate_employee_ranking(self, start_date, end_date):
        ranking = self.order_dao.get_employee_ranking(start_date, end_date)
        formatted_ranking = [
            {
                'employee_name': f"{employee.firstname} {employee.lastname}",
                'total_orders': employee.total_orders,
                'total_sales': employee.total_sales

            } 
            for employee in ranking
        
        ]
        return formatted_ranking
    
# Função principal
def main():
    session = Session()

    # Inicialização dos DAOs
    order_dao = OrderDAO(session)
    order_detail_dao = OrderDetailDAO(session)

    # Criação do controlador
    controller = OrderController(order_dao, order_detail_dao, session)

    # Interface do usuário
    print("1. Criar Pedido")
    print("2. Gerar relatorio sobre um pedido")
    print("3. Gerar relatorio sobre ranking dos funcionarios")
    choice = int(input("Escolha uma opção: "))

    if choice == 1:
        customer_id = input("Insira o ID do cliente: ")
        employee_id = input("Insira o ID do funcionario: ")
        shipper_id = input("Insira o ID do shipper: ")
        order_details = []
        
        while True:
            product_id = input("Insira o ID do produto ou digite fim para encerrar: ")
            if product_id == 'fim':
                break
            unit_price = float(input("Insira o preço unitário: "))
            quantity = int(input("Insira a quantidade do produto: "))
            discount = float(input("Insira o desconto dado sob o produto: "))
            
            order_details.append({
                'productid': product_id,
                'unitprice': unit_price,
                'quantity': quantity,
                'discount': discount
            })
        
        controller.create_order(customer_id, employee_id, shipper_id, order_details)
        print("Pedido criado com sucesso!")
    
    elif choice == 2:
        order_id = int(input("Insira o ID do pedido: "))
        report = controller.generate_order_report(order_id)
        # Imprimir o relatório A
        print(f"\n ID do pedido: {report['order_id']}")
        print(f"Data do pedido: {report['order_date']}")
        print(f"Nome do cliente: {report['customer_name']}")
        print(f"Nome do funcionario: {report['employee_name']}")
        for detail in report['order_details']:
            print(f"Nome do produto: {detail['product_name']} \nQuantidade: {detail['quantity']} \nPreço unitário: {detail['unit_price']}")
    
    elif choice == 3:
        # Imprimir o relatório B
        start_date = input("Insira a data de inicio (YYYY-MM-DD): ")
        end_date = input("Insira a data final (YYYY-MM-DD): ")
        ranking = controller.generate_employee_ranking(start_date, end_date)
        print(ranking)
    
    else:
        print("Escolha inválida")

if __name__ == '__main__':
    main()