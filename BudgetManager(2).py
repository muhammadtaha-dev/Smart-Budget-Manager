import datetime

# SMART BUDGET MANAGER
# A simple monthly expense tracking system


# List that stores user budget information
budget_list:list=[]


def AddExpense(Category,Item,Amount):

    current_date=datetime.datetime.now()

    expenses:dict={

        "Category":Category,

        "Item":Item,

        "Amount":Amount,

        "Month":current_date.strftime("%B"),

        "Year":current_date.year
    }

    return expenses


def Total_Spending():

    total:float=0

    for i in budget_info["Expenses"]:

        total+=i["Amount"]

    return total


def Check_Budget():

    total_amount:float=Total_Spending()

    if total_amount>budget_info["Total Budget"]:

        print("Danger! Budget exceeded.")

    elif total_amount>=budget_info["Total Budget"]*0.8 and total_amount<=budget_info["Total Budget"]:

        print("Warning! Near budget limit.")

    else:

        print("Budget is under control!")


print("********WELCOME TO SMART BUDGET MANAGER********")


# Take user details
name:str=str(input("Enter your name: "))
age:int=int(input("Enter your age: "))
total_budget:float=float(input("Enter your total budget: "))


# Store user information in dictionary
budget_info:dict={

    "Name":name,
    "Age":age,
    "Total Budget":total_budget,

    # Empty list to store expenses
    "Expenses":[]
}


# Store user data in main budget list
budget_list.append(budget_info)


# MAIN MENU LOOP
# Runs continuously until user exits
while True:

    # Display menu
    print("\n1.Add Expense")
    print("2.Show Expenses")
    print("3.Total Spending")
    print("4.Check Budget")
    print("5.Exit")


    # Take menu choice from user
    option:int=int(input("Enter choice (1-5): "))


    # Match-case menu system
    match option:

        # CASE 1=Add Expense
        case 1:

            Category:str=str(input("Enter the category: "))
            Item:str=str(input("Enter item name: "))
            Amount:float=float(input(f"Enter amount of {Item}: "))

            budget_info["Expenses"].append(
                AddExpense(Category,Item,Amount)
            )

        # CASE 2=Show Expenses
        case 2:

            if len(budget_info["Expenses"])==0:

                print("No Expense!")

            else:

                for i in budget_info["Expenses"]:

                    print("Category: ",i["Category"])
                    print("Item: ",i["Item"])
                    print("Amount: ",i["Amount"])
                    print("Month: ",i["Month"])
                    print("Year: ",i["Year"])


        # CASE 3=Show Total Spending
        case 3:

            print(Total_Spending())


        # CASE 4=Check Budget Status
        case 4:

            Check_Budget()


        # CASE 5=Exit Program
        case 5:

            print("Thanks for using Smart Budget Manager!")
            break


        # DEFAULT CASE=Invalid Input
        case _:

            print("Invalid choice!")