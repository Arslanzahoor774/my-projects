import datetime
import csv
from typing import List

class Customer:
    def __init__(self, customer_id, name, email, phone_number, birth_date, address):
        self.id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.address = address

    def __repr__(self):
        return f"Customer({self.id}, {self.name}, {self.email}, {self.phone_number}, {self.birth_date}, {self.address})"

    def calculate_age(self):
        today = datetime.date.today()
        birth_date = datetime.datetime.strptime(self.birth_date, "%Y-%m-%d").date()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Getters and Setters
    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def getPhoneNumber(self):
        return self.phone_number

    def getAddress(self):
        return self.address

    def setName(self, new_name):
        self.name = new_name

    def setEmail(self, new_email):
        self.email = new_email

    def setPhoneNumber(self, new_phone_number):
        self.phone_number = new_phone_number

    def setAddress(self, new_address):
        self.address = new_address

class CustomerManager:
    def __init__(self):
        self.customers = []

    def addCustomer(self, customer: Customer):
        self.customers.append(customer)

    def removeCustomer(self, customer: Customer):
        self.customers.remove(customer)

    def getCustomersByAgeRange(self, min_age: int, max_age: int) -> List[Customer]:
        return [customer for customer in self.customers if min_age <= customer.calculate_age() <= max_age]

    def getCustomersByAddress(self, address: str) -> List[Customer]:
        return [customer for customer in self.customers if customer.address == address]

    def exportData(self, filename: str):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Email', 'Phone Number', 'Birth Date', 'Address'])
            for customer in self.customers:
                writer.writerow([customer.id, customer.name, customer.email, customer.phone_number, customer.birth_date, customer.address])

# Example usage
try:
    customer_manager = CustomerManager()
    customer1 = Customer(1, "John Doe", "john@example.com", "1234567890", "1990-01-01", "123 Main St")
    customer_manager.addCustomer(customer1)
    customer_manager.exportData("customers.csv")
except Exception as e:
    print(f"An error occurred: {e}")
