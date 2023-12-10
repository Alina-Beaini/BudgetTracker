# BudgetTracker

#### Video Demo:  <https://youtu.be/YX-_n_iqJ0o>
#### Description:

BudgetTracker is a Python project designed to help users to track their expenses.

## Functionality

Once you run the app, the program will first check whether this is a new user or not. 
If you're a new user, it will guide you through the initialization process by prompting you for your current balance and salary.
Otherwise, it will present the main menu to choose from the 4 available options:

**1. Add a New Expense**: Allows you to input details of a new expense, specifying whether it's a one-time or monthly occurrence. For monthly expenses, the user provides the day of the month on which the transaction occurs. It will also return your new balance. 

**2. Change Monthly Income/Salary**: Allows you to update your monthly income.

**3. Check Balance**: Displays the current balance on the record.

**4. Print Out a Report**: Generates a detailed PDF report containing all of the transactions. The first row of the report contains the most up-to-date balance. 



## Files

1. **"budgeting.csv"**: A CSV file containing the balance and all of the transactions. The data is stored in the form ["Date", "Title", "Amount"].
The first row will always contain the balance and the date is always the last time the user ran the code. 
2. **"monthlydata.csv"**: A CSV file that stores all of the monthly expenses as well as the salary. Each row is of the form ["Title", "Amount", "Due Date"]. It is assumed that only the "Salary" is an added value, and all of the others are subtracted from the balance on their due date. 
3. **"project.py"**: Contains the python application. 
4. **"test_project.py"**: Contains test functions for some of the functions in "project.py".
5. **"BudgetReport.pdf"**: A PDF file generated by the program when the user chooses to print out the report.
6. **"requirements.txt"**: Contains all pip-installable libraries that the project requires. 


## Design Choices
1. Using File I/O (with CSV and PDF) rather than databases (with SQLite). This decision was made just to be in line with the chapters explained in the course CS50P. My goal is to later modify the project by using databases instead. This will also allow to accommodate multiple users at once.
2. The 4 main functionalities. I had to make a choice on what are the most useful functionalities that a user might need. The program was written in a way that it's easy to add functionalities, if needed.
3. Printing the report as a PDF. This decision was made to provide the user with a visually appealing document that they can save for their record. 

## Authors

- [@Alina-Beaini](https://github.com/Alina-Beaini)
