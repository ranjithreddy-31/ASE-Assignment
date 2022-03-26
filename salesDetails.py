from datetime import datetime
import pandas as pd
from commonFunctions import *
from tabulate import tabulate

class SalesDetails:
    def __init__(self, files):
        self.csv_files = files

    def getDataframe(self, file):
        path = self.csv_files.get(file,None)
        dataframe = pd.read_csv(path)
        return dataframe
    
    def getConnection(self):
        return None
        


    def generateInvoice(self, customer_id = 0, item_choice = 0, selling_price = 0, delivery_charges = 0):
        if type(customer_id) is not int or type(item_choice) is not int or type(selling_price) is not int:
            print('Invalid types of data')
            return False
            
        customer_id = customer_id

        try:
            customers_df = self.getDataframe('Customers')
            if customers_df[customers_df['customerID'] == customer_id].empty:
                print('Customer has not registered yet. Please register before generating an invoice')
                return False
            else:
                item_choice = item_choice
                if item_choice == 1:
                    item_name = 'Tv' 
                elif item_choice == 2:
                    item_name = 'Stereos'
                else:
                    print('Choose a valid option')
                    return False
                inventory_df = self.getDataframe('Inventory')
                filtered_inventory_df = inventory_df[inventory_df['product_name'] == item_name]
                product_quantity = max(filtered_inventory_df['product_quantity'])
                product_warehouse = filtered_inventory_df[filtered_inventory_df['product_quantity'] == product_quantity].iloc[0]['product_warehouse']

                invoice_df = self.getDataframe('Invoices')
                if not invoice_df.empty:
                    max_id = max(invoice_df['Id'])+1
                else:
                    max_id = 1
                filtered_customer_df = customers_df[customers_df['customerID'] == customer_id]
                name = filtered_customer_df.iloc[0]['name']
                zip = filtered_customer_df.iloc[0]['zip']
                tax_rate = filtered_customer_df.iloc[0]['taxRate']
                selling_price = selling_price
                delivery_charges = delivery_charges
                total_price = selling_price + delivery_charges + ((tax_rate / 100) * selling_price)
                balance = total_price
                date = datetime.today().strftime('%m-%d-%Y')
                new_invoice = pd.DataFrame(
                    {
                        'Id' : [max_id],
                        'name' : [name],
                        'zip' : [zip],
                        'taxRate' : [tax_rate],
                        'itemName' : [item_name],
                        'sellingPrice': [selling_price],
                        'deliveryCharges': [delivery_charges],
                        'total_price' : [total_price],
                        'balance' : [balance],
                        'dateOfPurchase': [date],
                        'isClosed' : [0]
                    }
                )
                invoice_df.reset_index()
                new_invoice.reset_index()
                updated_invoice_data = pd.concat([invoice_df, new_invoice])
                updated_invoice_data.reset_index()
                updated_invoice_data.to_csv(self.csv_files['Invoices'], encoding='utf-8', index=False)
                
                updated_index = inventory_df.index[(inventory_df['product_name'] == item_name) & (inventory_df['product_warehouse'] == product_warehouse)].tolist()[0]
                inventory_df.at[updated_index,'product_quantity'] = product_quantity-1
                inventory_df.to_csv(self.csv_files['Inventory'], encoding='utf-8', index=False)
                print('Invoice has been generated successfully')
                return True
        except Exception as e:
            print(f'Invoice generating failed with exception: {e}.')
            return False


    def payInstallment(self, invoice_id, installment_amount):
        invoice_id = invoice_id

        try:
            invoice_df = self.getDataframe('Invoices')
            filtered_invoice_df = invoice_df[invoice_df['Id'] == invoice_id]
            if filtered_invoice_df.empty:
                print('Invalid Invoice ID :(, Please try again')
                return False
            
            closed_invoices_df = filtered_invoice_df[filtered_invoice_df['isClosed'] == 0]
            if closed_invoices_df.empty:
                print('Invoice is closed !!')
                return True
            total_price = closed_invoices_df.iloc[0]['totalPrice']
            balance = closed_invoices_df.iloc[0]['balance']
            date = closed_invoices_df.iloc[0]['dateOfPurchase']
            current_date = datetime.now()
            date = datetime.strptime(date, '%m-%d-%Y')
            days = (current_date - date).days

            print(total_price, balance, date, current_date, days)
            if days <= 10:
                print(f'Amount to be paid to close the invoice is: {0.9 * (total_price + balance - total_price)}')
                installment_amount = installment_amount
                balance = 0.9 * (total_price + balance - total_price) - installment_amount
            elif days > 30:
                print(f'Amount to be paid is to close the invoice is: {1.02 * (total_price + balance -  total_price)}')
                installment_amount = installment_amount
                balance = 1.02 * (total_price + balance -  total_price) - installment_amount
            else:
                print(f'Amount to be paid is to close the invoice is: {(balance)}')
                installment_amount = installment_amount
                balance = balance - installment_amount
            if balance > 0:
                updated_index = invoice_df.index[invoice_df['Id'] == invoice_id].tolist()[0]
                invoice_df.at[updated_index,'balance'] = balance
                invoice_df.to_csv(self.csv_files['Invoices'], encoding='utf-8', index=False)
                return True
            else:
                self.closeInvoice(invoice_id)
                return True
        except Exception as e:
            print(f'Payment process failed with exeption:{e}')
            return False


    def closeInvoice(self,invoice_id=None):
        invoice_id = invoice_id
        if not invoice_id:
            print('Enter invoice ID t close an Invoice.')
            return False
        invoice_df = self.getDataframe('Invoices')
        mask = invoice_df['Id'] == invoice_id
        mask &= invoice_df['isClosed'] == 0
        filtered_invoice_df = invoice_df[mask]
        if filtered_invoice_df.empty:
            print('Invalid Invoice ID :( Please try again')
            return False
        updated_index = invoice_df.index[mask].tolist()[0]
        try:
            invoice_df.at[updated_index,'isClosed'] = 1
            invoice_df.at[updated_index,'balance'] = 0
            invoice_df.to_csv(self.csv_files['Invoices'], encoding='utf-8', index=False)
            print(f'Invoice: {invoice_id} has been closed successfully!!')
            return True
        except Exception as e:
            print(f'Failed closing invoice with exception: {e}')
            return False

    def showOpenInvoices(self):
        print('showing open invoices...')
        try:
            invoice_df = self.getDataframe('Invoices')
            mask = invoice_df['isClosed'] == 0
            open_invoice_df = invoice_df[mask]
            open_invoice_df.sort_values('dateOfPurchase')
            print(tabulate(open_invoice_df, headers='keys', tablefmt='psql'))
            return True
        except Exception as e:
            print(f'Failed fetching open invoices with exception: {e}')
            return False

    def showClosedInvoices(self):
        print('showing closed invoices...')
        try:
            invoice_df = self.getDataframe('Invoices')
            mask = invoice_df['isClosed'] == 1
            closed_invoice_df = invoice_df[mask]
            closed_invoice_df.sort_values('totalPrice')
            print(tabulate(closed_invoice_df, headers='keys', tablefmt='psql'))
            return True
        except Exception as e:
            print(f'Failed fetching closed invoices with exception: {e}')
            return False


    def salesdisplayMenu(self):
        print()
        print()
        print('1. Generate an invoice')
        print('2. Pay an installment')
        print('3. Show open invoices')
        print('4. Show closed invoices')
        print('5. Manually close an Invoice')
        print('6. Press any other key to exit to main menu')
        print()
        print()
        option = int(input('Select an option from the above menu: '))

        if option == 1:
            # customer_id = int(input('Please enter customer ID: '))
            # item_choice = int(input('Available items \n1. Tv\n2. Stereo\nSelect the item of your choice: '))
            # selling_price = int(input('Enter selling price of the item: '))
            # delivery_charges = int(input('Enter delivery charges if applicable. Else enter 0: '))
            self.generateInvoice(1, 2, 1, 1)
        elif option == 2:
            #invoice_id = int(input('Enter invoice Id: '))
            #installment_amount = int(input('Enter installment amount: '))
            self.payInstallment(1, 0)
        elif option == 3:
            self.showOpenInvoices()
        elif option == 4:
            print(self.showClosedInvoices())
        elif option == 5:
            #invoice_id = int(input('Enter invoice Id: '))
            print(self.closeInvoice(1))
        else:
            c = commonFunctions()
            c.displayMenu()


    def salesDetails(self):
        print('\nWelcome to Sales and Invoices module.')
        self.salesdisplayMenu()

# files = {
#             'Customers' : r'Customers.csv',
#             'Invoices' : r'SalesDetails.csv',
#             'Inventory' : r'Inventory.csv'
#         }
# s = SalesDetails(files)
# s.salesdisplayMenu()



