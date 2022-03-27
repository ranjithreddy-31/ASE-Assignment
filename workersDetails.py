from commonFunctions import commonFunctions
import pandas as pd
from prettytable import PrettyTable


class workerDetails:
    def showWorkerDetails(self):
        cols = [0, 1, 2, 3, 4]
        try:
            excel = pd.read_csv('workersDetails.csv', usecols=cols)
            x = PrettyTable()
            x.field_names = list(excel.columns)
            for i in range(len(excel.index)):
                x.add_row(list(excel.loc[i]))
            print(x)

        except Exception as e:
            print(e)
        self.workerDetails()

    def checkUserExists(self, id):
        try:
            cols = [0, 1, 2, 3, 4]
            excel = pd.read_csv('workersDetails.csv', usecols=cols)
            results = list(excel["person_id"])
            if id in results:
                return True
            return False
        except Exception as e:
            print(e)

    def updateCommission(self):
        userId = input("Choose person id whose commission percentage need to be updated: ")
        if self.checkUserExists(int(userId)):
            newPercentage = input("Enter the new commission percentage: ")
            try:
                cols = [0, 1, 2, 3, 4]
                excel = pd.read_csv('workersDetails.csv', usecols=cols)
                excel.loc[int(userId) - 1, 'commission'] = float(newPercentage)
                # writing into the file
                excel.to_csv("workersDetails.csv", index=False)
                print("Successfully updated new percentage")

            except Exception as e:
                print(e)
            self.workerDetails()
        else:
            print("User with that particular id doesn't exist.\n")
            userInput = input("Press 1 to enter the userId again or any other key to go back: ")
            if userInput == '1':
                self.updateCommission()
            else:
                self.workerDetails()

    def workerDetails(self):
        print()
        print()
        print("Salespersons deails")
        print("1.Show workers details")
        print("2.Update commission percentage")
        print("Press any other key to exit to main menu")
        print()
        print()
        ware_house_input = input("Enter the number based on the operation that you want to perform: ")
        if ware_house_input == '1':
            self.showWorkerDetails()
        elif ware_house_input == '2':
            self.updateCommission()
        else:
            # c = commonFunctions()
            # c.displayMenu()
            print("Thank you")
            return exit


wD = workerDetails()
wD.workerDetails()
