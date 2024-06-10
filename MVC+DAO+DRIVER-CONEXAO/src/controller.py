from model import add_orderModel, generate_reportModel, get_ranking

def add_order(customer_id, employee_id, order_details):
    add_orderModel(customer_id, employee_id, order_details)

def generate_report(orderId):
    return generate_reportModel(orderId)

def get_employee_ranking(startDate, endDate):
    return get_ranking(startDate, endDate)

