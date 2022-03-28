class commonFunctions:
    def displayMenu(self):
        print("-----------Menu-----------")
        print("1.Warehouse")
        print("2.Salesperson Details")
        print("3.Sales and Invoices")
        print("4.Quit")
        print()
        print()
        workflowNumber = int(input("Enter the number to navigate: "))

        if workflowNumber == 1:
            from wareHouse import wareHouse
            wH = wareHouse()
            wH.wareHouse()
        elif workflowNumber == 2:
            from workersDetails import workerDetails
            w = workerDetails()
            w.workerDetails()
        elif workflowNumber == 3:
            from salesDetails import SalesDetails
            files = {
                'Customers': r'Customers.csv',
                'Invoices': r'SalesDetails.csv',
                'Inventory': r'Inventory.csv'
            }
            s = SalesDetails(files)
            s.salesdisplayMenu()
        elif workflowNumber == 4:
            return "exit"
        return "exit"
