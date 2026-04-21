import json
from connect import connect

def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts(name, email, birthday) VALUES (%s,%s,%s)",
        (name, email, birthday)
    )

    conn.commit()
    cur.close()
    conn.close()


def add_phone():
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()


def move_group():
    name = input("Name: ")
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s,%s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()


def search():
    q = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def filter_group():
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    data = cur.fetchall()

    result = []
    for row in data:
        result.append({
            "name": row[0],
            "email": row[1],
            "birthday": str(row[2]),
            "group": row[3],
            "phone": row[4],
            "type": row[5]
        })

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    cur.close()
    conn.close()


def import_json():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        name = item["name"]
        email = item["email"]
        birthday = item["birthday"]
        group = item["group"]
        phone = item["phone"]
        ptype = item["type"]

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists (skip/overwrite): ")
            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute(
            "INSERT INTO contacts(name,email,birthday) VALUES (%s,%s,%s)",
            (name, email, birthday)
        )

        cur.execute("CALL move_to_group(%s,%s)", (name, group))
        cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()


def menu():
    while True:
        print("""
1 Add contact
2 Add phone
3 Move group
4 Search
5 Filter group
6 Export JSON
7 Import JSON
8 Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            add_phone()
        elif choice == "3":
            move_group()
        elif choice == "4":
            search()
        elif choice == "5":
            filter_group()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "8":
            break

menu()