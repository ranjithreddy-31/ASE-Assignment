from commonFunctions import *
from prettytable import PrettyTable
import pandas as pd


class wareHouse:

    def addItem(self):
        item_name = input("\nChoose 1 to add Tv's or choose 2 to add Stereo: ")
        if item_name not in ["1","2"]:
            print("Incorrect choices please choose again")
            self.addItem()
        ware_house_number = input("Choose 1 to add in warehouse 1 or choose 2 to add in warehouse 2: ")
        print()
        if item_name == '1' and ware_house_number == '1':
            confirmation = input(f"You are adding Tv's in warehouse {ware_house_number}. \nIf you are sure press 1 to "
                                 f"confirm or other key to choose again: ")
            if confirmation == '1':
                self.incrementItem(2)
            else:
                self.addItem()
        elif item_name == '2' and ware_house_number == '1':
            confirmation = input(
                f"You are adding Stereos in warehouse {ware_house_number}. \nIf you are sure press 1 to "
                f"confirm or other key to choose again: ")
            if confirmation == '1':
                self.incrementItem(1)
            else:
                self.addItem()
        elif item_name == '1' and ware_house_number == '2':
            confirmation = input(f"You are adding Tv's in warehouse {ware_house_number}. \nIf you are sure press 1 to "
                                 f"confirm or other key to choose again: ")
            if confirmation == '1':
                self.incrementItem(4)
            else:
                self.addItem()
        elif item_name == '2' and ware_house_number == '2':
            confirmation = input(
                f"You are adding Stereos in warehouse {ware_house_number}. \nIf you are sure press 1 to "
                f"confirm or other key to choose again: ")
            if confirmation == '1':
                self.incrementItem(3)
            else:
                self.addItem()
        else:
            print("Incorrect choices please choose again")
            self.addItem()
        self.wareHouse()

    def incrementItem(self, id):
        cols = [0, 1, 2, 3, 4, 5, 6, 7]

        excel = pd.read_csv('Products.csv', usecols=cols)
        try:
            quantity = int(input("Enter the number of items: "))
            excel.loc[id - 1, 'product_quantity'] += quantity
            # writing into the file
            excel.to_csv("Products.csv", index=False)
            print("Products added successfully")
        except Exception as e:
            print(e)

    def showItems(self):
        try:
            cols = [0, 1, 2, 3, 4, 5, 6, 7]
            excel = pd.read_csv('Products.csv', usecols=cols)
            x = PrettyTable()
            x.field_names = list(excel.columns)
            for i in range(4):
                x.add_row(list(excel.loc[i]))
            print(x)

        except Exception as e:
            print(e)
        self.wareHouse()

    def showItemsLessthanFive(self):
        try:
            cols = [0, 1, 2, 3, 4, 5, 6, 7]
            excel = pd.read_csv('Products.csv', usecols=cols)
            productQuantity = list(excel["product_quantity"])
            stereos = productQuantity[0] + productQuantity[2]
            tvs = productQuantity[1] + productQuantity[3]
            if stereos < 5 or tvs < 5:
                x = PrettyTable()
                x.field_names = ["Product_name", "Total_quantity"]
                if stereos < 5 and tvs < 5:
                    if stereos < tvs:
                        x.add_row(["Stereos", stereos])
                        x.add_row(["Tvs", tvs])
                    else:
                        x.add_row(["Tvs", tvs])
                        x.add_row(["Stereos", stereos])
                elif stereos < 5:
                    x.add_row(["Stereos", stereos])
                else:
                    x.add_row(["Tvs", tvs])
                print(x)
                print("")

            else:
                print("No items less than 5")
        except Exception as e:
            print(e)
        self.wareHouse()

    def wareHouse(self):
        print()
        print("Warehouse deails")
        print("1.Add item to inventory")
        print("2.Show quantity of each product by warehouse")
        print("3.Show products less than or equal to 5")
        # print("Press any other key to exit to main menu")
        print("Press any other key to exit")
        print()
        print()
        ware_house_input = input("Enter the number based on the operation that you want to perform: ")
        if ware_house_input == '1':
            self.addItem()
        elif ware_house_input == '2':
            self.showItems()
        elif ware_house_input == '3':
            self.showItemsLessthanFive()
        else:
            # c = commonFunctions()
            # c.displayMenu()
            print("Thank you")
            return exit


w = wareHouse()
w.wareHouse()
