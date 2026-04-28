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


def sort_contacts():
    field = input("Sort by (name/birthday/date): ")

    conn = connect()
    cur = conn.cursor()

    if field == "name":
        cur.execute("SELECT name, email FROM contacts ORDER BY name")
    elif field == "birthday":
        cur.execute("SELECT name, email FROM contacts ORDER BY birthday")
    elif field == "date":
        cur.execute("SELECT name, email FROM contacts ORDER BY created_at")

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# 🔥 ПАГИНАЦИЯ ЧЕРЕЗ DB FUNCTION
def paginate():
    offset = 0
    limit = 3

    conn = connect()
    cur = conn.cursor()

    while True:
        cur.execute("SELECT * FROM get_contacts_page(%s,%s)", (limit, offset))

        rows = cur.fetchall()
        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break

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
    contacts = {}

    for row in data:
        name = row[0]

        if name not in contacts:
            contacts[name] = {
                "name": name,
                "email": row[1],
                "birthday": str(row[2]),
                "group": row[3],
                "phones": []
            }

        if row[4]:
            contacts[name]["phones"].append({
                "phone": row[4],
                "type": row[5]
            })

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(list(contacts.values()), f, indent=4)

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

        # 🔥 ФИКС ГРУППЫ
        group = item.get("group")
        if not group:
            group = "Other"

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists (1-skip / 2-overwrite): ")

            if choice == "1":
                continue
            elif choice == "2":
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
            else:
                continue

        cur.execute(
            "INSERT INTO contacts(name,email,birthday) VALUES (%s,%s,%s)",
            (name, email, birthday)
        )

        # 🔥 теперь всегда есть группа
        cur.execute("CALL move_to_group(%s,%s)", (name, group))

        for p in item.get("phones", []):
            cur.execute("CALL add_phone(%s,%s,%s)", (name, p["phone"], p["type"]))

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
8 Sort
9 Pagination
10 Exit
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
            sort_contacts()
        elif choice == "9":
            paginate()
        elif choice == "10":
            break

menu()