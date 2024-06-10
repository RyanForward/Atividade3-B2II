from controller import add_order, generate_report, get_employee_ranking

def main_menu():
    while True:
        print("1. Criar Pedido")
        print("2. Gerar relatorio sobre um pedido")
        print("3. Gerar relatorio sobre ranking dos funcionarios")
        choice = int(input("Escolha uma opção: "))

        if choice == 1:
            customer_id = input("Insira o ID do cliente: ")
            employee_id = input("Insira o ID do funcionario: ")
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
            
            add_order(customer_id, employee_id, order_details)
            print("Pedido criado com sucesso!")
            print('\n')
        
        elif choice == 2:
            order_id = int(input("Insira o ID do pedido: "))
            report = generate_report(order_id)
            # Imprimir o relatório formatado conforme solicitado
            print(f"\nID do pedido: {report['order_id']}")
            print(f"Data do pedido: {report['order_date']}")
            print(f"Nome do cliente: {report['customer_name']}")
            print(f"Nome do funcionario: {report['employee_name']}")
            print('\n---------- PRODUTOS ------------\n')
            for detail in report['order_details']:
                print(f"Nome do produto: {detail['product_name']} \nQuantidade: {detail['quantity']} \nPreço unitário: {detail['unit_price']}")
                print('\n-----------------------\n')
            
            print('\n')
        
        elif choice == 3:
            start_date = input("Insira a data de inicio (YYYY-MM-DD): ")
            end_date = input("Insira a data final (YYYY-MM-DD): ")
            ranking = get_employee_ranking(start_date, end_date)
            position = 1
            for employee in ranking:
                print(f"\nPosição: {position}º Lugar")
                print(f"Nome do funcionário: {employee['employee_name']}")
                print(f"Total de pedidos: {employee['total_orders']}")
                print(f"Valor total vendido: {employee['total_sales']}")
                print('------------------------------------------------')
                position+=1
            print('\n')
        else:
            print("Escolha inválida")


if __name__ == '__main__':
    main_menu()