# seatingChart.py
# program to create seating chart for movie theater

import string

#-------------------------------------GLOBAL VARIABLES-------------------------------------#
LIMIT_ROW = 100
LIMIT_COLUMN = 100

rows = 0
columns = 0
tickets_sold = 0
revenue = 0

row_prices = []

seating_chart = [[0 for column in range(columns)] for row in range(rows)]
#-------------------------------------------------------------------------------------------#

# collects user input for number of rows
def row_input():
    global rows
    rows = int(
        input("Welcome! Enter the amount of rows (Max of {}): ".format(LIMIT_ROW)))

    # checks if amount entered is invalid
    while (rows > LIMIT_ROW or rows < 1):
        print("Error, number of rows is not valid.")
        rows = int(input("Please enter the amount of rows: "))

# collects user input for number of columns
def column_input():
    global columns
    columns = int(
        input("Next, enter the amount of columns (Max of {}): ".format(LIMIT_COLUMN)))

    # checks if amount entered is invalid
    while (columns > LIMIT_COLUMN or columns < 1):
        print("Error, number of columns is not valid.")
        columns = int(input("Please enter the amount of rows: "))

# gets price inputs
def price_input():
    global row_prices
    print("Now, enter the price of each row")

    # iterates through rows and assigns price to them
    for i in range(rows):
        price = int(input("Price of row {}: ".format(i + 1)))
        row_prices.append(price)

        # if price is invalid, pop back value and enter new one
        while (row_prices[i] < 0):
            row_prices.pop()
            print("Invalid price for row.")
            price = int(
                input("Please enter the price of row {} again: ".format(i + 1)))
            row_prices.append(price)

# reads from config and stores values into variables
def read_from_config():
    global row_prices
    global rows
    global columns

    with open("theater.txt", "r") as c:
        # assigns first two values to rows and columns
        rows = int(c.readline())
        columns = int(c.readline())

        line = c.readline()  # reads line, returning string
        number = int(line)  # converts string to int
        # reads through file and appends values to row_price list
        while line != '':  # while not eof
            number = int(line)
            row_prices.append(number)
            line = c.readline()

# stores all values in config (theater.txt)
def store_in_config(rows_config, columns_config):
    # converts config and column int to string to be stored
    rows_config = str(rows_config)
    columns_config = str(columns_config)

    # writes the rows, columns and row prices to theater.txt
    with open("theater.txt", "w") as c:
        c.write(rows_config)
        c.write("\n")

        c.write(columns_config)
        c.write("\n")

        for i in range(rows):
            price = str(row_prices[i])
            c.write(price)
            c.write("\n")

# creates a "blank" seating chart filled with "#"
def fill_chart(rows_config, columns_config):
    global seating_chart
    seating_chart = [["#" for column in range(columns_config)] for row in range(rows_config)]

# prints seating chart
def print_chart(rows_config, columns_config):
    global seating_chart
    # Prints column numbers
    print("               "),
    print("      Column")
    print("               "),

    # Displays column numbers
    for i in range(columns_config):
        if ((i+1) == 1):
            print("0"),
        elif ((i+1) % 10 == 0):
            print(i+1)/10,
        else:
            print(" "),
    print("\n")
    print("               "),

    for k in range(columns_config):
        print((k+1) % 10),
    print("\n")

    # Displays rows
    for r in range(rows_config):
        print("Row {}: ".format(r+1)),
        print("\t"),
        for c in range(columns_config):
            print(seating_chart[r][c]),
        print("\n")
    print("\n")

# sells multiple tickets
def sell_tickets():
    global row_prices
    global tickets_sold
    global revenue
    sold = False

    # Gets row of series of seats being sold
    row_choice = int(input("Enter the row of the seats: "))
    while (row_choice < 1 or row_choice > rows):
        row_choice = int(input("Invalid row, enter another: "))

    # Gets beginning of range
    column_one = int(
        input("Enter the number of the first seat (the one on the left): "))
    while (column_one < 1 or column_one > columns or column_one == columns):
        column_one = int(
            input("Invalid. Enter the number of the first seat: "))

    # Gets end of range
    column_two = int(
        input("Enter the number of the last seat (the one on the right): "))
    while (column_two < 1 or column_two > columns):
        column_two = int(input("Invalid. Enter the number of the last seat: "))
    while(column_two <= column_one):
        column_two = int(input(
            "Invalid, left seat greater than or equal to right seat. Re-enter right seat: "))
    # If seat is sold, subtract tickets_sold and revenue,
    # then display error and set sold to true
    for i in range((column_one - 1), (column_two)):
        if(seating_chart[row_choice - 1][i] == "*"):
            print("\n")
            print("Error, a seat in this range is already sold!")
            sold = True
            break
        else:
            sold = False

    # If sold is false, sell seat and update ticketes_sold and revenue
    if (sold == False):
        for j in range((column_one - 1), column_two):
            seating_chart[row_choice - 1][j] = "*"
            tickets_sold += 1
            number = row_choice - 1
            revenue += row_prices[number]

