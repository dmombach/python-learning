def add_contact(db, contact):
    db["contacts"].append(contact)


def find_contact(db, name):
    return next((c for c in db["contacts"] if c["name"] == name), None)


def list_contacts(db):
    return db["contacts"]
