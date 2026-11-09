import speech_recognition as sr
import pyttsx3
import csv
import os
from datetime import datetime


# Text-to-speech setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Speech recognition setup
r = sr.Recognizer()
r.pause_threshold = 0.4
r.non_speaking_duration = 0.5


# CSV file configuration
filename = "expenses.csv"

fieldnames = ["name", "category", "amount", "date"]


# Create CSV file and add column headings if necessary
with open(filename, "a", newline="", encoding="utf-8") as file:

    if os.path.getsize(filename) == 0:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()


# Load previously saved expenses
expenses = []

with open(filename, "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        expense = {
            "name": row["name"],
            "category": row["category"],
            "amount": float(row["amount"]),
            "date": row["date"]
        }

        expenses.append(expense)


print("\n===== PERSONAL EXPENSE TRACKER =====\n")
print("Previously saved expenses loaded:", len(expenses))


engine.say("Hello Welcome to the Personal Expense Tracker Application.")
engine.say("You can add your expenses, view all expenses, calculate total expenses and search expenses by category.")
engine.say("Please choose an option.")
engine.runAndWait()


while True:

    print("\n 1. Add Expense \n 2. View All Expenses \n 3. Total Expenses \n 4. Search Expense by Category \n 5. Exit \n")

    try:

        with sr.Microphone() as source:

            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening for option number...")
            audio = r.listen(source, timeout=10, phrase_time_limit=5)

        text = r.recognize_google(audio)
        print("Recognized:", text)

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        continue

    except sr.RequestError as e:
        print("Speech recognition service error:", e)
        continue

    except sr.WaitTimeoutError:
        print("No voice detected. Please try again.")
        continue


    choices = {
        "1": 1,
        "one": 1,
        "won": 1,
        "first": 1,
        "2": 2,
        "two": 2,
        "second": 2,
        "3": 3,
        "three": 3,
        "third": 3,
        "4": 4,
        "four": 4,
        "fourth": 4,
        "5": 5,
        "five": 5,
        "fifth": 5
    }

    words = text.lower().split()
    word = choices.get(words[-1], None) if words else None


    # OPTION 1: ADD EXPENSE

    if word == 1:

        engine.stop()
        engine.say("What is the expense name?")
        engine.runAndWait()

        try:

            with sr.Microphone() as source:

                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for expense name...")
                audio = r.listen(source, timeout=10, phrase_time_limit=4)

            text = r.recognize_google(audio)
            expense_name = text
            print("Expense name:", expense_name)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the expense name.")
            continue

        except sr.RequestError as e:
            print("Speech recognition service error:", e)
            continue

        except sr.WaitTimeoutError:
            print("No voice detected.")
            continue


        engine.stop()
        engine.say("What is the category name?")
        engine.runAndWait()

        try:

            with sr.Microphone() as source:

                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for category...")
                audio = r.listen(source, timeout=10, phrase_time_limit=6)

            text = r.recognize_google(audio)
            category = text
            print("Category:", category)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the category.")
            continue

        except sr.RequestError as e:
            print("Speech recognition service error:", e)
            continue

        except sr.WaitTimeoutError:
            print("No voice detected.")
            continue


        engine.stop()
        engine.say("What is the amount?")
        engine.runAndWait()

        try:

            with sr.Microphone() as source:

                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for amount...")
                audio = r.listen(source, timeout=10, phrase_time_limit=6)

            text = r.recognize_google(audio)
            print("Recognized amount:", text)

            amount = float(text.replace(",", ""))

            if amount <= 0:
                print("Please enter an amount greater than zero.")
                continue

        except sr.UnknownValueError:
            print("Sorry, I could not understand the amount.")
            continue

        except sr.RequestError as e:
            print("Speech recognition service error:", e)
            continue

        except sr.WaitTimeoutError:
            print("No voice detected.")
            continue

        except ValueError:
            print("Please speak the amount as a number.")
            continue


        date = datetime.now().strftime("%Y-%m-%d")

        expense = {
            "name": expense_name,
            "category": category,
            "amount": amount,
            "date": date
        }


        # Add expense to Python list
        expenses.append(expense)


        # Save expense permanently in CSV file
        with open(filename, "a", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(expense)


        print("\nExpense saved successfully!")
        print(expense)

        engine.stop()
        engine.say("Your expense has been added successfully.")
        engine.runAndWait()


    # OPTION 2: VIEW ALL EXPENSES

    elif word == 2:

        print("\n========== ALL EXPENSES ==========\n")

        if len(expenses) == 0:

            print("No expenses have been added yet.")

        else:

            print(f"{'Name':<20}{'Category':<20}{'Amount':<12}{'Date':<15}")

            for item in expenses:

                print(f"{item['name']:<20}{item['category']:<20}{item['amount']:<12.2f}{item['date']:<15}")


    # OPTION 3: TOTAL EXPENSES

    elif word == 3:

        print("\n========== TOTAL EXPENSES ==========\n")

        total = 0

        for item in expenses:

            total += item['amount']

        print(f"\nTotal Expenses: ₹{total:.2f}")


    # OPTION 4: SEARCH EXPENSE BY CATEGORY

    elif word == 4:

        search_category = input("\nEnter category to search: ")

        print(f"\n========== EXPENSES IN CATEGORY: {search_category} ==========\n")

        found = False

        for items in expenses:

            if items['category'].lower() == search_category.lower():

                print(f"{items['name']:<20}{items['category']:<20}{items['amount']:<12.2f}{items['date']:<15}")

                found = True

        if found == False:

            print("No expenses found in this category.")


    # OPTION 5: EXIT

    elif word == 5:

        print("\nExiting the program. Goodbye!")

        engine.stop()
        engine.say("Goodbye!")
        engine.runAndWait()

        break


    else:

        print("\nInvalid choice. Please try again.")
