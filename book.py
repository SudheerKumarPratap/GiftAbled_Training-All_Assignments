class Book:
    tot_books = 0
    def __init__(self,title,price):
        self.title=title
        self.price=price 
        Book.tot_books +=1

    def discount(self):
        self.price = self.price*0.90
        print(f" the  new price of '{self.title}' after 10%  discount is Rs.:{self.price:.2f}")
b1 = Book("Secret of AI",500)
b2 = Book(" Intro of Economics",562)
b3 = Book("Principles of maths",4522)
#print(b1)
#print(b2)
#print(b3) 

b1.discount()
b2.discount()
b3.discount()
print(f"No.of total books purchased on discount :{Book.tot_books}")
#print(f"{b2.tot_books}")
#print(f"{b3.tot_books}") 
    