from datetime import date
import csv
from fpdf import FPDF


def main():
    actions = ["Add a new expense", "Change monthly income/salary", "Check balance", "Print out a report", "Modify a recurrent expense", "Add extra income"]

    #The actions are as follows: 0 - add a new expense
    balance = get_balance()
    salary = get_salary()


    print("Menu:")
    for i in range(len(actions)):
        print(i+1, actions[i])

    while True:
        try:
            action = int(input("What would you like to do today? "))
        except ValueError:
            print("This is not a valid number")
            pass
        else:
            if not action - 1 in range(len(actions)):
                print("This is not a valid action. Please chose a number from the list")
                continue
            else:
                break

    # The following would've been much better...
    # to_do = {"Add a new expense" : add_expense() , "Change monthly income/salary" : change_salary(), "Check balance" : check_balance(), "Print out a report" : print_report(), "Modify a recurrent expense" : modify_expense(), "Add extra income" : add_income()}

    # to_do[actions[action - 1]] # apply/call corresponding function
    if actions[action - 1] == "Check balance":
        print(f"Your balance is ${balance}")

    elif actions[action - 1] == "Add a new expense":

        ans = input("Is this a recurrent expense (yes/no)? ").lower()
        while not check_yes_no(ans):
            ans = input("Please answer by yes or no: ")

        title = input("Title of expense: ")
        amount = input("Amount of expense: ")
        while not check_number_isvalid(amount):
            amount = input("Please enter a valid price: ")

        if ans == "yes" or ans == "y":
            dueday = input("Due day?: ")
            with open("monthlydata.csv", "a") as file:
                csv.DictWriter(file, fieldnames = ["title", "amount","dueday"]).writerow({"title" : title.title(), "amount" : amount, "dueday" : dueday})


        with open("budgeting.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames = ["date", "title", "amount"])
            writer.writerow({"date" : date.today(), "title" : title.title(), "amount" : amount})
            balance = float(balance) - float(amount)
        # Write back in file.

        with open("budgeting.csv", "r") as file:
            data = list(csv.DictReader(file, fieldnames = ["date", "title", "amount"]))
            data[0]["date"] = date.today()
            data[0]["amount"] = balance
        with open("budgeting.csv", "w") as file:
            csv.DictWriter(file, fieldnames=["date", "title", "amount"]).writerows(data)

    elif actions[action - 1] == "Change monthly income/salary":
        salary = input("New amount: ")
        dueday = input("Due day: ")

        while not check_day(dueday):
            dueday = input("Please enter a valid day of the month: ")


        with open("monthlydata.csv") as file:
            data = list(csv.DictReader(file, fieldnames = ["title", "amount", "dueday"]))
            data[0]["amount"] = salary
            data[0]["dueday"] = dueday
        with open("monthlydata.csv", "w") as file:
            csv.DictWriter(file, fieldnames=["title", "amount", "dueday"]).writerows(data)

    elif actions[action - 1] == "Print out a report":
        print_report("budgeting.csv")

    elif actions[action - 1] == "Modify a recurrent expense":
        with open("monthlydata.csv") as file:
            data = list(csv.DictReader(file, fieldnames = ["title", "amount", "dueday"]))

        for i in range(len(data)):
            print(i+1, data[i]["title"])

        while True:
            try:
                modify = int(input("Which expense would you like to modify? "))
            except ValueError:
                print("Please enter a valid number: ")
                pass
            else:
                while modify - 1 not in range(len(data)):
                    modify = int(input("Please chose a valid number "))
                break

        data[i-1]["title"] = input("New title: ").title()
        data[i-1]["amount"] = input("New amount: ")
        data[i-1]["dueday"] = input("New due day: ")

        with open("monthlydata.csv", "w") as file:
            csv.DictWriter(file, fieldnames = ["title", "amount", "dueday"]).writerows(data)
        ...













def get_balance():
    with open("budgeting.csv") as file:
        try:    # check if user info/balance exists
            balance = list(csv.reader(file))[0]
        except IndexError:

            balance = input("New user. Input balance: ") #get balance of new user
            while not check_number_isvalid(balance):
                balance = input("Please enter a valid number: ")

            with open("budgeting.csv", "a") as writeinfile:
                csv.DictWriter(writeinfile, fieldnames = ["date", "title", "amount"]).writerow({"date" : date.today(), "title" : "Balance", "amount" : balance})  #add it to file

            return balance

        else:
            return balance[2]


def check_number_isvalid(balance):
    try:
        float(balance)
    except ValueError:
        return False
    return True
#ADD FUNCTIONS: 1. CHECK AMOUNT ENTERED IS AN ACTUAL NUMBER.
#               2. WHEN ASKED NUMBERED QUESTIONS, CHECK NUMBER EXISTS.

def get_salary():
     with open("monthlydata.csv") as file:
        try:    # check if user info/salary exists
            salary = list(csv.reader(file))[0]
        except IndexError:

            salary = input("Input salary: ") #get salary of new user
            while not check_number_isvalid(salary):
                salary = input("Please enter a valid number: ")

            dueday = input("Deposited monthly on: ")

            while not check_day(dueday):
                dueday = input("Please enter a valid day of the month: ")


            with open("monthlydata.csv", "a") as writeinfile:
                csv.DictWriter(writeinfile, fieldnames = ["title", "amount", "dueday"]).writerow({"title" : "Salary", "amount" : salary, "dueday" : dueday})  #add it to file

            return salary

        else:
            return salary[1]




def print_report(filename):
    # no need to check anything because we know it's a valid csv file.
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', 'B', size = 20)
    pdf.text(80, 30, f"Your report as of {date.today()}")
    pdf.ln(40)

    pdf.set_font('helvetica', size = 14)
    pdf.set_fill_color(27, 155, 219)
    pdf.set_text_color(255)
    for heading in ["Date", "Title", "Amount"]:
        pdf.cell(40, 7, heading, 1, align="C", fill = True)
    pdf.ln()

    pdf.set_fill_color(224, 235, 255)
    pdf.set_text_color(0)
    fill = False
    with open(filename) as file:
        reader = csv.DictReader(file, fieldnames = ["date", "title", "amount"])

        for row in reader:
            pdf.cell(40, 6, row["date"],1, fill = fill)
            pdf.cell(40, 6, row["title"],1, fill = fill)
            pdf.cell(40, 6, f"${row['amount']}",1, fill = fill)
            pdf.ln()
            fill =  not fill

    pdf.output("BudgetReport.pdf")



def add_income():
    ...

def check_yes_no(ans):
    if ans not in ["yes", "y", "no", "n"]:
        return False
    else:
        return True


def check_day(dueday):
    if not dueday.isnumeric() or int(dueday) <1 or int(dueday) > 31:
        return False
    else:
        return True


if __name__ == "__main__":
    main()