import psycopg2
import json
from psycopg2.extras import Json

# ---------- 1. Connect to the database ----------
conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="1"
)
cur = conn.cursor()

# ---------- 2. Menu functions ----------
def search_contacts():
    term = input("Enter search term: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (term,))
    results = cur.fetchall()
    print("\nResults:")
    for r in results:
        print(f"Username: {r[0]}, Phone: {r[1]}")
    print()

def upsert_contact_menu():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    cur.execute("CALL upsert_contact(%s, %s)", (username, phone))
    conn.commit()
    print("Upsert completed.\n")

def bulk_insert_menu():
    users = []
    print("Enter contacts in format 'username,phone'. Type 'done' when finished:")
    while True:
        line = input("> ")
        if line.lower() == "done":
            break
        try:
            uname, uphone = line.split(",")
            users.append({"username": uname.strip(), "phone": uphone.strip()})
        except:
            print("Invalid format. Use username,phone")

    if users:
        # Explicitly cast to JSON in SQL
        cur.execute("CALL bulk_insert_from_json(%s::json)", (json.dumps(users),))
        conn.commit()
        print("Bulk insert completed.\n")

def delete_contact_menu():
    value = input("Enter username or phone to delete: ")
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    print("Delete completed.\n")

def get_paginated_menu():
    lim = int(input("Enter limit: "))
    off = int(input("Enter offset: "))
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (lim, off))
    results = cur.fetchall()
    print("\nPaginated Results:")
    for r in results:
        print(f"Username: {r[0]}, Phone: {r[1]}")
    print()

# ---------- 3. Main menu loop ----------
def main_menu():
    while True:
        print("=== PHONEBOOK MENU ===")
        print("1. Search Contacts")
        print("2. Upsert Contact")
        print("3. Bulk Insert Contacts")
        print("4. Delete Contact")
        print("5. Paginated View")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            upsert_contact_menu()
        elif choice == "3":
            bulk_insert_menu()
        elif choice == "4":
            delete_contact_menu()
        elif choice == "5":
            get_paginated_menu()
        elif choice == "6":
            break
        else:
            print("Invalid choice, try again.\n")

# ---------- 4. Run the menu ----------
if __name__ == "__main__":
    try:
        main_menu()
    finally:
        cur.close()
        conn.close()