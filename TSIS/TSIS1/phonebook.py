import csv
import json
from connect import get_connection


# ---------------------------------------------------------
# Helper function to print database rows in a readable format
# ---------------------------------------------------------
def print_rows(rows):
    if not rows:
        print("No contacts found.")
        return

    print("-" * 120)
    for row in rows:
        print(row)
    print("-" * 120)


# ---------------------------------------------------------
# Helper function to get group ID
# If group does not exist, it creates it automatically
# ---------------------------------------------------------
def get_group_id(cur, group_name):
    # If user leaves group empty, we use "Other" as default group
    if not group_name or group_name.strip() == "":
        group_name = "Other"

    # Insert group only if it does not already exist
    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    # Get group ID to connect contact with this group
    cur.execute("""
        SELECT id FROM groups
        WHERE name = %s
    """, (group_name,))

    return cur.fetchone()[0]


# ---------------------------------------------------------
# Add new contact with email, birthday, group, and phone
# This function inserts data into contacts and phones tables
# ---------------------------------------------------------
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD or empty: ")
    group_name = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    # Empty birthday must be stored as NULL in PostgreSQL
    birthday = birthday if birthday.strip() else None

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Get group id or create group if it does not exist
        group_id = get_group_id(cur, group_name)

        # Insert contact and return generated contact ID
        cur.execute("""
            INSERT INTO contacts(username, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        # Insert phone into separate phones table
        # This supports one contact having many phone numbers
        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (contact_id, phone, phone_type))

        conn.commit()
        print("Contact added successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Add another phone number to an existing contact
# Uses PostgreSQL stored procedure add_phone()
# ---------------------------------------------------------
def add_phone_console():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Move existing contact to another group
# Uses PostgreSQL stored procedure move_to_group()
# ---------------------------------------------------------
def move_group_console():
    name = input("Contact name: ")
    group_name = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        conn.commit()
        print("Contact moved successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Search contacts by name, email, phone, or group
# Uses PostgreSQL function search_contacts()
# ---------------------------------------------------------
def search_contacts_console():
    query = input("Search query: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()
        print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Filter contacts by group name
# Example: show only Family or Work contacts
# ---------------------------------------------------------
def filter_by_group():
    group_name = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                c.username,
                c.email,
                c.birthday,
                g.name AS group_name,
                p.phone,
                p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name ILIKE %s
            ORDER BY c.username
        """, (group_name,))

        rows = cur.fetchall()
        print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Search contacts by partial email
