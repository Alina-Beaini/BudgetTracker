import csv
from datetime import date

class User:
    def __init__(self, id):
        self.id = id
        self.balance = 0
        self.incomes = []
        
    def create(self):
        print(f"User with id {self.id} was created")
        return self
            
    def set_balance(self, new_balance):
        if self.balance == 0:
            self.balance =  new_balance
            
            with open("budgeting.csv", "a") as writeinfile:
                csv.DictWriter(writeinfile, fieldnames = ["date", "title", "amount"]).writerow({"date" : date.today(), "title" : "Balance", "amount" : self.balance})  #add it to file
            
            print(f"Balance of {new_balance} was added")
        else:
            print("User already has a balance")
        return self
    
    def get_balance(self):
        return self.balance
    
    def get_salary(self):
        return self.balance
    
    def add_income(self, income):
        self.incomes.append(income)
        return self.incomes
    


    
        
