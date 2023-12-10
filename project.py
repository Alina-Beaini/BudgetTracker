from datetime import date, timedelta, datetime
import csv
from fpdf import FPDF


def main():

    actions = ["Add a new expense", "Change monthly income/salary", "Check balance", "Print out a report"]

    #The actions are as follows: 0 - add a new expense ...

    balance = float(get_balance())
    salary = float(get_salary())
    
    # First, check if new user --if not compute with all recurrent expenses till day.

    if not check_new_user():
        #want to (1) compute all recurrent expenses, (2) add them to list, and (3) remove from balance. 
        print("Welcome Back!")

        #Note: Last date == date under "balance" so far
        with open("budgeting.csv") as file:
            last_date_used = list(csv.reader(file))[0][0] #This is a sting with the date of last use
    
        today_date = datetime.today().date()
        start = datetime.strptime(last_date_used, "%Y-%m-%d").date()
        end = today_date
        # difference between current and previous date
        delta = timedelta(days=1)

        # store the DAYS of dates between lastdate and todaysdate in a list
        dates = []
        while start <= end:
            dates.append(start.day)
             # increment start date by timedelta
            start += delta

        with open("monthlydata.csv") as file:
            #want to iterate over stuff in monthly data // salary always 1st (to be added to balance) and all else to be subtracted
            rowsofdata = list(csv.DictReader(file, fieldnames= ["title", "amount", "duedate"]))
            
            for row in rowsofdata:
                for d in dates[1:]:
                    if int(row["duedate"]) == int(d):
                        if row["title"] == "Salary":
                            balance += float(row["amount"])
                        else:
                            balance -= float(row["amount"])
                        with open("budgeting.csv", "r") as file:
                            data = list(csv.DictReader(file, fieldnames = ["date", "title", "amount"]))
                            data[0]["date"] = date.today()
                            data[0]["amount"] = balance
                            data.append({"date": date.today(), "title": row["title"], "amount": row["amount"]}) #need to change date added. 
                        with open("budgeting.csv", "w") as file:
                            csv.DictWriter(file, fieldnames=["date", "title", "amount"]).writerows(data)

     
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
                print("This is not a valid action. Please chose a number from the list above.")
                continue
            else:
                break

    # to_do[actions[action - 1]] # apply/call corresponding function
    if actions[action - 1] == "Check balance":
        print(f"Your balance is ${get_balance()}") #using get_balance() instead of balance: for future use, other actions might have taken place. 

    elif actions[action - 1] == "Add a new expense":

        ans = input("Is this a recurrent expense (yes/no)? ").lower()
        while not check_yes_no(ans):
            ans = input("Please answer by yes or no: ")

        title = input("Title of expense: ")
        amount = input("Amount of expense: ")
        while not check_number_isvalid(amount):
            amount = input("Please enter a valid amount: ")

        if ans == "yes" or ans == "y":
            dueday = input("Monthly due day? ")
            with open("monthlydata.csv", "a") as file:
                csv.DictWriter(file, fieldnames = ["title", "amount","dueday"]).writerow({"title" : title.title(), "amount" : amount, "dueday" : dueday})

        #only subtract if duedate today or NOT recurrent
        
        if ((ans == "yes" or ans == "y") and int(dueday) == today_date.day) or (ans == "no" or ans == "n"):
            with open("budgeting.csv", "a") as file:
                writer = csv.DictWriter(file, fieldnames = ["date", "title", "amount"])
                writer.writerow({"date" : date.today(), "title" : title.title(), "amount" : amount})
                balance = float(balance) - float(amount)
                
            # Write back in file
            with open("budgeting.csv", "r") as file:
                data = list(csv.DictReader(file, fieldnames = ["date", "title", "amount"]))
                data[0]["date"] = date.today()
                data[0]["amount"] = balance
            with open("budgeting.csv", "w") as file:
                csv.DictWriter(file, fieldnames=["date", "title", "amount"]).writerows(data)

        print(f"Your new balance is now {balance}")

    elif actions[action - 1] == "Change monthly income/salary":
        salary = input("New amount: ")

        while not check_number_isvalid(salary):
            salary = input("Please enter a valid amount: ")


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


def check_new_user():
    with open("budgeting.csv") as file:
        try:    # check if user info/balance exists
            balance = list(csv.reader(file))[0]
        except IndexError:
            return True
        return False

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


def check_number_isvalid(amt):
    try:
        float(amt)
    except ValueError:
        return False
    if float(amt) <= 0:
        return False
    return True


def get_salary():
     with open("monthlydata.csv") as file:
        try:    # check if user info/salary exists
            salary = list(csv.reader(file))[0]
        except IndexError:

            salary = input("No salary yet. Input salary: ") #get salary of new user
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
    pdf.text(60, 30, f"Your report as of {date.today()}")
    pdf.ln(40)

    pdf.set_font('helvetica', size = 14)
    pdf.set_fill_color(27, 155, 219)
    pdf.set_text_color(255)
    for heading in ["Date", "Title", "Amount"]:
        pdf.cell(60,8.5, heading, 1, align="C", fill = True)
    pdf.ln()

    pdf.set_fill_color(224, 235, 255)
    pdf.set_text_color(0)
    fill = False
    with open(filename) as file:
        reader = csv.DictReader(file, fieldnames = ["date", "title", "amount"])

        for row in reader:
            if row["title"] == "Salary":
                pdf.cell(60, 6, row["date"],1, align="C", fill = fill)
                pdf.cell(60, 6, row["title"],1, align="C", fill = fill)
                pdf.cell(60, 6, f"+${row['amount']}",1, align="C", fill = fill)
                pdf.ln()
            elif row["title"] == "Balance":
                pdf.cell(60, 7, row["date"],1, align="C", fill = fill)
                pdf.cell(60, 7, row["title"],1, align="C", fill = fill)
                pdf.cell(60, 7, f"${row['amount']}",1, align="C", fill = fill)
                pdf.ln()
            else:
                pdf.cell(60, 6, row["date"],1, align="C", fill = fill)
                pdf.cell(60, 6, row["title"],1, align="C", fill = fill)
                pdf.set_text_color(128,0,0)
                pdf.cell(60, 6, f"-${row['amount']}",1, align="C", fill = fill)
                pdf.ln()
                pdf.set_text_color(0)
            fill =  not fill

    pdf.output("BudgetReport.pdf")

def check_yes_no(ans):
    if ans.lower() not in ["yes", "y", "no", "n"]:
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