from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value):
        if not self.validate_date(value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    @staticmethod
    def validate_date(value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def string_to_date(date_string):
        return datetime.strptime(date_string, "%d.%m.%Y").date()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = None
        self.birthday = None

    def add_phone(self, phone):
        self.phone = (Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def edit_phone(self, new_phone):
        self.phones = new_phone

    def __str__(self):
        birthday_str = self.birthday.value if self.birthday else 'N/A'
        return f"Contact name: {self.name.value}, phone {self.phone}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        for record in self.data.values():
            if record.birthday:
                bday_date = Birthday.string_to_date(record.birthday.value)
                this_year_bday = bday_date.replace(year=today.year)
                if today <= this_year_bday <= today + timedelta(days=days):
                    upcoming_birthdays.append(record)
        return upcoming_birthdays


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "You haven't entered a contact name or phone!"
        except KeyError:
            return "Contact is not found!"
        except ValueError as e:
            return str(e)

    return inner


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Maybe you forgot enter name or phone?")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("You did not enter the subscriber's name!")
    if len(args) < 2:
        raise ValueError("You did not enter a new phone number!")
    name, new_phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    if not Phone.validate(new_phone):
        raise ValueError("Phone number must be 10 digits.")
    record.edit_phone(new_phone)
    return "Phone number updated."


@input_error
def get_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    return f"{name}: {record.phone}"


@input_error
def show_all(book: AddressBook):
    return '\n'.join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    return f"{name}: {record.birthday.value if record.birthday else 'N/A'}"


@input_error
def show_birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        raise ValueError("Протягом наступного тижня Днів Нардження немає!")
    return '\n'.join(str(record) for record in upcoming_birthdays)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if user_input == '':
            print("You have not entered anything")
            continue
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(get_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
