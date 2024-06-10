from dao import OrderDao, Order_detailDao, EmployeesDao
from models_northwind import Order, OrderDetail

def add_orderModel(customer_id, employee_id, order_details):
    newOrderDAO = OrderDao()
    newOrderDAO.add_order(customer_id, employee_id, order_details)
    return True

def generate_reportModel(orderId):
    newOrderDAO = OrderDao()
    order_report = newOrderDAO.get_order(orderId)
    newOrderDetailDAO = Order_detailDao()
    detail_report = newOrderDetailDAO.get_order_detail(orderId)

    report = {
        'order_id': order_report[0],
        'order_date': order_report[1],
        'customer_name': order_report[2],
        'employee_name': order_report[3],
        'order_details': [
            {
                'product_name': detail[0],
                'quantity': detail[1],
                'unit_price': detail[2]
            } for detail in detail_report
        ]
    }

    return report

def get_ranking(startDate, endDate):
    newEmployeesDAO = EmployeesDao()
    ranking = newEmployeesDAO.get_ranking(startDate, endDate)
    formatted_ranking = [
                {
                    'employee_name': f"{employee[0]}",
                    'total_orders': employee[1],
                    'total_sales': employee[2]

                } 
                for employee in ranking
            
            ]
    return formatted_ranking

