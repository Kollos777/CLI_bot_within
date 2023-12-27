from collections import UserDict
from datetime import date, datetime


class Field:
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, phone):
        super().__init__(phone)
        self.validate_phone(phone)

        @property
        def phone(self):
            return self.__value

        @phone.setter
        def phone(self, phone_number):
            if not phone_number.isdigit() or len(phone_number) != 10:
                raise ValueError("Phone number must be a 10-digit number.")
            else:
                self.__value = phone_number

    def validate_phone(self, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be a 10-digit number.")


class Birthday(Field):

    def __init__(self, birthday=None):
        super().__init__(birthday)
        if birthday:
            try:
                birthday = datetime.strptime(birthday, "%d-%m-%Y").date()
            except ValueError:
                return "Incorrect birthday"

        @property
        def birthday(self):
            return self.__value

        @birthday.setter
        def birthday(self, birthday):
            try:
                birthday = datetime.strptime(birthday, "%d-%m-%Y").date()
            except ValueError:
                return "Incorrect birthday"
            self.__value = birthday


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break
        return f"Phone: {phone_number} not found"

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return phone.value

        raise ValueError(f"Phone: {old_phone} not found")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def days_to_birthday(self):
        print(self.birthday)
        if self.birthday.value is not None:
            today = date.today()
            user_birthday = datetime.strptime(self.birthday.value, '%d.%m.%Y')
            next_birthday = date(today.year, user_birthday.month, user_birthday.day)
        else:
            return None

        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year+1)

        number_of_days = next_birthday - today

        return number_of_days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, name):
        self.data[name.name.value] = name
        print(self.data)

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        return f"Name: {name} not found"

    def iterator(self, N=int):

        items = list(self.data.items())
        for i in range(0, len(items), N):
            yield items[i:i + N]


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