# Example: searching "gmail" shows all Gmail contacts
# ---------------------------------------------------------
def search_by_email():
    email_query = input("Email keyword: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                c.username,
                c.email,
                c.birthday,
                g.name AS group_name,
                p.phone,
                p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.email ILIKE %s
            ORDER BY c.username
        """, (f"%{email_query}%",))

        rows = cur.fetchall()
        print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Sort contacts by name, birthday, or date added
# User chooses sorting field from menu
# ---------------------------------------------------------
def sort_contacts():
    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    # Dictionary protects from SQL injection
    allowed_columns = {
        "1": "c.username",
        "2": "c.birthday",
        "3": "c.date_added"
    }

    order_by = allowed_columns.get(choice, "c.username")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(f"""
            SELECT 
                c.username,
                c.email,
                c.birthday,
                c.date_added,
                g.name AS group_name,
                p.phone,
                p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY {order_by}
        """)

        rows = cur.fetchall()
        print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Paginated navigation
# Uses existing PostgreSQL function get_contacts_paginated(limit, offset)
# User can type next, prev, or quit
# ---------------------------------------------------------
def paginated_navigation():
    limit = 5
    offset = 0

    conn = get_connection()
    cur = conn.cursor()

    try:
        while True:
            cur.execute("""
                SELECT * FROM get_contacts_paginated(%s, %s)
            """, (limit, offset))

            rows = cur.fetchall()
            print_rows(rows)

            command = input("next / prev / quit: ").lower()

            if command == "next":
                offset += limit

            elif command == "prev":
                offset = max(0, offset - limit)

            elif command == "quit":
                break

            else:
                print("Invalid command.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Export all contacts to JSON
# JSON includes contact info, group, and all phone numbers
# ---------------------------------------------------------
def export_json():
    filename = input("JSON filename to export, for example contacts.json: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                c.id,
                c.username,
                c.email,
                c.birthday,
                c.date_added,
                g.name AS group_name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
        """)

        contacts = cur.fetchall()
        result = []

        for contact in contacts:
            contact_id, name, email, birthday, date_added, group_name = contact

            # Get all phone numbers for this contact
            cur.execute("""
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
            """, (contact_id,))

            phones = cur.fetchall()

            # Create nested JSON structure
            result.append({
                "name": name,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "date_added": str(date_added) if date_added else None,
                "group": group_name,
                "phones": [
                    {
                        "phone": phone_row[0],
                        "type": phone_row[1]
                    }
                    for phone_row in phones
                ]
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print("Export completed successfully.")

    except Exception as error:
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Import contacts from JSON
# If contact already exists, user chooses skip or overwrite
# ---------------------------------------------------------
def import_json():
    filename = input("JSON filename to import, for example contacts.json: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            name = item.get("name")
            email = item.get("email")
            birthday = item.get("birthday")
            group_name = item.get("group") or "Other"
            phones = item.get("phones", [])

            # Convert empty or invalid birthday values to NULL
            birthday = birthday if birthday not in ["", "None", None] else None

            # Check duplicate by username
            cur.execute("""
                SELECT id FROM contacts
                WHERE username = %s
            """, (name,))

            existing = cur.fetchone()

            if existing:
                action = input(f"{name} already exists. skip/overwrite: ").lower()

                if action == "skip":
                    continue

                elif action == "overwrite":
                    contact_id = existing[0]
                    group_id = get_group_id(cur, group_name)

                    # Update main contact data
                    cur.execute("""
                        UPDATE contacts
                        SET email = %s,
                            birthday = %s,
                            group_id = %s
                        WHERE id = %s
                    """, (email, birthday, group_id, contact_id))

                    # Delete old phones before inserting new ones
                    cur.execute("""
                        DELETE FROM phones
                        WHERE contact_id = %s
                    """, (contact_id,))

                else:
                    print("Unknown action. Contact skipped.")
                    continue

            else:
                group_id = get_group_id(cur, group_name)

                # Insert new contact
                cur.execute("""
                    INSERT INTO contacts(username, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (name, email, birthday, group_id))

                contact_id = cur.fetchone()[0]

            # Insert all phones for this contact
            for phone_item in phones:
                phone = phone_item.get("phone")
                phone_type = phone_item.get("type")

                if phone and phone_type in ["home", "work", "mobile"]:
                    cur.execute("""
                        INSERT INTO phones(contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, phone, phone_type))

        conn.commit()
        print("Import completed successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Extended CSV import
# CSV must include:
# name,email,birthday,group,phone,phone_type
# ---------------------------------------------------------
def import_csv_extended():
    filename = input("CSV filename, for example contacts.csv: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row.get("name")
                email = row.get("email")
                birthday = row.get("birthday")
                group_name = row.get("group") or "Other"
                phone = row.get("phone")
                phone_type = row.get("phone_type")

                birthday = birthday if birthday not in ["", "None", None] else None

                group_id = get_group_id(cur, group_name)

                # Insert new contact or update existing contact
                cur.execute("""
                    INSERT INTO contacts(username, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (username)
                    DO UPDATE SET
                        email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                    RETURNING id
                """, (name, email, birthday, group_id))

                contact_id = cur.fetchone()[0]

                # Insert phone if phone data is valid
                if phone and phone_type in ["home", "work", "mobile"]:
                    cur.execute("""
                        INSERT INTO phones(contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, phone, phone_type))

        conn.commit()
        print("CSV import completed successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# Main console menu
# This function connects all project features together
# ---------------------------------------------------------
def menu():
    while True:
        print("""
PHONEBOOK EXTENDED MENU

1. Add contact
2. Add phone to existing contact
3. Move contact to group
4. Search contacts
5. Filter by group
6. Search by email
7. Sort contacts
8. Paginated navigation
9. Export to JSON
10. Import from JSON
11. Import CSV extended
0. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()

        elif choice == "2":
            add_phone_console()

        elif choice == "3":
            move_group_console()

        elif choice == "4":
            search_contacts_console()

        elif choice == "5":
            filter_by_group()

        elif choice == "6":
            search_by_email()

        elif choice == "7":
            sort_contacts()

        elif choice == "8":
            paginated_navigation()

        elif choice == "9":
            export_json()

        elif choice == "10":
            import_json()

        elif choice == "11":
            import_csv_extended()

        elif choice == "0":
            print("Program finished.")
            break

        else:
            print("Wrong choice. Try again.")


# ---------------------------------------------------------
# Program starts here
# ---------------------------------------------------------
if __name__ == "__main__":
    menu()