# sells single ticket
def sell_ticket(rows_config, columns_config):
    global row_prices
    global tickets_sold
    global revenue
    choice = "y"

    # asks for row and column of seat being sold and checks that they're valid.
    while (choice == "y"):
        # gets row of seat and checks validity
        row_choice = int(input("Enter the row of the seat: "))
        while (row_choice < 1 or row_choice > rows_config):
            row_choice = int(input("Invalid row, enter another: "))

        # gets column of seat and checks validity
        column_choice = int(input("Enter the column of the seat: "))
        while (column_choice < 1 or column_choice > columns_config):
            column_choice = int(input("Invalid column, enter another: "))

        # checks to see if selection is sold or not
        if (seating_chart[row_choice - 1][column_choice - 1] == "*"):
            choice = raw_input(
                "Seat already sold, would you like to sell another? (y)es or (n)o: ").tolower()

        # if seat isn't sold, update it with asterisk, increment tickets_sold & revenue
        if (seating_chart[row_choice - 1][column_choice - 1] == "#"):
            seating_chart[row_choice - 1][column_choice - 1] = "*"
            number = int(row_choice - 1)
            revenue += row_prices[number]
            tickets_sold += 1

        choice = raw_input(
            "Type (y) to sell another seat, any other key to continue: ")

# iterates through chart and counts available seats
def seats_available():
    available = 0
    for l in range(rows):
        for m in range(columns):
            if (seating_chart[l][m] == "#"):
                available += 1
    return available

# resets all values and lists
def reset_program():
    global row_prices
    global revenue
    global tickets_sold
    global rows
    global columns

    revenue = 0
    tickets_sold = 0
    rows = 0
    columns = 0
    # row_prices.reverse()
    for i in range(len(row_prices)):
        row_prices.pop()

    row_input()
    column_input()
    price_input()
    store_in_config(rows, columns)
    read_from_config()
    fill_chart(rows, columns)

# main menu function to run the program
def main_menu():
    print("\n")
    print("Choose from one of the following: ")
    print("1). Display a seating chart")
    print("2). Sell one or more tickets")
    print("3). View how many tickets have been sold")
    print("4). View how many seats are available")
    print("5). View the total revenue")
    print("6). Reset the program and re-enter seating and pricing information")
    print("7). Exit program")

    user_choice = input("Choice: ")
    print("\n")
    while (user_choice != 1 and user_choice != 2 and user_choice != 3 and user_choice != 4 and user_choice != 5 and user_choice != 6 and user_choice != 7):
        print("Error, invalid choice.")
        user_choice = input("Please choose a valid option: ")

    # Displays seating chart
    if (user_choice == 1):
        print_chart(rows, columns)
        main_menu()

    # Sells tickets
    if (user_choice == 2):
        sell_choice = raw_input(
            "Would you like to sell (o)ne or (m)ultiple tickets? ").lower()
        while (sell_choice != "o" and sell_choice != "m"):
            print("Invalid input.")
            sell_choice = raw_input(
                "Would you like to sell (o)ne or (m)ultiple tickets? ").lower()
        if (sell_choice == "o"):
            sell_ticket(rows, columns)
        if (sell_choice == "m"):
            sell_tickets()
        main_menu()

    # Displays number of tickets sold
    if (user_choice == 3):
        number = tickets_sold
        print("{} ticket(s) have been sold".format(number))
        main_menu()

    # Displays seats available
    if (user_choice == 4):
        number = seats_available()
        print("Seats available: {}".format(number))
        main_menu()

    # Displays total revenue
    if (user_choice == 5):
        print("Total revenue: ${}".format(revenue))
        main_menu()

    # Resets the program and returns to main menu
    if (user_choice == 6):
        reset_program()
        main_menu()

    # Exits Program
    if (user_choice == 7):
        exit




#-------------------------------------DRIVER CODE-----------------------------------------#
read_from_config()
print("Welcome to the seating chart assistant program!")
print("Pre-loaded Rows: {}".format(rows))
print("Pre-loaded Columns: {}".format(columns))

# asks is user wants to put in new price / seating info or use old
choice = raw_input(
    "Would you like to use your (o)ld settings or create (n)ew ones?: ").lower()

while(choice != "o" and choice != "n"):
    choice = raw_input(
        "Error, invalid input. (o)ld settings or create (n)ew ones?: ").lower()

# if using old, fill chart with # and display main menu
if (choice == "o"):
    fill_chart(rows, columns)
    main_menu()

# if using new, prompt for info, store in config, fill chart, show menu
if (choice == "n"):
    row_input()
    column_input()
    price_input()
    store_in_config(rows, columns)
    read_from_config()
    fill_chart(rows, columns)
    main_menu()
