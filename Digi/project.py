class Book:
    def _init_(self,title,author,price,quantity,book_type):
        self._title=title
        self._author=author
        self.price=price
        self._quantity=quantity
        self._type=book_type
def getTitle(self):
    return self._title
def getAuthor(self):
    return self._author
def getPrice(self):
    return self._price
def getQuantity(self):
    return self._quantity
def getType(self):
    return self._type
def setPrice(self,new_price):
    self._price=new_price
def setQuantity(self,new_quantity):
    self._quantity=new_quantity

def __repr__(self):
    return f"Book(Title={self._title}, Author={self._author}, Price={self.price}, Quantity={self.quantity}, Type={self._type})"

class User:
    def __init__(self,username,email,password):
        self._username=username
        self._email=email
        self._password=password
    def getUsername(self):
        return self._username
    def getEmail(self):
        return self._email
    def setEmail(self, new_email):
        self._email=new_email
    def setPassword(self,new_password):
        self._password=new_password
    def __repr__(self):
        return f"User(Username={self._username}, Email={self._email})"
class Order:
    def __init__(self,order_id,user,book,quantity):
        self._order_id=order_id
        self._user=user
        self._book=book
        self._quantity=quantity
    def getOrderId(self):
        return self._order_id
    def getUser(self):
        return self._user
    def getBook(self):
        return self._book
    def getQuantity(self):
        return self._quantity
    def setQuantity(self, new_quantity):
        self._quantity=new_quantity
    def __repr__(self):
        return f"Order_id={self._order_id}, User={self._user.getUsername()}, Book={self._book.getTitle()}, Quantity={self._quantity}"





    



book=Book("1984","George Orwell",15.99, 10,"Fiction")
user=User("johndoe","john@example.com","password123")
order=Order("1234",user,book,1)

print(book)
print(user)
print(order)

