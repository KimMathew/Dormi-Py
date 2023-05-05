import csv
import sys
import pandas as pd

user_liabs = {
    'Russel': 'russel.txt',
    'Mochu': 'mochu.txt',
    'Gian': 'gian.txt',
    'Luna': 'luna.txt',
}

class Admin:
    def __init__(self, username):
        self.username = username

    def attendace_table(self): #Will show the attendance table of the users
        table = pd.read_csv("attendance.csv")
        print("\n", table, "\n")

    def who_is_at_home(self): #Will display the people at home
        with open('attendance.csv', mode='r', newline='') as csv_file:
            updater = csv.reader(csv_file)
            rows = list(updater)
            for i in range(len(rows)):
                if rows[i][1] == 'Time-in':
                    print(f"{rows[i][0]} is currently at home.")
    
    def liab_admin(self):
        # Load current liabilities from file
        liabilities = {}
        with open('liabilities.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':')
                if len(parts) != 2:
                    continue
                name, price = parts
                if not price.isdigit():
                    continue
                liabilities[name] = int(price)

        while True:
            print("Select an option:")
            print("1. Add liability")
            print("2. Remove liability")
            print("3. Assign liability to a specific user")
            print("4. Remove liability to a specific user")
            print("5. Exit")
            option = input("What do you want to do? ")

            if option == '1':
                liab_name = input("What's the name of the liability? ")
                liab_price = input("Price: ")
                price = int(liab_price)
                liabilities[liab_name] = price
                with open('liabilities.txt', 'a') as f:
                    f.write(f"{liab_name}:{price}\n")
                print(f"{liab_name} has been added with price {price}.")

            elif option == '2':
                print("Which liability do you want to remove?")
                for i, name in enumerate(liabilities):
                    print(f"[{i+1}] {name}: {liabilities[name]}")
                option_1 = input("Type the number of the liability you want to remove, or type 0 to cancel: ")
                if option_1 == '0':
                    continue
                elif option_1.isdigit() and 1 <= int(option_1) <= len(liabilities):
                    index = int(option_1) - 1
                    name = list(liabilities.keys())[index]
                    del liabilities[name]
                    with open('liabilities.txt', 'w') as f:
                        for name, price in liabilities.items():
                            f.write(f"{name}:{price}\n")
                    print(f"{name} has been removed.")
                else:
                    print("Invalid input.")

            elif option == '3':
                print("Which user do you want to assign a liability to?")
                option_1 = input("Insert his/her username: ")
                
                # dictionary that maps usernames to filenames
                file_dict = {'Mochu': 'mochu.txt',
                            'Russel': 'russel.txt',
                            'Gian': 'gian.txt',
                            'Luna': 'luna.txt',}
                
                # check if the entered username is in the dictionary
                if option_1 in file_dict:
                    liab_name = input("What's the name of the liability? ")
                    liab_price = input("Price: ")
                    price = int(liab_price)
                    liabilities[liab_name] = price
                    with open(file_dict[option_1], 'a') as f:
                        f.write(f"{liab_name}:{price}\n")
                    print(f"{liab_name} has been added with price {price}.")
                else:
                    print("Invalid input.")

            elif option == '4':
                username_to_file = {
                    'Russel': 'russel.txt',
                    'Mochu': 'mochu.txt',
                    'Gian': 'gian.txt',
                    'Luna': 'luna.txt',
            }
                print("Which user do you want to remove a liability from?")
                option_1 = input("Insert their username: ")
                filename = username_to_file.get(option_1)
                if filename:
                    with open(filename, 'r') as file1:
                        liab1 = file1.read()

                    with open('liabilities.txt', 'r') as file2:
                        liab2 = file2.read()

                    liab_all = liab1 + liab2

                    liab_list = liab_all.split('\n')  # convert to list of liabilities

                    print("The following liabilities are currently listed:")
                    for i, liab in enumerate(liab_list):
                        print(f"[{i+1}] {liab}")

                    item_number = int(input("\nWhich liability do you want to remove? Enter the corresponding number: "))

                    try:
                        item_to_remove = liab_list[item_number-1]  # get the specified item
                    except IndexError:
                        print("Invalid input. Please enter a valid number.")
                        return  # exit the function if number is invalid

                    liab_list.remove(item_to_remove)  # remove the specified item

                    liab_all = '\n'.join(liab_list)  # convert back to string

                    with open(filename, 'w') as file1:
                        file1.write(liab_all)

                    with open('liabilities.txt', 'w') as file2:
                        file2.write(liab_all)

                    print(f"{item_to_remove} removed successfully.")
                else:
                    print("Invalid username.")

            elif option == '5':
                print("Exiting liability admin...")
                break

            else:
                print("Invalid input.")

    def options(self):
        print("\n[1] Make an Announcement")
        print("[2] Add/Remove Liabilities")
        print("[3] View Attendance")
        print("[4] Log out")

class Regular(Admin):
    def __init__(self, username):
        self.username = username

    def attendance_checker(self, status, choice):
        with open('attendance.csv', mode='r', newline='') as csv_file: # update on csv
            updater = csv.reader(csv_file)
            rows = list(updater)

            for i in range(len(rows)): # updating the status
                if self.username in rows[i]:
                    rows[i][1] = status
                    break

            reasons_collection = ( # updating the reasons
                "School", "Meeting with Friends", "Meeting with family", "Going Home", "Buy Grocery", "Other Reason")
            
            if choice == 2: # getting the reason of the user for time-out
                print("\nSelect your reason for leaving: ")
                for i, reason in enumerate(reasons_collection):
                    print(f"[{i + 1}] {reason}")

                main_reason = int(input("\nYour Choice: "))
                reason = reasons_collection[main_reason - 1] if main_reason <= 5 else input(
                    "Please specify your reason for leaving: ")
                
                print(f"\n{self.username} is Time-out! Reason:", reason)
                for i in range(len(rows)):
                    if self.username in rows[i]:
                        rows[i][2] = reason

            if choice == 1: # change reasons to default
                print(f"\n{self.username} is Time-in!")
                for i in range(len(rows)):
                    if self.username in rows[i]:
                        rows[i][2] = "none"
                        break
                    
        with open('attendance.csv', mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

    def reg_liab(self, username):
        filename = user_liabs.get(username)

        if filename:
            with open(filename, 'r') as file1:
                liab1 = file1.read()

            with open('liabilities.txt', 'r') as file2:
                liab2 = file2.read()

            liab_all = liab1 + liab2

            liab_list = liab_all.split('\n')  # convert to list of liabilities

            if any(liab_list):
                print("\nThe following liabilities are currently listed:")
                for i, liab in enumerate(liab_list):
                    print(f"{i+1}. {liab}")
            else:
                print("\nNo liabilities")

    def options(self):
        print("\n[1] Announcements")
        print("[2] Liabilities")
        print("[3] Attendance")
        print("[4] Log out")




