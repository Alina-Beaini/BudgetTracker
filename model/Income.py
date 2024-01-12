# date incomedate
# string title

# bool recurrent

# float amount

# string currency
# string type

class Income:
    def __init__(self, id, title, amount, currency, incomedate, Type):
        self.id = id
        self.title = title
        self.__amount = amount
        self.currency = currency
        self.incomedate = incomedate
        self.Type = Type

    def get_amount(self) -> float:
        return self.__amount
    
