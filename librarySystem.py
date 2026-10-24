class Book:
    """Represents a unique  book title in the system."""
    def __init__(self, isbn: str,title:str,author :str):
        self.isbn=isbn
        self.title=title
        self.author= author 
    def __str__(self):
        return f"'{self.title}' by {self.author}(ISBN:{self.isbn})"


class Library:
    """Represents a specific Library branches that manages its  own physical inventory."""    
    
    def __init__(self,name: str):
        self.name = name
        self.inventory = {}
        self.borrowed_records = {}
    def add_book(self,book: Book,copies : int =1):
        #self.book=Book
        """Represents a specific Library branches that manages its  own physical inventory."""    
        if copies  <=0:
            print("Number of  copies must be more than  zero.")
            return
        self.inventory[book] = self.inventory.get(book,0)+copies
        print(f" Added {copies}copy(ies) of {book} to {self.name}")
        
        #print("-" *40)    
    def show_book(self):
        print(f"\n ---Current Inventory at {self.name}---")
        if not self.inventory:
            print("there are no book available in this library")
            return 
            
        for book,count in self.inventory.items() :
            print(f"book_Details:{book}|available_copies:{count}")
        #print("-" *40)
    def borrow_book(self,user:str,book:Book):
        if user not in self.borrowed_records :
            self.borrowed_records[user]=[]

        if book in self.borrowed_records[user]:
            print(f" {user} has already borrowed a copy of {book.title}' from {self.name}"  
                  f" You can't borrow  the same book multiple time simultaneously.")
            return

        if self.inventory.get(book,00)>0:

            self.inventory[book] -= 1

            self.borrowed_records[user].append(book)
            print(f"{user} sucessfully borrowed '{book.title}' from {self.name}.")
        
        else:
            print(f" Sorry,'{book.title}' is currently out of stock at {self.name}")
        
    def show_borrower_info(self):
        """ Display who has borrowed books,how many books they have and their titles."""

        print(f"\nActive borrower Information at{self.name}---")
        has_borrowers = any(len(books)>0 for books in self.borrowed_records.values())
        if not self.borrowed_records or not has_borrowers:
            print(f" no books are currently borrowed from this library branch")
            return
        for user,book_list in self.borrowed_records.items():

            if book_list:
                num_books = len(book_list)

                book_names =",".join([f" '{book.title}'" for book in book_list])
                print(f"User Name : {user}")
                print(f"Total Books borrowed :{num_books}")
                print(f"Book Names : {book_names}\n")
        
          
                             
    def remaining_book(self):
        total_remaining = sum(self.inventory.values())
         
        print(f"total Remaining books at {self.name} :{total_remaining}")
               
if __name__ == "__main__" :
    b1= Book("978-01411439518"," Secret Cryptography","Rajkumar")
    b2= Book("978-01411439518"," Secret Science of AI","Dr.Mahesh kumar")
    #b3= Book("978-01411439518"," English  Grammar"," Dr. S.K. pratap")
    #b4= Book("978-01411439518"," Prem chand Literature","smt. Nidhi")
    #loc = Library("Local library")
    cen= Library("Central library")
    delh= Library("Delhi library")
    #nou= Library("IGNOU library")


print("\n---- Stocking the Libraries ----")

#loc.add_book(b1,copies = 125)
cen.add_book(b1,copies = 116)
delh.add_book(b2,copies = 133)
#nou.add_book(b4,copies = 253)

print("-" *40)
print("\n---- Showing the books----")
#loc.show_book()
cen.show_book()
delh.show_book()
#nou.show_book()
print("-" *40)

print("\n---- Borrowing  Simulation ----")
#loc.borrow_book("D.D Rawat",b1)
cen.borrow_book("Ram",b1)
delh.borrow_book("David",b2)
#nou.borrow_book("Dinesh",b4)
print("-" *40)

print("\n --- showing borrower_info---")
#lloc.show_borrower_info()
cen.show_borrower_info()
delh.show_borrower_info()
#nou.show_borrower_info()

print("-" *40)
print("\n --- showing Remaining Books_info---")
#loc.remaining_book()
cen.remaining_book()
delh.remaining_book()
#nou.remaining_book()


print("\n Welcome to the interactive Library System---")
user_name = input(" Your name:").strip()
print("\n Available Libraries:")
print("1. Central Library")
print("2. Delhi Library")
##print("3. Local Library")
#print("3. IGNOU Library")

lib_choice= input("Select a library number(1 or 2):").strip()
selected_lib = cen if lib_choice  == "1" else delh
print(f"\nBooks in System:")
print("1.Secret Cryptography")
print("2.Secret Science of AI")  
#print("3.English  Grammar")
#print("4.Prem chand Literature")

book_choice= input("Select a Book number to borrrow(1 or 2):").strip()
selected_book = b1 if book_choice == "1" else b2

print("\n ---- Processing  Transaction---")

selected_lib.borrow_book(user_name,selected_book)
selected_lib.show_book()


        
    