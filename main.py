import sys
import json
import os
import getpass
import hashlib

FILENAME = "Residents_database.json"
PASSWORD_FILE = "password.json"
USERNAME = "admin"
if os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "r") as file:
        PASSWORD_HASH = json.load(file)
else:
    PASSWORD_HASH = hashlib.sha256(
        "admin123".encode()
    ).hexdigest()

def login():
    print("\n===== BARANGAY SYSTEM LOGIN =====")

    for attempt in range(3):
        username = input("Username: ").strip()
        password = input("Password: ")

        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()
        
        if username == USERNAME and password_hash == PASSWORD_HASH:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password.")

    print("Too many failed attempts.")
    return False

def change_password():
    global PASSWORD_HASH

    print("\n===== CHANGE PASSWORD =====")

    current = getpass.getpass("Current password: ")
    current_hash = hashlib.sha256(
        current.encode()
    ).hexdigest()

    if current_hash != PASSWORD_HASH:
        print("Wrong current password.")
        return

    new_password = input("New password: ")

    if len(new_password) < 8:
        print("Password must be at least 8 characters.")
        return

    confirm = getpass.getpass("Confirm new password: ")


    if new_password != confirm:
        print("Passwords do not match.")
        return

    PASSWORD_HASH = hashlib.sha256(
        new_password.encode()
    ).hexdigest()

    with open(PASSWORD_FILE, "w") as file:
        json.dump(PASSWORD_HASH, file)

    print("Password changed successfully!")

def load_data():
    """Loads records from the JSON file when the program starts."""
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except Exception:
        return {}

def save_data(database):
    """Saves records to the JSON file automatically."""
    try:
        with open(FILENAME, "w") as file:
            json.dump(database, file, indent=4)
    except Exception as e:
        print(f"System Storage Error: Could not save data. {e}")
        
def display_menu():
    print("\n=========================================================================")
    print("                BARANGAY SERVICES REQUEST MANAGEMENT SYSTEM                           ")
    print("\n=========================================================================")
    print(" [1] Log New Request")
    print(" [2] View All Requests")
    print(" [3] Update Request Status")
    print(" [4] Search Residents Records")
    print(" [5] Change Password")
    print(" [6] Exit")
    print("===========================================================================")
    choice = input("Select an option (1-6):").strip()
    return choice

def log_request(database):
    print("\n>>> LOG NEW REQUEST <<<")
    name = input("Enter Resident Full Name: ").strip()
    if not name:
        print("Validation Error: Name field cannot be left blank.")
        return

    age = input("Enter Resident Age: ").strip()
    birthday = input("Enter Resident Birthday (YYYY-MM-DD): ").strip()
    address = input("Enter Resident Address: ").strip()

    print("\nSelect Document Tyhpe:")
    print(" [1] Barangay Clearance")
    print(" [2] Certificate of Indigency")
    print(" [3] Certificate of Residency")
    doc_type_choice = input("Choice (1-3): ").strip()

    types = {"1": "Barngay Clearance", "2": "Certificate of Indigency", "3": "Certificate of Residency"}
    doc_type = types.get(doc_type_choice, "Barangay Clearance")

    purpose = input("Enter Purpose of Request: ").strip()
    if not purpose:
        print("Validation Error: Purpose field cannot blank.")
        return

    request_id = len(database) + 1
    new_entry = {
        "id": request_id,
        "resident_name": name,
        "age": age,
        "birthday": birthday,
        "address": address,
        "document_type": doc_type,
        "purpose": purpose,
        "status": "Pending"
    }
    database.append(new_entry)
    save_data(database)
    print(f"Success: Request ID {request_id} has been recorded!")

def view_all_requests(database):
    print("\n>>> VIEW ALL REQUESTS <<<")
    if not database:
        print("No actice records found in the system database.")
        return
    print("-" * 75)
    print(f"{'ID':<5} | {'Resident Name':<22} | {'Document Type':<25} | {'Status':<10} ")
    print("-" * 75)
    for item in database:
        print(f"{item['id']:<5} | {item['resident_name']} | {item['document_type']:<25} | {item['status']:<10}")
    print("-" * 75)

def update_status(database):
    print("\n>>> UPDATE REQUEST STATUS <<<")
    if not database:
        print("No active database records found.")
        return

    try:
        search_id = int(input("Enter Request Id to update: "))
        for item in database:
            if item["id"] == search_id:
                print(f"\nCurrent Status: {item['status']}")
                print(" [1] Pending")
                print(" [2] Completed")
                new_status_choice = input("Select new status (1-2): ").strip()
                item["status"] = "Completed" if new_status_choice == "2" else "Pending"
                print(f"Sxuccess: Request ID {search_id} updated to {item['status']}.")
                return
        print("Error: Request ID not found in system records.")
    except ValueError:
        print("Validation Error: Please enter a valid numerical ID.")

def search_records(database):
    print("\n>>> SEARCH RESIDENT RECORDS <<<")
    if not database:
        print("No records to search through.")
        return
    query = input("Enter Resident Name keyword to search: ").strip().lower()
    found = False
    for item in database:
        if query in item['resident_name'].lower():
            if not found:
                print("-" * 90)
                print(
                    f"{'ID':<4} | {'Resident Name':<18} | {']age':<3} | "
                    f"{'Birthday':<10} | {'Address':<18} | "
                )
                print("-" * 90)
                found = True

            print(
                f"{item['id']:<4} | "
                f"{item['resident_name'][:18]:<18} | "
                f"{item.get('age', 'N/A'):<3} | "
                f"{item.get('birthday', 'N/A'):<10} | "
                f"{item.get('address', 'N/A')[:18]:<18}"
            )
            print(
                f"Document: {item['document_type']} | "
                f"Purpose:{item['purpose']} | "
                f"Status:{item['status']}"
            )
            print("-" * 90)

    if not found:
        print(f"No records found matching tracking query: '{query}'.")
    else:
        print("-" * 75)

def main():
    database = load_data()
    while True:
        choice = display_menu()
        if choice == "1":
            log_request(database)
        elif choice == "2":
            view_all_requests(database)
        elif choice == "3":
            update_status(database)
        elif choice == "4":
            search_records(database)
        elif choice == "5":
            change_password()
        elif choice == "6":
            print("\nExiting systemm panel safely. Goodbye!")
            sys.exit()
        else:
            print("\nInvalid selection choice line. Please enter numbers 1 to 5 only.")

if __name__ == "__main__":
    if login():
        main()
    else:
        print("System closed.")