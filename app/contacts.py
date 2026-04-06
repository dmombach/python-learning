contacts = []


def add_contact(name, phone):
    contact = {"name": name, "phone": phone}
    contacts.append(contact)


def remove_contact(name):
    for i, obj in enumerate(contacts):
        if obj.get("name") == name:
            contacts.pop(i)
            return True
    return False


def search_contact(name):
    # for obj in contacts:
    #     if obj["name"] == name:
    #         return obj
    # return None
    return next((c for c in contacts if c["name"] == name), None)


def list_contacts():
    return contacts
