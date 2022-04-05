from datetime import datetime
import pandas as pd
from tabulate import tabulate

class SalesDetails:
    '''
        Class 'SalesDetails' handles different functionalities like:
            1. Generating a new Invoice
            2. Paying an Installment for an open Invoice
            3. Close an Open Invoice
            4. Show Open Invoices
            5. Shw Closed Invoices
    '''

    def __init__(self):
        # CSV Files required to store data related to different modules
        self.csv_files = {
            'Customers' : r'Customers.csv',
            'Invoices' : r'SalesDetails.csv',
            'Inventory' : r'Inventory.csv'
        }
    
    def getDataframe(self, file):
        '''
        This method returns a CSV file data in a DataFrame

        Parameters:
                file (str): The path of the CSV file
        Returns:
                DataFrame(file): The data of CSV file in DataFrame
        '''
        path = self.csv_files.get(file,None)
        if path:
            dataframe = pd.read_csv(path)
            return dataframe
        else:
            return pd.DataFrame()

    def joinDataframes(self, first,second):
        '''
        This method joins two Dataframes into one

        Parameters:
                first (DataFrame): First Dataframe
                second (DataFrame): Second DataFrame
        Returns:
                DataFrame(first,second): DataFrame formed by concatinating first and second
        '''
        if first.empty:
            return second
        if second.empty:
            return first
        updated_df = pd.concat([first, second], ignore_index=True)
        updated_df.reset_index(drop=True)
        return updated_df

    def generateInvoice(self, customer_id = 0, item_choice = 0, selling_price = 0, delivery_charges = 0):
        '''
        This method generates a new Invoice

        Parameters:
                customer_id (int): Customer ID
                item_choice (int): TV or Stereo
                selling_price (int): Selling price of the item
                delivery_charges (int): Delivery charges applicable to item
        Returns:
                Status(Bool): If the invoice is generated successfully, the data is saved to SalesDetails.csv and 'True' is returned. Incase of failure, this method returns False
        '''   
        # Handling invalid data cases
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
                # Fetch product details from inventey.csv
                inventory_df = self.getDataframe('Inventory')
                filtered_inventory_df = inventory_df[inventory_df['product_name'] == item_name]
                product_quantity = max(filtered_inventory_df['product_quantity'])
                product_warehouse = filtered_inventory_df[filtered_inventory_df['product_quantity'] == product_quantity].iloc[0]['product_warehouse']

                invoice_df = self.getDataframe('Invoices')
                if not invoice_df.empty:
                    max_id = max(invoice_df['Id'])+1
                else:
                    max_id = 1
                # Fetch and calculate all the required data for the new invoice
                filtered_customer_df = customers_df[customers_df['customerID'] == customer_id]
                name = filtered_customer_df.iloc[0]['name']
                zip = filtered_customer_df.iloc[0]['zip']
                tax_rate = filtered_customer_df.iloc[0]['taxRate']
                selling_price = selling_price
                delivery_charges = delivery_charges
                total_price = selling_price + delivery_charges + ((tax_rate / 100) * selling_price)
                balance = total_price
                date = datetime.today().strftime('%m-%d-%Y')
                # Create a dataframe with all the required data and values calculated above
                new_invoice = pd.DataFrame(
                    {
                        'Id' : [max_id],
                        'name' : [name],
                        'zip' : [zip],
                        'taxRate' : [tax_rate],
                        'itemName' : [item_name],
                        'sellingPrice': [selling_price],
                        'deliveryCharges': [delivery_charges],
                        'totalPrice' : [total_price],
                        'balance' : [balance],
                        'dateOfPurchase': [date],
                        'isClosed' : [0]
                    }
                )
                # Add new Invoice to the existing invoices and concatinate the data frames
                invoice_df.reset_index()
                new_invoice.reset_index()
                updated_invoice_data = self.joinDataframes(invoice_df, new_invoice)
                updated_invoice_data.to_csv(self.csv_files['Invoices'], encoding='utf-8', index=False)
                # Update the inventory by reducing the number of products of selected item
                updated_index = inventory_df.index[(inventory_df['product_name'] == item_name) & (inventory_df['product_warehouse'] == product_warehouse)].tolist()[0]
                inventory_df.at[updated_index,'product_quantity'] = product_quantity-1
                inventory_df.to_csv(self.csv_files['Inventory'], encoding='utf-8', index=False)
                print('Invoice has been generated successfully')
                return True
                
        except Exception as e:
            print(f'Invoice generating failed with exception: {e}.')
            return False

    def payInstallment(self, invoice_id, installment_amount):
        '''
        This method allows user to pay an installment for an open Invoice

        Parameters:
                invoice_id (int): Invoice ID
                installment_amount (int): Installment amount
        Returns:
                Status(Bool): If the installment is paid successfully, the data is saved to SalesDetails.csv and 'True' is returned. Incase of failure, this method returns False
        '''  
        invoice_id = invoice_id
        # Handling invalid data cases
        if not invoice_id or not installment_amount:
            return False
        if type(invoice_id) is not int or type(installment_amount) is not int:
            return False

        try:
            # check if invoice_id is valid
            invoice_df = self.getDataframe('Invoices')
            filtered_invoice_df = invoice_df[invoice_df['Id'] == invoice_id]
            if filtered_invoice_df.empty:
                print('Invalid Invoice ID :(, Please try again')
                return False
            
            # check if invoice is closed previously
            closed_invoices_df = filtered_invoice_df[filtered_invoice_df['isClosed'] == 0]
            if closed_invoices_df.empty:
                print('Invoice is closed !!')
                return True
            # Fetch and calculate all the details required to pay an installment
            total_price = closed_invoices_df.iloc[0]['totalPrice']
            balance = closed_invoices_df.iloc[0]['balance']
            date = closed_invoices_df.iloc[0]['dateOfPurchase']
            current_date = datetime.now()
            date = datetime.strptime(date, '%m/%d/%Y')
            days = (current_date - date).days

            # Calculate the balane based on the number of days since invoice is opened
            if days <= 10:
                # If number of days is less than or equal to 10, apply 10% discount
                print(f'Amount to be paid to close the invoice is: {0.9 * (total_price + balance - total_price)}')
                installment_amount = installment_amount
                balance = 0.9 * (total_price + balance - total_price) - installment_amount
            elif days > 30:
                # If number of days is greater than 30, apply 2% additional charge
                print(f'Amount to be paid is to close the invoice is: {1.02 * (total_price + balance -  total_price)}')
                installment_amount = installment_amount
                balance = 1.02 * (total_price + balance -  total_price) - installment_amount
            else:
                # Ifnumber of days is between 11 and 30, no additional charges or discounts are applied
                print(f'Amount to be paid is to close the invoice is: {(balance)}')
                installment_amount = installment_amount
                balance = balance - installment_amount

            if balance > 0:
                # if balnce is greater than 0, keep the invoice open
                updated_index = invoice_df.index[invoice_df['Id'] == invoice_id].tolist()[0]
                invoice_df.at[updated_index,'balance'] = balance
                invoice_df.to_csv(self.csv_files['Invoices'], encoding='utf-8', index=False)
                return True
            else:
                # if balnce is equal to 0, close the invoice
                self.closeInvoice(invoice_id)
                return True

        except Exception as e:
            print(f'Payment process failed with exeption:{e}')
            return False

    def closeInvoice(self,invoice_id=None):
        '''
        This method closes Invoice if the balance amount is paid

        Parameters:
                invoice_id (int): Invoice ID
        Returns:
                Status(Bool): If the invoice is closed successfully, the data is saved to SalesDetails.csv and 'True' is returned. Incase of failure, this method returns False
        '''  
        invoice_id = invoice_id
        # Handling invalid data cases
        if not invoice_id or type(invoice_id) is not int:
            print('Enter invoice ID t close an Invoice.')
            return False
        # Check if invoice_id is valid
        invoice_df = self.getDataframe('Invoices')
        mask = invoice_df['Id'] == invoice_id
        filtered_invoice_df = invoice_df[mask]
        if filtered_invoice_df.empty:
            print('Invalid Invoice ID :( Please try again')
            return False
        # If invoice_id is valid, close the invoice and change the balance to 0
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
        '''
        This method prints the open invoices in a tabular format

        Returns:
                Status(Bool): If the the open invoices are printed successfully, then 'True' is returned. Incase of failure, this method returns False
        '''  
        print('showing open invoices...')
        try:
            # Fetch open invoices and print them
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
        '''
        This method prints the closed invoices in a tabular format

        Returns:
                Status(Bool): If the the closed invoices are printed successfully, then 'True' is returned. Incase of failure, this method returns False
        ''' 
        print('showing closed invoices...')
        try:
            # Fetch closed invoices and print them
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
        print('6. Press any other key to exit')
        print()
        print()
        option = int(input('Select an option from the above menu: '))

        if option == 1:
            customer_id = int(input('Please enter customer ID: '))
            item_choice = int(input('Available items \n1. Tv\n2. Stereo\nSelect the item of your choice: '))
            selling_price = int(input('Enter selling price of the item: '))
            delivery_charges = int(input('Enter delivery charges if applicable. Else enter 0: '))
            self.generateInvoice(customer_id, item_choice, selling_price, delivery_charges)
        elif option == 2:
            invoice_id = int(input('Enter invoice Id: '))
            installment_amount = int(input('Enter installment amount: '))
            self.payInstallment(invoice_id, installment_amount)
        elif option == 3:
            self.showOpenInvoices()
        elif option == 4:
            self.showClosedInvoices()
        elif option == 5:
            invoice_id = int(input('Enter invoice Id: '))
            self.closeInvoice(invoice_id)
        return "exit"

    def salesDetails(self):
        print('\nWelcome to Sales and Invoices module.')
        self.salesdisplayMenu()

def main():
    '''
    main method to invoke SalesDetails object
    '''
    invoices = SalesDetails()
    invoices.salesDetails()

