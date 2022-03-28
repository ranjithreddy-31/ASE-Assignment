from workersDetails import *
from wareHouse import *

import re
import pandas as pd

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class ownerLogin:
    def getPassword(self, password):
        cols = [0, 1, 2]

        excel = pd.read_csv('OwnerInfo.csv', usecols=cols)
        try:
            result = list(excel["Password"])
            if result[0] == password:
                return "Success"
            else:
                return "Incorrect"

        except Exception as e:
            print(e)

    def getEmail(self, email):
        cols = [0, 1, 2]

        excel = pd.read_csv('OwnerInfo.csv', usecols=cols)
        try:
            result = list(excel["Email"])
            if result[0] == email:
                return "Success"
            else:
                return "Incorrect"

        except Exception as e:
            print(e)

    def updatePassword(self, newPassword):
        cols = [0, 1, 2]

        excel = pd.read_csv('OwnerInfo.csv', usecols=cols)
        try:
            excel.loc[0, 'Password'] = newPassword
            # writing into the file
            excel.to_csv("OwnerInfo.csv", index=False)
        except Exception as e:
            print(e)
        print("\n")
        self.startProgram()

    def isValid(self, email):
        if re.fullmatch(regex, email):
            return True
        else:
            print("Invalid email format!!!")
            return False

    def resetPassword(self):
        enter_registered_email = input("Enter your registered email: ")
        if self.isValid(enter_registered_email):
            if self.getEmail(enter_registered_email) == "Success":
                while True:
                    new_password = input("Enter the new password: ")
                    confirm_password = input("Reenter to confirm password: ")
                    if new_password == confirm_password:
                        self.updatePassword(new_password)
                        break
                    else:
                        print("Passwords didn't match\n")
            else:
                print("Email is not correct")
                trychoice = input("\nDo you want to try again?"
                                  " Press 1 to retry or"
                                  " Press any other other key to quit: ")
                if trychoice == '1':
                    self.resetPassword()
                else:
                    print("\nBye Bye! See you later")
        else:
            trychoice = input("\nDo you want to try again?"
                              " Press 1 to retry or"
                              " Press any other other key to quit: ")
            if trychoice == '1':
                self.resetPassword()
            else:
                print("\nThank you")

    def displayMenu(self):
        print("-----------Menu-----------")
        print("1.Warehouse")
        print("2.Salesperson Details")
        print("3.Sales and Invoices")
        print("4.User Registration")
        print("5.Quit")
        print()
        print()
        workflowNumber = int(input("Enter the number to navigate: "))

        if workflowNumber == 1:
            w = wareHouse()
            w.wareHouse()
        elif workflowNumber == 2:
            wD = workerDetails()
            wD.workerDetails()
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

    def startProgram(self):
        password = input("                   Welcome! \n"
                         "Enter your password to continue or Press 1 to quit: ")

        if password == '1':
            print("Thank you")
        else:
            while True:
                passwordStatus = self.getPassword(password)
                if passwordStatus == "Success":
                    # menuStatus = self.displayMenu()
                    # if menuStatus == "exit":
                    #     print("Thank you!")
                    print("Thank you!")
                elif passwordStatus == "Incorrect":
                    print("Incorrect password")
                    reEnter = input("\nPress 1 to reenter or Press 2 to reset or "
                                    " Press any other other key to quit: ")
                    if reEnter.lower() == "1":
                        password = input("\nReenter your password: ")
                        continue
                    elif reEnter.lower() == "2":
                        self.resetPassword()
                    else:
                        print("Try again later by entering the correct password!")
                break


s = ownerLogin()
s.startProgram()
